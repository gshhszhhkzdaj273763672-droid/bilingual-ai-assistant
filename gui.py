import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import assistant

with open("/data/data/com.termux/files/home/my_ai_app/app_config.json", "r", encoding="utf-8") as f:
    CFG = json.load(f)

HTML_PAGE = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{CFG['app_name']}</title>
<style>
  body {{ font-family: sans-serif; background: #121212; color: #f1f1f1; margin: 0; padding: 16px; }}
  .box {{ max-width: 600px; margin: auto; background: #1e1e1e; padding: 16px; border-radius: 12px; }}
  h2 {{ margin-top: 0; color: #4fc3f7; }}
  #chat {{ min-height: 220px; max-height: 420px; overflow-y: auto; background: #141414; padding: 12px; border-radius: 8px; margin-bottom: 12px; }}
  .msg {{ margin: 8px 0; padding: 8px 12px; border-radius: 8px; white-space: pre-wrap; }}
  .user {{ background: #263238; }}
  .ai {{ background: #1b5e20; }}
  form {{ display: flex; gap: 8px; }}
  input {{ flex: 1; padding: 10px; border-radius: 8px; border: 1px solid #444; background: #2c2c2c; color: #fff; font-size: 16px; }}
  button {{ padding: 10px 16px; border: none; border-radius: 8px; background: #0288d1; color: #fff; font-size: 16px; }}
</style>
</head>
<body>
<div class="box">
  <h2>{CFG['app_name']} (v{CFG['version']})</h2>
  <div id="chat"></div>
  <form onsubmit="sendMsg(event)">
    <input id="inp" type="text" placeholder="বাংলা বা English-এ লিখুন..." required>
    <button type="submit">পাঠান</button>
  </form>
</div>
<script>
async function sendMsg(e) {{
  e.preventDefault();
  const inp = document.getElementById("inp");
  const chat = document.getElementById("chat");
  const text = inp.value.trim();
  if (!text) return;
  chat.innerHTML += `<div class="msg user"><b>আপনি:</b> ${{text}}</div>`;
  inp.value = "";
  chat.scrollTop = chat.scrollHeight;
  const res = await fetch("/ask", {{
    method: "POST",
    headers: {{"Content-Type": "application/x-www-form-urlencoded"}},
    body: "msg=" + encodeURIComponent(text)
  }});
  const data = await res.json();
  chat.innerHTML += `<div class="msg ai"><b>AI:</b> ${{data.reply}}</div>`;
  chat.scrollTop = chat.scrollHeight;
}}
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/ask":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            msg = parse_qs(body).get("msg", [""])[0].strip()
            bn = any("\u0980" <= c <= "\u09ff" for c in msg)
            reply = assistant.ask_ai(msg, bn) if msg else ""
            payload = json.dumps({"reply": reply}, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(payload)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print(f"Starting {CFG['app_name']} GUI on http://127.0.0.1:8080")
    HTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
