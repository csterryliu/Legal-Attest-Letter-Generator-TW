"""
Web UI for the generator: form (sender/receiver/cc + article) with a
real-time layout preview, served over plain stdlib HTTP so no extra
package install is required.

The preview redraws in the browser on every keystroke using a JS port of
core._parse_main_article's char/line/page counters. The final PDF is still
produced by the real core.py/pdfpainter.py pipeline when the user exports.
"""
import json
import os
import tempfile
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import core
from .constants import CONTENT_MAX_CHARACTER_PER_LINE, CONTENT_MAX_LINE_PER_PAGE, VERSION

DEFAULT_PORT = 8420

PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>台灣郵局存證信函產生器 {version}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: "Microsoft JhengHei", "PingFang TC", sans-serif;
    background: #f2f1ec; color: #222;
  }}
  header {{ background: #7a2e2e; color: #fff; padding: 10px 20px; font-size: 16px; }}
  main {{ display: flex; gap: 20px; padding: 16px 24px 40px; max-width: 1100px; margin: 0 auto; }}
  .col {{ flex: 1; min-width: 320px; }}
  h2 {{ font-size: 15px; margin: 16px 0 8px; color: #333; }}
  h2:first-child {{ margin-top: 0; }}
  label {{ font-size: 12px; color: #555; display: block; margin-bottom: 2px; }}
  input[type=text], textarea {{
    width: 100%; font-size: 14px; padding: 6px 8px; border: 1px solid #ccc;
    border-radius: 4px; font-family: inherit;
  }}
  textarea {{ resize: vertical; }}
  .row {{ display: flex; gap: 8px; margin-bottom: 6px; align-items: flex-end; }}
  .row > div {{ flex: 1; }}
  fieldset {{ border: 1px solid #ddd; border-radius: 6px; margin-bottom: 10px; }}
  legend {{ font-size: 13px; color: #7a2e2e; padding: 0 6px; }}
  .btn {{ font-size: 12px; border-radius: 4px; padding: 4px 10px; cursor: pointer; }}
  .btn-add {{ background: none; border: 1px dashed #999; color: #555; }}
  .btn-remove {{ background: none; border: 1px solid #ccc; color: #a33; flex: 0 0 auto; padding: 6px 8px; }}
  .btn-primary {{ background: #7a2e2e; color: #fff; border: none; font-size: 14px; padding: 10px 18px; }}
  .btn-primary:disabled {{ background: #b99; cursor: wait; }}
  .entry-group {{ margin-bottom: 6px; }}
  #status {{ font-size: 12px; margin-top: 8px; color: #555; min-height: 1.2em; }}
  #status.error {{ color: #b00; }}

  .letter-page {{
    background: #fffdf7; border: 1px solid #b8a98a; aspect-ratio: 8.2677/11.692;
    width: 100%; max-width: 460px; margin: 0 auto 14px; position: relative;
    box-shadow: 0 2px 6px rgba(0,0,0,.15);
  }}
  .grid-area {{
    position: absolute; left: 15%; top: 33%; right: 4%;
    display: grid; grid-template-columns: repeat({chars}, 1fr); gap: 1px;
  }}
  .cell {{
    aspect-ratio: 1/1; border: 0.5px solid #e3ddc9; font-size: 11px;
    display: flex; align-items: center; justify-content: center;
  }}
  .page-label {{ position: absolute; bottom: 4px; right: 8px; font-size: 10px; color: #999; }}
  .info-box {{
    position: absolute; left: 6%; top: 3%; right: 6%; height: 27%;
    border: 1px solid #999; font-size: 9px; padding: 4px 6px; color: #444;
    background: rgba(255,255,255,.6); overflow: hidden; white-space: pre-line;
  }}
  .single-page-note {{ font-size: 11px; color: #888; text-align: center; }}
</style>
</head>
<body>
<header>台灣郵局存證信函產生器 {version}</header>
<main>
  <div class="col">
    <h2>寄件人</h2>
    <fieldset><div id="senders"></div>
      <button class="btn btn-add" onclick="addEntry('senders')">+ 新增寄件人</button></fieldset>
    <h2>收件人</h2>
    <fieldset><div id="receivers"></div>
      <button class="btn btn-add" onclick="addEntry('receivers')">+ 新增收件人</button></fieldset>
    <h2>副本收件人</h2>
    <fieldset><div id="ccs"></div>
      <button class="btn btn-add" onclick="addEntry('ccs')">+ 新增副本收件人</button></fieldset>

    <h2>內文</h2>
    <textarea id="article" rows="14" oninput="renderPreview()"
      placeholder="輸入信函內文，換行即分段，超過{chars}字自動換行..."></textarea>

    <div style="margin-top:14px; text-align:right;">
      <button id="export-btn" class="btn btn-primary" onclick="doExport()">匯出成 PDF</button>
    </div>
    <div id="status"></div>
  </div>
  <div class="col">
    <h2>即時預覽</h2>
    <div id="preview"></div>
  </div>
</main>

<script>
const CHARS_PER_LINE = {chars};
const LINES_PER_PAGE = {lines};
const LABELS = {{senders: '寄件人', receivers: '收件人', ccs: '副本收件人'}};
const state = {{senders: [], receivers: [], ccs: []}};

function addEntry(kind) {{
  const idx = state[kind].length;
  state[kind].push({{name: '', addr: ''}});
  const container = document.getElementById(kind);
  const div = document.createElement('div');
  div.className = 'entry-group row';
  div.innerHTML = `
    <div><label>姓名（多人以空白分隔）</label>
      <input type="text" oninput="state['${{kind}}'][${{idx}}].name=this.value; renderPreview()"></div>
    <div><label>地址</label>
      <input type="text" oninput="state['${{kind}}'][${{idx}}].addr=this.value; renderPreview()"></div>
    <button class="btn btn-remove" title="移除" onclick="removeEntry('${{kind}}', ${{idx}}, this)">&times;</button>`;
  container.appendChild(div);
}}

function removeEntry(kind, idx, btn) {{
  state[kind][idx] = null;
  btn.closest('.entry-group').remove();
  renderPreview();
}}

function compactEntries(kind) {{
  return state[kind].filter(e => e && (e.name.trim() || e.addr.trim()));
}}

// mirrors core.py's fill_name_address(): one entry's name may be several
// people sharing one address ("王小明 王大明"), joined back with a space.
function buildInfoText() {{
  const fmt = (label, list) => list.length
    ? list.map(e => `${{label}}：${{e.name}}　地址：${{e.addr}}`).join('\\n')
    : `${{label}}：\\n\\t詳細地址：`;
  return [
    fmt('寄件人', compactEntries('senders')),
    fmt('收件人', compactEntries('receivers')),
    fmt('副本收件人', compactEntries('ccs')),
  ].join('\\n');
}}

// mirrors core.py's _parse_main_article() char/line/page counters
function paginate(text) {{
  const pages = [[]];
  let page = pages[0];
  let line = [];
  page.push(line);
  let charCounter = 1;
  let lineCounter = 1;
  for (const ch of text) {{
    if (ch === '\\n' || charCounter > CHARS_PER_LINE) {{
      line = [];
      page.push(line);
      lineCounter += 1;
      charCounter = 1;
      if (ch === '\\n') continue;
    }}
    if (lineCounter > LINES_PER_PAGE) {{
      page = [];
      pages.push(page);
      line = [];
      page.push(line);
      lineCounter = 1;
      charCounter = 1;
    }}
    line.push(ch);
    charCounter += 1;
  }}
  return pages;
}}

function renderGridPage(lines, pageNo, totalPages, showInfoBox, infoText) {{
  const pageEl = document.createElement('div');
  pageEl.className = 'letter-page';
  if (showInfoBox) {{
    const box = document.createElement('div');
    box.className = 'info-box';
    box.textContent = infoText;
    pageEl.appendChild(box);
  }}
  const grid = document.createElement('div');
  grid.className = 'grid-area';
  grid.style.gridTemplateRows = `repeat(${{LINES_PER_PAGE}}, 1fr)`;
  for (let r = 0; r < LINES_PER_PAGE; r++) {{
    const lineChars = lines[r] || [];
    for (let c = 0; c < CHARS_PER_LINE; c++) {{
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.textContent = lineChars[c] || '';
      grid.appendChild(cell);
    }}
  }}
  pageEl.appendChild(grid);
  const label = document.createElement('div');
  label.className = 'page-label';
  label.textContent = `第 ${{pageNo}} / ${{totalPages}} 頁`;
  pageEl.appendChild(label);
  return pageEl;
}}

function renderPreview() {{
  const text = document.getElementById('article').value;
  const pages = paginate(text);
  const preview = document.getElementById('preview');
  preview.innerHTML = '';
  const infoText = buildInfoText();
  pages.forEach((lines, i) => {{
    preview.appendChild(renderGridPage(lines, i + 1, pages.length,
      i === pages.length - 1 && pages.length > 1, infoText));
  }});
  if (pages.length === 1) {{
    const note = document.createElement('div');
    note.className = 'single-page-note';
    note.textContent = '（單頁信件：姓名地址將直接印在信紙抬頭欄位）';
    preview.appendChild(note);
  }}
}}

function setStatus(text, isError) {{
  const el = document.getElementById('status');
  el.textContent = text;
  el.className = isError ? 'error' : '';
}}

async function doExport() {{
  const btn = document.getElementById('export-btn');
  const text = document.getElementById('article').value;
  if (!text.trim()) {{
    setStatus('請先輸入內文', true);
    return;
  }}
  btn.disabled = true;
  setStatus('產生 PDF 中...');
  try {{
    const resp = await fetch('/export', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{
        senders: compactEntries('senders'),
        receivers: compactEntries('receivers'),
        ccs: compactEntries('ccs'),
        article: text,
      }}),
    }});
    if (!resp.ok) {{
      const err = await resp.text();
      throw new Error(err || ('HTTP ' + resp.status));
    }}
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus('已下載 PDF');
  }} catch (e) {{
    setStatus('匯出失敗：' + e.message, true);
  }} finally {{
    btn.disabled = false;
  }}
}}

addEntry('senders');
addEntry('receivers');
renderPreview();
</script>
</body>
</html>
"""


def _render_index():
    return PAGE_TEMPLATE.format(
        version=VERSION,
        chars=CONTENT_MAX_CHARACTER_PER_LINE,
        lines=CONTENT_MAX_LINE_PER_PAGE,
    ).encode("utf-8")


def _entries_to_core_lists(entries):
    """[{'name': 'a b', 'addr': 'x'}, ...] -> (names, addrs) in core.py's shape."""
    names = [e.get("name", "").split() for e in entries]
    addrs = [e.get("addr", "") for e in entries]
    return names, addrs


class Handler(BaseHTTPRequestHandler):
    server_version = "LALGeneratorWebUI/1.0"

    def log_message(self, format_, *args):
        pass  # keep terminal quiet; this is a local single-user tool

    def do_GET(self):
        if self.path not in ("/", ""):
            self.send_error(404)
            return
        body = _render_index()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/export":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            pdf_bytes = self._generate_pdf(payload)
        except Exception as exc:  # noqa: BLE001 - surfaced to the browser as-is
            message = str(exc).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(message)))
            self.end_headers()
            self.wfile.write(message)
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", 'attachment; filename="output.pdf"')
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def _generate_pdf(self, payload):
        senders, senders_addr = _entries_to_core_lists(payload.get("senders", []))
        receivers, receivers_addr = _entries_to_core_lists(payload.get("receivers", []))
        ccs, cc_addr = _entries_to_core_lists(payload.get("ccs", []))
        article = payload.get("article", "")

        # core.py resolves both its input assets (res/tw_lal.pdf, the font)
        # and its GENERATED_*_PATH scratch files relative to cwd, so cwd
        # must stay the project directory. Only the final merged output
        # goes to a throwaway temp path (same pattern as gui.py's export).
        fd, output_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        try:
            core.generate_text_and_letter(
                senders, senders_addr, receivers, receivers_addr, ccs, cc_addr, article
            )
            core.merge_text_and_letter(output_path)
            core.clean_temp_files()
            with open(output_path, "rb") as f:
                return f.read()
        finally:
            os.remove(output_path)


def run(port=DEFAULT_PORT, open_browser=True):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = "http://127.0.0.1:%d/" % port
    print("台灣郵局存證信函產生器 Web UI 已啟動： %s" % url)
    print("按 Ctrl+C 結束")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
