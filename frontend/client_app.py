import requests
from flask import Flask, render_template
from flask import session, request, redirect, url_for

from frontend.utils import get_missing_vars

app = Flask(__name__)
app.secret_key = "client_app"
BASE = "http://127.0.0.1:5000"


@app.route("/")
def base_url():
    # for dev only
    if "curr_user" in session:
        del session["curr_user"]

    if "curr_user" not in session:
        return redirect(url_for("signin_user"))

    return redirect(url_for("home_display"))


# http://127.0.0.1:8000/sign_in
@app.route("/sign_in", methods=["GET", "POST"])
def signin_user():
    def login_page(_error_msg=None):
        return render_template("login.html", error_msg=_error_msg)

    if request.method != "POST":
        return login_page()

    # code from this point req request.method == "POST"
    if request.form["submit-button"] == "register":
        return redirect(url_for("signup_user"))

    email_or_phone = request.form.get("email-or-phone")
    password = request.form.get("password")

    response = requests.post(
        BASE + "/user/get",
        json={
            "data": {
                "email_or_mobile": email_or_phone,
                "password": password,
            }
        },
    )

    if response.status_code == 200:
        session["curr_user"] = response.json()
        return redirect(url_for("home_display"))

    else:
        error_msg = response.json()["error_msg"].split(".", 1)[0]
        return login_page(error_msg)


# http://127.0.0.1:8000/sign_up
@app.route("/sign_up", methods=["GET", "POST"])
def signup_user():
    def register_page(_error_msg=None):
        return render_template("register.html", error_msg=_error_msg)

    if request.method != "POST":
        return register_page()

    # code from this point req request.method == "POST"
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    invitation_code = request.form.get("invitation-code")
    phone_number = request.form.get("phone-number")

    missing_vars = get_missing_vars(
        ["name", "email", "phone number", "password", "invitation code"],
        [name, email, phone_number, password, invitation_code],
    )
    if missing_vars:
        error_msg = f"{', '.join(missing_vars)} field(s) are missing"
        return register_page(error_msg)
    if password != confirm_password:
        return register_page("password and confirm password does not match")

    response = requests.put(
        BASE + "/user/create",
        json={
            "data": {
                "email": email,
                "mobile": phone_number,
                "username": name,
                "password": password,
                "invitation_code": invitation_code,
            }
        },
    )

    if response.status_code == 200:
        session["curr_user"] = response.json()
        return redirect(url_for("home_display"))

    else:
        error_msg = response.json()["error_msg"].split(".", 1)[0]
        return register_page(error_msg)


# http://127.0.0.1:8000/img_display
@app.route("/home")
def home_display():
    if "curr_user" not in session:
        return redirect(url_for("signin_user"))

    print(session["curr_user"])
    return render_template("homepage.html")


# http://127.0.0.1:8000/gallery_display
@app.route("/gallery_display")
def gallery_display():
    if "curr_user" not in session:
        return redirect(url_for("signin_user"))

    response = requests.get(BASE + "/gallery")
    response = response.json()

    return render_template("gallery.html", value=response)


def main():
    app.run(port=8000)


if __name__ == "__main__":
    main()
