from flask import Flask
from flask import render_template
from flask import request
import httpx
import igpp
import secrets_session

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("response.html", PICTURE="static/instagram.png")


@app.route("/search", methods=["POST"])
def send_image():
    user = request.form["search"]  # comes from <input name="search" />
    error = user
    print(f"[>] Recieved: {user}")
    picture = fetch(user)
    if picture == "bruh.jpg":
        error = f"user not exist: \"{user}\""
    return render_template("image.html", PICTURE="static/" + picture, REASON=error)


def fetch(user: str) -> str:
    if len(user) == 0:
        print(f"[-] Blank search")
        return "bruh.jpg"
    with httpx.Client(headers=secrets_session.headers, cookies=secrets_session.cookies) as client:
        if igpp.download(username=user, client=client):
            print(f"[+] Found: {user}")
            return f"{user}.jpg"
        print(f"[-] Unavailable: {user}")
        return "bruh.jpg"


# Start the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
