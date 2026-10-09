"""Start the local-only assistant: python -m ai_ai.main"""
from __future__ import annotations
import os
import pathlib
import uvicorn
from .server import make_app

app = make_app()

def main():
    port = int(os.getenv("AI_AI_PORT", "8765"))
    if not (1024 <= port <= 65535):
        raise SystemExit("AI_AI_PORT must be between 1024 and 65535")
    print(f"AI.AI: Open http://127.0.0.1:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port, access_log=False)

if __name__ == "__main__":
    main()
