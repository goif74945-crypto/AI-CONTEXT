"""Local-only approval and plan lifecycle HTTP API."""
from __future__ import annotations
import asyncio
import hmac
import os
import pathlib
import secrets
import threading
import time
from dataclasses import dataclass
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from .contracts import ExecuteRequest, PlanRequest, PlanView
from .executor import Executor, ActionError
from .planner import PlanningError, parse_llm, parse_rules
from .vision import VisionError
from .audit import AuditLog
from .assurance import analyze_plan, PlanScopeError

PORT = int(os.getenv("AI_AI_PORT", "8765"))
WEB = pathlib.Path(__file__).parent / "web"
HIGH_RISK_TOOLS = {"file.write", "code.run", "android.tap", "android.text", "android.open",
                   "android.swipe", "android.keyevent", "android.tap_text",
                   "desktop.click", "desktop.click_text", "desktop.hotkey", "desktop.type", "app.open", "app.launch",
                   "browser.open", "browser.click_text", "browser.fill"}
HIGH_RISK_TOOLS.add("browser.click_role")

@dataclass
class Stored:
    view: PlanView
    expires: float

class Runtime:
    def __init__(self, workspace: pathlib.Path, *, executor: Executor | None = None):
        self.executor = executor or Executor(workspace, enable_code_run=os.getenv("AI_AI_ENABLE_CODE_RUN") == "1")
        self.audit = AuditLog(self.executor.workspace)
        self.token = secrets.token_urlsafe(32)
        self.pending: dict[str, Stored] = {}
        self.pending_lock = threading.Lock()
        self.control_lock = threading.Lock()
        self.stop_generation = 0
        self.run_lock = asyncio.Lock()
        self.cancel = threading.Event()
        self.running = False

    def add(self, req: PlanRequest) -> PlanView:
        # A stop issued during long LLM/OCR planning must revoke *that* plan,
        # even if planning completes after stop and before the HTTP response.
        with self.control_lock:
            generation = self.stop_generation
        screen_evidence = (self.executor.read_screen_evidence() if req.share_screen_text else None)
        with self.control_lock:
            if generation != self.stop_generation:
                raise PlanningError("Plan invalidated by emergency stop while gathering screen evidence")
        proposal = parse_llm(req.text, screen_evidence=screen_evidence) if req.use_ai else parse_rules(req.text)
        assurance_warnings = analyze_plan(proposal.steps)
        risky = sorted({s.tool for s in proposal.steps if s.tool in HIGH_RISK_TOOLS})
        view = PlanView(id=secrets.token_hex(16), steps=proposal.steps,
            warnings=(["Changes on your device require direct approval. Review each step."] if risky else []) + assurance_warnings +
                     (["Visible OCR text was shared with the configured external AI provider."] if req.share_screen_text else []),
            clap_eligible=not risky, source="llm" if req.use_ai else "rules")
        with self.control_lock:
            if generation != self.stop_generation:
                raise PlanningError("Plan invalidated by emergency stop during planning")
            # Record prior to publishing an executable approval token.
            self.audit.record("PLAN_CREATED", plan_id=view.id, tools=[s.tool for s in proposal.steps], source=view.source)
            with self.pending_lock:
                now = time.monotonic()
                self.pending = {k:v for k,v in self.pending.items() if v.expires > now}
                if len(self.pending) >= 30:
                    oldest = next(iter(self.pending))
                    del self.pending[oldest]
                self.pending[view.id] = Stored(view=view, expires=now+180)
        return view

    def consume(self, plan_id: str) -> PlanView:
        with self.pending_lock:
            stored = self.pending.pop(plan_id, None)  # Single-use, including on errors
        if not stored or stored.expires <= time.monotonic():
            raise HTTPException(409, "Unknown, expired, or already executed plan")
        return stored.view


def make_app(workspace: pathlib.Path | None = None, *, executor: Executor | None = None) -> FastAPI:
    runtime = Runtime(workspace or pathlib.Path.cwd() / "workspace", executor=executor)
    app = FastAPI(title="AI.AI Local Agent", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.runtime = runtime

    @app.middleware("http")
    async def boundary(request: Request, call_next):
        host = request.headers.get("host", "")
        if host not in (f"127.0.0.1:{PORT}", f"localhost:{PORT}", "testserver"):
            return JSONResponse({"detail":"Localhost only"}, status_code=403)
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            origin = request.headers.get("origin", "")
            if origin not in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}") and host != "testserver":
                return JSONResponse({"detail":"Invalid request origin"}, status_code=403)
        return await call_next(request)

    def auth(token: str | None) -> None:
        if not token or not hmac.compare_digest(token, runtime.token):
            raise HTTPException(401, "Invalid local session token")

    @app.get("/")
    def home():
        return FileResponse(WEB / "index.html", media_type="text/html", headers={"Cache-Control":"no-store"})

    @app.get("/app.js")
    def script():
        return FileResponse(WEB / "app.js", media_type="text/javascript", headers={"Cache-Control":"no-store"})

    @app.get("/app.css")
    def style():
        return FileResponse(WEB / "app.css", media_type="text/css", headers={"Cache-Control":"no-store"})

    @app.get("/api/session")
    def session():
        return {"token":runtime.token, "code_run_enabled":runtime.executor.enable_code_run, "workspace":str(runtime.executor.workspace)}

    @app.post("/api/plan")
    async def plan(req: PlanRequest, x_ai_ai_token: str | None = Header(None)):
        auth(x_ai_ai_token)
        try:
            return await asyncio.to_thread(runtime.add, req)
        except (PlanningError, PlanScopeError, VisionError, ActionError) as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.post("/api/execute")
    async def execute(req: ExecuteRequest, x_ai_ai_token: str | None = Header(None)):
        auth(x_ai_ai_token)
        with runtime.control_lock:
            expected_generation = runtime.stop_generation
        if runtime.run_lock.locked():
            raise HTTPException(409, "Another plan is executing")
        async with runtime.run_lock:
            plan_view = runtime.consume(req.plan_id)
            with runtime.control_lock:
                if runtime.stop_generation != expected_generation:
                    raise HTTPException(409, "Execution invalidated by emergency stop")
                runtime.cancel.clear()
                runtime.running = True
            results = []
            try:
                # If the audit cannot be opened, fail closed before any user action.
                runtime.audit.record("EXECUTION_STARTED", plan_id=plan_view.id)
                for index, step in enumerate(plan_view.steps):
                    if runtime.cancel.is_set():
                        runtime.audit.record("EXECUTION_STOPPED", plan_id=plan_view.id, at=index)
                        return {"status":"STOPPED", "steps":results, "at":index}
                    try:
                        message = await asyncio.to_thread(runtime.executor.perform, step, runtime.cancel)
                        results.append({"index":index, "tool":step.tool, "status":"PASS", "message":message[:20000]})
                        runtime.audit.record("STEP_OK", plan_id=plan_view.id, index=index, tool=step.tool)
                    except Exception as exc:
                        if runtime.cancel.is_set():
                            runtime.audit.record("EXECUTION_STOPPED", plan_id=plan_view.id, at=index)
                            return {"status":"STOPPED", "steps":results, "at":index}
                        runtime.audit.record("EXECUTION_FAILED", plan_id=plan_view.id, index=index,
                                             tool=step.tool, error_type=type(exc).__name__)
                        return {"status":"FAIL", "steps":results, "failed_index":index,
                                "error":f"{type(exc).__name__}: {str(exc)[:500]}"}
                runtime.audit.record("EXECUTION_COMPLETE", plan_id=plan_view.id, steps=len(results))
                return {"status":"PASS", "steps":results}
            finally:
                runtime.running = False

    @app.post("/api/stop")
    async def stop(x_ai_ai_token: str | None = Header(None)):
        auth(x_ai_ai_token)
        with runtime.control_lock:
            runtime.stop_generation += 1
            runtime.cancel.set()
            was_running = runtime.running
            # Lock order: control_lock -> pending_lock. No opposite nesting is used.
            with runtime.pending_lock:
                discarded = len(runtime.pending)
                runtime.pending.clear()
        return {"stop_requested":True, "running":was_running, "pending_discarded":discarded}

    @app.get("/api/status")
    def status():
        return {"running":runtime.running, "approval_required":True, "bind":"loopback-only"}

    @app.get("/api/history")
    def history(x_ai_ai_token: str | None = Header(None)):
        auth(x_ai_ai_token)
        return {"events":runtime.audit.recent()}

    return app
