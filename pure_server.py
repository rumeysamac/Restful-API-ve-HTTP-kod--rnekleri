from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

db_users = [
    {"id": 1, "name": "Süleyman Seba", "email": "seba@bjk.com"},
    {"id": 2, "name": "Semih kılıçsoy", "email": "kılıcsoy@bjk.com"}
]
id_counter = 3

class FullCRUDRESTHandler(BaseHTTPRequestHandler):
    
    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _get_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode("utf-8"))
        return {}

    def _parse_user_id(self):
        match = re.match(r"^/users/(\d+)$", self.path)
        if match:
            return int(match.group(1))
        return None

    def do_GET(self):
        user_id = self._parse_user_id()
        if user_id is not None:
            user = next((u for u in db_users if u["id"] == user_id), None)
            if user:
                self._send_json_response(200, {"data": user})
            else:
                self._send_json_response(404, {"error": "Kullanıcı bulunamadı"})
        elif self.path == "/users":
            self._send_json_response(200, {"total": len(db_users), "data": db_users})
        else:
            self._send_json_response(404, {"error": "Endpoint bulunamadı"})

    def do_POST(self):
        global id_counter
        if self.path == "/users":
            data = self._get_request_body()
            new_user = {
                "id": id_counter,
                "name": data.get("name", ""),
                "email": data.get("email", "")
            }
            id_counter += 1
            db_users.append(new_user)
            self._send_json_response(201, {"message": "Kullanıcı eklendi", "data": new_user})
        else:
            self._send_json_response(404, {"error": "Endpoint bulunamadı"})

    def do_PUT(self):
        user_id = self._parse_user_id()
        if user_id is not None:
            data = self._get_request_body()
            user = next((u for u in db_users if u["id"] == user_id), None)
            if user:
                user["name"] = data.get("name", user["name"])
                user["email"] = data.get("email", user["email"])
                self._send_json_response(200, {"message": "Kullanıcı güncellendi", "data": user})
            else:
                self._send_json_response(404, {"error": "Kullanıcı bulunamadı"})
        else:
            self._send_json_response(400, {"error": "Geçersiz URL formatı"})

    def do_DELETE(self):
        user_id = self._parse_user_id()
        if user_id is not None:
            global db_users
            initial_count = len(db_users)
            db_users = [u for u in db_users if u["id"] != user_id]
            if len(db_users) < initial_count:
                self._send_json_response(200, {"message": f"ID: {user_id} olan kullanıcı silindi"})
            else:
                self._send_json_response(404, {"error": "Kullanıcı bulunamadı"})
        else:
            self._send_json_response(400, {"error": "Geçersiz URL formatı"})

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, FullCRUDRESTHandler)
    print("Saf Python REST Sunucusu http://127.0.0.1:8080 üzerinde çalışıyor...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()