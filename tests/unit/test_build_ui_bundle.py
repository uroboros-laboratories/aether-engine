from scripts.build_ui_bundle import build_ui_bundle, parse_args


def test_build_ui_bundle_honours_env_defaults(monkeypatch, tmp_path):
    src_dir = tmp_path / "ui_src"
    dist_dir = tmp_path / "custom_dist"
    src_dir.mkdir()
    (src_dir / "index.html").write_text("hello")

    monkeypatch.setenv("OPERATOR_UI_SRC", str(src_dir))
    monkeypatch.setenv("OPERATOR_UI_DIST", str(dist_dir))

    args = parse_args([])

    assert args.src == src_dir
    assert args.dist == dist_dir
    # Default zip path should follow the dist parent when no explicit env zip is set.
    expected_zip = dist_dir.parent / "operator_ui.zip"
    assert args.zip_path == expected_zip

    bundle_path = build_ui_bundle(src=args.src, dist=args.dist, zip_path=args.zip_path)

    assert bundle_path == dist_dir
    assert (dist_dir / "index.html").read_text() == "hello"
    assert expected_zip.exists()


def test_build_ui_bundle_env_can_disable_zip(monkeypatch, tmp_path):
    src_dir = tmp_path / "src"
    dist_dir = tmp_path / "dist"
    src_dir.mkdir()
    (src_dir / "index.html").write_text("hello")

    monkeypatch.setenv("OPERATOR_UI_SRC", str(src_dir))
    monkeypatch.setenv("OPERATOR_UI_DIST", str(dist_dir))
    monkeypatch.setenv("OPERATOR_UI_ZIP", "")

    args = parse_args([])
    assert args.zip_path is None

    build_ui_bundle(src=args.src, dist=args.dist, zip_path=args.zip_path)

    assert dist_dir.exists()
    assert not (dist_dir.parent / "operator_ui.zip").exists()
