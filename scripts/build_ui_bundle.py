"""Build a static, offline-ready bundle of the Operator UI assets."""
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_SRC = Path(__file__).resolve().parent.parent / "ui"
DEFAULT_DIST = Path(__file__).resolve().parent.parent / "dist" / "operator_ui"
DEFAULT_ZIP = Path(__file__).resolve().parent.parent / "dist" / "operator_ui.zip"


def _default_paths_from_env() -> tuple[Path, Path, Path | None]:
    """Resolve default paths, allowing environment overrides."""

    env_src = os.environ.get("OPERATOR_UI_SRC")
    env_dist = os.environ.get("OPERATOR_UI_DIST")
    env_zip = os.environ.get("OPERATOR_UI_ZIP")

    src = Path(env_src) if env_src else DEFAULT_SRC
    dist = Path(env_dist) if env_dist else DEFAULT_DIST

    if env_zip is not None:
        zip_path: Path | None = Path(env_zip) if env_zip else None
    else:
        zip_path = dist.parent / "operator_ui.zip"

    return src, dist, zip_path


def build_ui_bundle(src: Path = DEFAULT_SRC, dist: Path = DEFAULT_DIST, zip_path: Path | None = DEFAULT_ZIP) -> Path:
    """Copy static UI assets into a dist folder and optionally zip them."""

    src = Path(src)
    dist = Path(dist)

    if not src.exists():
        raise FileNotFoundError(f"UI source directory does not exist: {src}")

    dist_root = dist.parent
    dist_root.mkdir(parents=True, exist_ok=True)

    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(src, dist)

    if zip_path:
        zip_path = Path(zip_path)
        if zip_path.exists():
            zip_path.unlink()
        with ZipFile(zip_path, "w", ZIP_DEFLATED) as bundle:
            for path in dist.rglob("*"):
                bundle.write(path, arcname=path.relative_to(dist.parent))

    return dist


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default_src, default_dist, default_zip = _default_paths_from_env()

    parser = argparse.ArgumentParser(description="Bundle the offline Operator UI")
    parser.add_argument(
        "--src",
        type=Path,
        default=default_src,
        help="UI source directory (default: ui/ or OPERATOR_UI_SRC)",
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=default_dist,
        help="Output directory for bundled assets (or OPERATOR_UI_DIST)",
    )
    parser.add_argument(
        "--zip",
        dest="zip_path",
        type=Path,
        default=default_zip,
        help="Optional zip output path (default: dist/operator_ui.zip or OPERATOR_UI_ZIP)",
    )
    parser.add_argument("--no-zip", dest="zip_path", action="store_const", const=None, help="Skip creating a zip archive")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    bundle_path = build_ui_bundle(src=args.src, dist=args.dist, zip_path=args.zip_path)
    print(f"UI bundle written to {bundle_path}")
    if args.zip_path:
        print(f"Zip archive written to {args.zip_path}")


if __name__ == "__main__":
    main()
