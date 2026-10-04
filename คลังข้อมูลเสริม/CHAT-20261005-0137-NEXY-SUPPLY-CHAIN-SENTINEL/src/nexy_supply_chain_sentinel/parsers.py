from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .policy import Policy

_REQUIREMENT_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;]+)(.*)$")
_HASH_RE = re.compile(r"--hash=sha256:([0-9a-fA-F]{64})(?=\s|$)")
_NAME_NORMALIZE_RE = re.compile(r"[-_.]+")


def _violation(code: str, subject: str, message: str) -> dict[str, str]:
    return {"code": code, "subject": subject, "message": message}


def _package(ecosystem: str, name: str, version: str, source: str, integrity: str) -> dict[str, str]:
    return {
        "ecosystem": ecosystem,
        "name": name,
        "version": version,
        "source": source,
        "integrity": integrity,
    }


def parse_dependency_file(path: Path, policy: Policy) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "unknown", [], [_violation("INPUT_NOT_UTF8", path.name, "dependency input must be valid UTF-8")]
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return _parse_requirements(text, policy)
    if isinstance(parsed, dict) and "lockfileVersion" in parsed and "packages" in parsed:
        return _parse_npm_lock(parsed, policy)
    return "unknown", [], [_violation("UNSUPPORTED_DEPENDENCY_INPUT", path.name, "JSON input is not a supported npm package-lock structure")]


def _parse_npm_lock(data: dict[str, Any], policy: Policy) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
    violations: list[dict[str, str]] = []
    packages_out: list[dict[str, str]] = []
    version = data.get("lockfileVersion")
    if version not in (2, 3):
        violations.append(_violation("NPM_UNSUPPORTED_LOCKFILE_VERSION", "package-lock.json", f"lockfileVersion {version!r} is not supported"))
    packages = data.get("packages")
    if not isinstance(packages, dict):
        return "npm-package-lock", [], violations + [_violation("NPM_INVALID_PACKAGES_MAP", "packages", "packages must be an object")]

    seen: set[tuple[str, str, str, str, str]] = set()
    for package_path in sorted(packages):
        if package_path == "":
            continue
        meta = packages[package_path]
        if not isinstance(meta, dict):
            violations.append(_violation("NPM_INVALID_PACKAGE_RECORD", package_path, "package record must be an object"))
            continue
        marker = "node_modules/"
        if marker not in package_path:
            violations.append(_violation("NPM_UNSUPPORTED_PACKAGE_PATH", package_path, "package path does not identify node_modules content"))
            continue
        name = package_path.rsplit(marker, 1)[1].strip()
        pkg_version = meta.get("version")
        resolved = meta.get("resolved")
        integrity = meta.get("integrity", "")
        if not name:
            violations.append(_violation("NPM_MISSING_NAME", package_path, "package name cannot be derived"))
            continue
        if not isinstance(pkg_version, str) or not pkg_version.strip():
            violations.append(_violation("NPM_MISSING_VERSION", name, "package version is missing"))
            continue
        if not isinstance(resolved, str) or not resolved.strip():
            violations.append(_violation("NPM_MISSING_RESOLVED_SOURCE", name, "resolved source URL is missing"))
            resolved = ""
        else:
            parsed = urlparse(resolved)
            if parsed.scheme.lower() != "https":
                violations.append(_violation("NPM_SOURCE_SCHEME_NOT_ALLOWED", name, "resolved source must use https"))
            host = (parsed.hostname or "").lower()
            if host not in policy.allowed_npm_hosts:
                violations.append(_violation("NPM_SOURCE_HOST_NOT_ALLOWED", name, f"resolved host {host or '<missing>'} is not allowed"))
            if parsed.username is not None or parsed.password is not None:
                violations.append(_violation("NPM_SOURCE_CREDENTIALS_FORBIDDEN", name, "resolved source must not embed credentials"))
            if parsed.query or parsed.fragment:
                violations.append(_violation("NPM_SOURCE_QUERY_OR_FRAGMENT_FORBIDDEN", name, "resolved source must not contain query or fragment data"))
            try:
                port = parsed.port
            except ValueError:
                port = None
                violations.append(_violation("NPM_SOURCE_PORT_INVALID", name, "resolved source contains an invalid port"))
            safe_netloc = host
            if port is not None:
                safe_netloc = f"{safe_netloc}:{port}"
            resolved = f"{parsed.scheme.lower()}://{safe_netloc}{parsed.path}" if parsed.scheme else parsed.path
        if not isinstance(integrity, str):
            violations.append(_violation("INVALID_INTEGRITY", name, "integrity must be a string"))
            integrity = ""
        if policy.require_integrity and not integrity.strip():
            violations.append(_violation("MISSING_INTEGRITY", name, "integrity evidence is required"))
        record = _package("npm", name, pkg_version.strip(), resolved.strip(), integrity.strip())
        key = tuple(record[k] for k in ("ecosystem", "name", "version", "source", "integrity"))
        if key not in seen:
            seen.add(key)
            packages_out.append(record)
    return "npm-package-lock", packages_out, violations


def _parse_requirements(text: str, policy: Policy) -> tuple[str, list[dict[str, str]], list[dict[str, str]]]:
    violations: list[dict[str, str]] = []
    packages_out: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for line_no, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("\\"):
            violations.append(_violation("PYTHON_LINE_CONTINUATION_UNSUPPORTED", f"line:{line_no}", "multi-line requirements are not supported in v0.1"))
            continue
        match = _REQUIREMENT_RE.match(line)
        if not match:
            violations.append(_violation("PYTHON_UNPINNED_OR_UNSUPPORTED_REQUIREMENT", f"line:{line_no}", "requirement must use exact name==version syntax"))
            continue
        name, version, tail = match.groups()
        normalized_name = _NAME_NORMALIZE_RE.sub("-", name).lower()
        hashes = sorted(set(_HASH_RE.findall(tail)))
        remainder = _HASH_RE.sub("", tail).strip()
        if remainder:
            violations.append(_violation("PYTHON_UNSUPPORTED_OPTION", f"line:{line_no}", "only sha256 --hash options are supported after the exact pin"))
        if policy.require_integrity and not hashes:
            violations.append(_violation("MISSING_INTEGRITY", normalized_name, "sha256 hash evidence is required"))
        integrity = "|".join(f"sha256:{h.lower()}" for h in hashes)
        record = _package("pypi", normalized_name, version, "requirements.txt", integrity)
        key = tuple(record[k] for k in ("ecosystem", "name", "version", "source", "integrity"))
        if key not in seen:
            seen.add(key)
            packages_out.append(record)
    return "python-requirements", packages_out, violations
