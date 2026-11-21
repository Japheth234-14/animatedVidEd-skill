# Notion Workflows for Video & Motion Production

Use Notion as the production hub for video briefs, scripts, storyboards, KPI data sources, and render logs—either through **AI Agent Notion Connector tools** or programmatically via **`scripts/notion_sync.py`** (`notion-client` / Notion REST API).

---

## 1. Two Ways to Execute Notion Actions

### Option A: Connected Notion App (Inside AI Agents like Arena)
When Notion is enabled as a connected app, always call `list_connector_tools("notion")` first, then use the discovered tool names and real IDs from earlier `search` / `fetch` results:

- **Find briefs, scripts, or databases:** Search by title/keyword, then fetch the page or query the database.
- **Create a video project page or storyboard:** Create pages inside a target parent page or database with structured properties (`Status`, `Format`, `Target Duration`, `Aspect Ratio`) and Markdown/block body (Hook, Scene Breakdown, Narration Script, Visual Notes).
- **Update status & log deliverables:** After rendering (`render.py`) or editing (`video_edit.py`), update the Notion item's `Status` (`Draft` -> `In Review` -> `Rendered`) and append render metadata (resolution, fps, duration, file path, transcript summary).
- **Drive data visualizations from Notion databases:** Query numeric columns (e.g., sprint velocity, monthly revenue, video metrics) and pass the parsed JSON directly into `templates/data_viz_dashboard.py` or `templates/math_code_and_diagrams.py`.

### Option B: Python CLI & Automation (`scripts/notion_sync.py`)
Set `NOTION_TOKEN` (from a Notion internal integration) and use `scripts/notion_sync.py` (works via `notion-client` if installed, with a zero-dependency `urllib` fallback):

```bash
export NOTION_TOKEN="ntn_..."

# Search pages & databases
python3 scripts/notion_sync.py search "Video Roadmap"

# Read a page's blocks as clean Markdown/text
python3 scripts/notion_sync.py read-page <PAGE_ID>

# Query a database and export rows as JSON (ready to feed into Manim charts!)
python3 scripts/notion_sync.py query-db <DATABASE_ID> --out metrics.json

# Create a new video storyboard page inside a database or parent page
python3 scripts/notion_sync.py create-page --parent-db <DATABASE_ID> \
  --title "Product Launch Reel" --status "Draft" --body-file storyboard.md

# Update status / properties on an existing page
python3 scripts/notion_sync.py update-status <PAGE_ID> --prop Status --value "Rendered"

# Log a rendered MP4's metadata (duration, resolution, fps) directly onto a Notion page
python3 scripts/notion_sync.py log-render <PAGE_ID> --video out.mp4 --notes "1080p60 crossfade master"

# Append text/heading/todo/callout blocks or post a comment
python3 scripts/notion_sync.py append <PAGE_ID> --text "Scene 3 camera tracking verified"
python3 scripts/notion_sync.py comment <PAGE_ID> --text "Ready for final review!"
```

---

## 2. End-to-End Notion -> Manim -> Video Edit Pipelines

1. **Notion Script / Storyboard -> Manim Video:**
   - Fetch the Notion page (`read-page` or connector fetch) containing scene timestamps, voiceover lines, and visual cues.
   - Generate the Manim scene (`templates/motion_graphics_camera.py`, `templates/character_rig_scene.py`, `templates/loaders_and_microinteractions.py`).
   - Optionally synthesize or align narration (`faster-whisper` / TTS) and run `scripts/video_edit.py mux-audio`.
   - Log the finished deliverable back to Notion (`log-render` + status update).

2. **Notion Database -> Animated Manim Chart / Dashboard:**
   - Export rows with `scripts/notion_sync.py query-db <DB_ID> --out data.json`.
   - Load `data.json` inside a Manim `Scene` using `BarChart`, `Axes`, `Table`, and `AnnularSector` (remember `label_constructor=Text` for zero-LaTeX rendering).
   - Render `1080p60` (`landscape` or `portrait`) and attach the summary back to Notion.

3. **Notion Content Calendar -> Batch Social Reels:**
   - Query items where `Status == "Ready to Render"`.
   - Render each reel (`--preset portrait`), auto-generate captions (`video_edit.py auto-captions`), combine highlight compilations (`video_edit.py combine`), and update every Notion row to `"Rendered"`.
