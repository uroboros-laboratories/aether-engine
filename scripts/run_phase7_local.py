"""Start the Operator Service and serve the offline UI from a single command."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer

from build_ui_bundle import build_ui_bundle, DEFAULT_DIST, DEFAULT_SRC


def _get_env_default(name: str, fallback: str) -> str:
    return os.environ.get(name, fallback)


def _get_env_default_int(name: str, fallback: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return fallback
    try:
        return int(value)
    except ValueError:
        return fallback


def _start_static_server(directory: Path, host: str, port: int) -> TCPServer:
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    httpd = TCPServer((host, port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def _start_operator_service(host: str, port: int, repo_root: Path) -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{repo_root / 'src'}{os.pathsep}{env.get('PYTHONPATH', '')}".rstrip(os.pathsep)

    cmd = [
        sys.executable,
        "-m",
        "operator_service",
        "--host",
        host,
        "--port",
        str(port),
        "--repo-root",
        str(repo_root),
    ]
    return subprocess.Popen(cmd, env=env)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 7 offline stack (Operator Service + UI)")
    parser.add_argument(
        "--service-host",
        default=_get_env_default("OPERATOR_SERVICE_HOST", "127.0.0.1"),
        help="Operator Service host (default: 127.0.0.1 or OPERATOR_SERVICE_HOST)",
    )
    parser.add_argument(
        "--service-port",
        type=int,
        default=_get_env_default_int("OPERATOR_SERVICE_PORT", 8000),
        help="Operator Service port (default: 8000 or OPERATOR_SERVICE_PORT)",
    )
    parser.add_argument(
        "--ui-host",
        default=_get_env_default("OPERATOR_UI_HOST", "127.0.0.1"),
        help="UI static server host (default: 127.0.0.1 or OPERATOR_UI_HOST)",
    )
    parser.add_argument(
        "--ui-port",
        type=int,
        default=_get_env_default_int("OPERATOR_UI_PORT", 9000),
        help="UI static server port (default: 9000 or OPERATOR_UI_PORT)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        default=os.environ.get("OPERATOR_UI_NO_BROWSER") is not None,
        help="Do not automatically open the browser after startup (or set OPERATOR_UI_NO_BROWSER)",
    )
    parser.add_argument(
        "--ui-src",
        type=Path,
        default=Path(_get_env_default("OPERATOR_UI_SRC", str(DEFAULT_SRC))),
        help="Source directory for UI assets (default: ui/ or OPERATOR_UI_SRC)",
    )
    parser.add_argument(
        "--ui-dist",
        type=Path,
        default=Path(_get_env_default("OPERATOR_UI_DIST", str(DEFAULT_DIST))),
        help="Output directory for bundled UI assets (default: dist/operator_ui or OPERATOR_UI_DIST)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent

    bundle_path = build_ui_bundle(src=args.ui_src, dist=args.ui_dist)
    httpd = _start_static_server(bundle_path, host=args.ui_host, port=args.ui_port)
    service_proc = _start_operator_service(args.service_host, args.service_port, repo_root=repo_root)

    ui_url = f"http://{args.ui_host}:{args.ui_port}".replace("0.0.0.0", "127.0.0.1")
    service_url = f"http://{args.service_host}:{args.service_port}".replace("0.0.0.0", "127.0.0.1")

    print("Phase 7 stack is running:")
    print(f"  Operator Service: {service_url}")
    print(f"  Operator UI:      {ui_url}")
    print("Press Ctrl+C to stop both servers.")

    if not args.no_browser:
        webbrowser.open(ui_url)

    try:
        service_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.shutdown()
        service_proc.terminate()
        try:
            service_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            service_proc.kill()


if __name__ == "__main__":
    main()
