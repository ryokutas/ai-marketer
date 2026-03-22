#!/usr/bin/env python3
"""
競合インテリジェンス バトルカード Web アプリ
Python 標準ライブラリのみで動作するシンプルな Web サーバー

起動方法:
    python app.py

ブラウザで http://localhost:8080 を開く

本番デプロイ (Render/Railway):
    PORT 環境変数で自動的にポートを変更します
"""

import json
import sys
import os
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / "scripts"))


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """リクエストログを簡潔に表示"""
        status = args[1]
        path = self.path
        if not path.startswith("/api"):
            return  # 静的ファイルのログは省略
        color = "\033[32m" if str(status).startswith("2") else "\033[31m"
        print(f"  {color}{status}\033[0m  {path}")

    # ── GET ──────────────────────────────────────────────────────────
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._serve_file(BASE / "static" / "index.html", "text/html; charset=utf-8")
        else:
            self._send_error(404, "Not Found")

    # ── POST ─────────────────────────────────────────────────────────
    def do_POST(self):
        if self.path == "/api/generate":
            self._handle_generate()
        else:
            self._send_error(404, "Not Found")

    def _handle_generate(self):
        """JSON を受け取って PPTX を返す"""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            intel_data = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            self._send_json_error(400, f"Invalid JSON: {e}")
            return

        # バリデーション
        if not intel_data.get("competitors"):
            self._send_json_error(400, "競合が1社以上必要です")
            return

        temp_in = temp_out = None
        try:
            # intel_data を一時JSONファイルに書き込む
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, encoding="utf-8"
            ) as f:
                json.dump(intel_data, f, ensure_ascii=False)
                temp_in = f.name

            temp_out = temp_in.replace(".json", ".pptx")

            # PPTX 生成
            from generate_battlecard import generate_battlecard
            generate_battlecard(input_path=temp_in, output_path=temp_out)

            pptx_bytes = Path(temp_out).read_bytes()
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"battlecard_{date_str}.pptx"

            comp_count = len(intel_data.get("competitors", []))
            company = intel_data.get("my_company", {}).get("name", "?")
            print(f"  ✅ 生成完了: {company} / {comp_count}社 → {filename}")

            # レスポンス送信
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
            self.send_header(
                "Content-Disposition", f'attachment; filename="{filename}"'
            )
            self.send_header("Content-Length", str(len(pptx_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(pptx_bytes)

        except Exception as e:
            import traceback
            print(f"  ❌ エラー: {e}")
            traceback.print_exc()
            self._send_json_error(500, str(e))
        finally:
            for p in [temp_in, temp_out]:
                if p and os.path.exists(p):
                    try:
                        os.unlink(p)
                    except Exception:
                        pass

    # ── ヘルパー ──────────────────────────────────────────────────────
    def _serve_file(self, path: Path, content_type: str):
        if not path.exists():
            self._send_error(404, f"File not found: {path.name}")
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_error(self, code: int, msg: str):
        body = msg.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json_error(self, code: int, msg: str):
        body = json.dumps({"error": msg}, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)

    print("\n\033[1;34m🔍 競合インテリジェンス バトルカード\033[0m")
    print("━" * 44)
    print(f"  ブラウザで開く  →  \033[1mhttp://localhost:{port}\033[0m")
    print("  停止: Ctrl+C")
    print("━" * 44 + "\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n停止しました。")
        server.shutdown()
