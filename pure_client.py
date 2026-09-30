import urllib.request
import json

BASE_URL = "http://127.0.0.1:8080"

def send_request(url, method="GET", body=None):
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json"} if body else {}
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            raw_data = response.read().decode("utf-8")
            response_data = json.loads(raw_data) if raw_data else {}
            print(f"[{method}] Status: {status_code} | Yanıt: {response_data}")
    except urllib.error.HTTPError as e:
        raw_error = e.read().decode("utf-8")
        error_data = json.loads(raw_error) if raw_error else {}
    print(f"[{method}] Status: {e.code} | Hata: {error_data}")

print("=== SAF PYTHON REST CLIENT TESTİ ===")

# 1. POST
print("\n1. POST /users")
send_request(f"{BASE_URL}/users", method="POST", body={"name": "Ernest Muçi", "email": "muci@bjk.com"})

# 2. GET (Tümü)
print("\n2. GET /users")
send_request(f"{BASE_URL}/users", method="GET")

# 3. PUT
print("\n3. PUT /users/3")
send_request(f"{BASE_URL}/users/3", method="PUT", body={"name": "Ernest Muçi (10 Numara)", "email": "muci10@bjk.com"})

# 4. DELETE
print("\n4. DELETE /users/2")
send_request(f"{BASE_URL}/users/2", method="DELETE")

# 5. GET (Son Durum)
print("\n5. GET /users")
send_request(f"{BASE_URL}/users", method="GET")