"""Render .excalidraw -> SVG (Excalidraw exportToSvg) -> PNG (screenshot), headless.
Polls for the Excalidraw UMD global (name auto-detected), exports SVG (DOM-based,
headless-safe), then screenshots the SVG at 2x for a crisp PNG."""
import json, pathlib, time
from patchright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent
VER = "0.17.6"
FILES = ["01-pipeline", "02-autonomy-build-mode", "03-self-learning-trio"]
CDN = f"https://unpkg.com/@excalidraw/excalidraw@{VER}/dist"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(device_scale_factor=2)
    page = ctx.new_page()
    page.on("pageerror", lambda e: None)
    page.goto("about:blank")
    page.evaluate(f"window.EXCALIDRAW_ASSET_PATH = '{CDN}/';")
    for u in ["https://unpkg.com/react@18/umd/react.production.min.js",
              "https://unpkg.com/react-dom@18/umd/react-dom.production.min.js",
              f"{CDN}/excalidraw.production.min.js"]:
        try:
            page.add_script_tag(url=u)
        except Exception as e:
            print("script load issue:", u, str(e)[:80])

    glob = None
    for i in range(45):
        try:
            glob = page.evaluate("""() => {
                for (const k of ['ExcalidrawLib','Excalidraw']) {
                    if (window[k] && typeof window[k].exportToSvg === 'function') return k;
                }
                return null;
            }""")
        except Exception:
            glob = None
        if glob:
            break
        time.sleep(1)
    if not glob:
        keys = page.evaluate("() => Object.keys(window).filter(k => /excal|react/i.test(k))")
        raise SystemExit(f"no excalidraw export global found. excal/react globals = {keys}")
    print("using global:", glob)

    for f in FILES:
        scene = json.loads((OUT / f"{f}.excalidraw").read_text(encoding="utf-8"))
        svg_html = page.evaluate(
            """async ([g, scene]) => {
                const svg = await window[g].exportToSvg({
                    elements: scene.elements,
                    appState: { ...scene.appState, exportBackground: true,
                                viewBackgroundColor: '#ffffff', exportPadding: 16 },
                    files: scene.files || {},
                });
                return svg.outerHTML;
            }""", [glob, scene])
        (OUT / f"{f}.svg").write_text(svg_html, encoding="utf-8")
        shot = ctx.new_page()
        shot.set_content(f'<!doctype html><html><body style="margin:0;display:inline-block">{svg_html}</body></html>')
        shot.wait_for_selector("svg")
        shot.locator("svg").screenshot(path=str(OUT / f"{f}.png"))
        shot.close()
        kb = (OUT / f"{f}.png").stat().st_size // 1024
        print(f"rendered {f}.svg + {f}.png ({kb} KB)")
    browser.close()
print("done")
