from flask import Flask, request, Response
import requests, os

app = Flask(__name__)
PROXY_KEY = os.environ.get("PROXY_KEY", "PaqLlegue_EI_2026_xK9mZ")
EI_BASE   = "https://app.enviosinternacionales.com/api/v1"

@app.route("/", defaults={"path": ""}, methods=["GET","POST","PUT","PATCH","DELETE"])
@app.route("/<path:path>", methods=["GET","POST","PUT","PATCH","DELETE"])
def proxy(path):
    if request.headers.get("X-Proxy-Key") != PROXY_KEY:
        return {"error": "Acceso denegado"}, 403
    endpoint = request.args.get("endpoint", "")
    if not endpoint:
        return {"error": "Falta ?endpoint="}, 400
    url  = EI_BASE + endpoint
    hdrs = {k: v for k, v in request.headers if k.lower() in ("content-type","authorization","accept")}
    hdrs["User-Agent"] = "Mozilla/5.0"
    resp = requests.request(request.method, url, headers=hdrs, data=request.get_data(), timeout=45)
    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get("content-type","application/json"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
