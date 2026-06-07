"""Generate editable .excalidraw source files for the agent-builder README.
Emits three diagrams: pipeline, autonomy+build-mode, self-learning trio.
Run: python docs/diagrams/build_diagrams.py
"""
import json, random, pathlib

OUT = pathlib.Path(__file__).parent
random.seed(7)

def _id(): return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(12))
def _nonce(): return random.randint(1, 2_000_000_000)

LAV = "#e9e7fd"; LAV_S = "#5b53c6"; INK = "#1e1e1e"; GREEN = "#e7f5e9"; GREEN_S = "#2f9e44"
AMBER = "#fff4e0"; AMBER_S = "#e8893b"; WHITE = "#ffffff"

def rect(x, y, w, h, fill=LAV, stroke=LAV_S):
    return {"id": _id(), "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
            "angle": 0, "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": {"type": 3}, "seed": _nonce(),
            "version": 1, "versionNonce": _nonce(), "isDeleted": False, "boundElements": [],
            "updated": 1, "link": None, "locked": False}

def text(x, y, w, h, s, size=16, color=INK, align="center"):
    return {"id": _id(), "type": "text", "x": x, "y": y, "width": w, "height": h, "angle": 0,
            "strokeColor": color, "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": None, "seed": _nonce(), "version": 1,
            "versionNonce": _nonce(), "isDeleted": False, "boundElements": [], "updated": 1,
            "link": None, "locked": False, "text": s, "fontSize": size, "fontFamily": 1,
            "textAlign": align, "verticalAlign": "middle", "containerId": None,
            "originalText": s, "lineHeight": 1.25, "baseline": int(h * 0.75)}

def box(x, y, w, h, label, fill=LAV, stroke=LAV_S, size=16):
    return [rect(x, y, w, h, fill, stroke), text(x + 8, y + h / 2 - (size * 1.25 * label.count(chr(10)) + size) / 2,
                                                 w - 16, size * 1.25 * (label.count(chr(10)) + 1), label, size)]

def arrow(x1, y1, x2, y2):
    return {"id": _id(), "type": "arrow", "x": x1, "y": y1, "width": abs(x2 - x1), "height": abs(y2 - y1),
            "angle": 0, "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid", "roughness": 1, "opacity": 100, "groupIds": [],
            "frameId": None, "roundness": {"type": 2}, "seed": _nonce(), "version": 1,
            "versionNonce": _nonce(), "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
            "locked": False, "points": [[0, 0], [x2 - x1, y2 - y1]], "lastCommittedPoint": None,
            "startBinding": None, "endBinding": None, "startArrowhead": None, "endArrowhead": "arrow"}

def save(name, els):
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": els, "appState": {"viewBackgroundColor": WHITE, "gridSize": None}, "files": {}}
    (OUT / f"{name}.excalidraw").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print("wrote", name + ".excalidraw", "(", len(els), "elements )")

# ---- Diagram 1: the pipeline ----
e = []
e += [text(40, 20, 700, 30, "agent-builder pipeline:  idea  →  reliable, eval-ready PRD", 22, LAV_S, "left")]
e += box(40, 80, 150, 60, "Product idea", WHITE, INK)
e += [arrow(190, 110, 250, 110)]
e += box(250, 70, 200, 80, "GATES\nworth-an-agent\nagent-vs-workflow\ncan-we-eval-it", GREEN, GREEN_S, 14)
e += [arrow(450, 110, 510, 110)]
e += box(510, 60, 240, 100, "SECTIONS (10)\nscope · tools · memory\neval* · hitl* · safety\nreliability* · model+cost\nobservability · learning*", LAV, LAV_S, 12)
e += [arrow(630, 160, 630, 210)]
e += box(510, 210, 240, 50, "agent-prd  (assemble)", WHITE, INK, 15)
e += [arrow(510, 235, 450, 235)]
e += box(250, 210, 200, 50, "agent-prd-review  (critic)", AMBER, AMBER_S, 14)
e += [arrow(350, 260, 350, 300)]
e += box(250, 300, 200, 50, "Shippable PRD", GREEN, GREEN_S, 15)
e += [text(40, 380, 720, 20, "* = the differentiator sections most agent PRDs skip", 13, AMBER_S, "left")]
save("01-pipeline", e)

# ---- Diagram 2: autonomy ladder + build mode ----
e = []
e += [text(40, 20, 700, 30, "Pick the LEAST autonomy + simplest build mode that works", 20, LAV_S, "left")]
e += box(40, 80, 220, 55, "L0  decider-node\nLLM choice in a fixed workflow", WHITE, INK, 13)
e += [arrow(150, 135, 150, 160)]
e += box(40, 160, 220, 55, "L1  agent\nmemory + tools + retry", LAV, LAV_S, 13)
e += [arrow(150, 215, 150, 240)]
e += box(40, 240, 220, 55, "L2  high-autonomy\nplans · subtasks · sub-agents", AMBER, AMBER_S, 13)
e += [text(40, 320, 240, 20, "lower is safer + cheaper", 13, GREEN_S, "left")]
e += [text(360, 70, 380, 24, "Build mode", 18, INK, "left")]
e += box(360, 105, 380, 60, "Code-first agent framework (Mastra-style)\nagent owns control flow · fast · type-safe", LAV, LAV_S, 12)
e += box(360, 180, 380, 60, "Durable workflow engine (Conductor / Temporal)\nretries · scheduling · survives restart · HITL@scale", GREEN, GREEN_S, 12)
e += box(360, 255, 380, 70, "RULE: reach for the durable engine when it\ncalls external APIs, runs hours/days, or must\noutlive a worker restart. Else go code-first.", WHITE, AMBER_S, 12)
save("02-autonomy-build-mode", e)

# ---- Diagram 3: the self-learning trio ----
e = []
e += [text(40, 20, 720, 30, "\"Self-learning\" = three sections working together", 20, LAV_S, "left")]
e += box(60, 90, 200, 70, "MEMORY\nworking / semantic / observational", LAV, LAV_S, 13)
e += box(300, 90, 200, 70, "EVAL LOOP\ngolden set · rubric · regression gate", GREEN, GREEN_S, 13)
e += box(540, 90, 200, 70, "SELF-IMPROVE\ntraces → datasets → re-eval → fix", AMBER, AMBER_S, 13)
e += [arrow(260, 125, 300, 125), arrow(500, 125, 540, 125)]
e += [arrow(640, 160, 160, 200)]
e += box(60, 200, 680, 50, "Reliable, self-learning agent  (ship all three, or drop the claim)", WHITE, INK, 15)
e += [text(40, 290, 720, 24, "The other reliability pillars: HITL boundaries · guardrails · failure premortem · observability", 13, INK, "left")]
save("03-self-learning-trio", e)
