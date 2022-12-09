import requests
from flask import Flask, render_template
from flask import session, request, redirect, url_for

from frontend import utils

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
        return login_page(utils.get_session_error_msg(session))

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
        session["curr_user"]["password"] = password

        redirect_from = utils.get_session_redirect_from(session)
        if redirect_from:
            return redirect(url_for(redirect_from))
        else:
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

    missing_vars = utils.get_missing_vars(
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
        session["curr_user"]["password"] = password

        redirect_from = utils.get_session_redirect_from(session)
        if redirect_from:
            return redirect(url_for(redirect_from))
        else:
            return redirect(url_for("home_display"))

    else:
        error_msg = response.json()["error_msg"].split(".", 1)[0]
        return register_page(error_msg)


# http://127.0.0.1:8000/home
@app.route("/home")
def home_display():
    if "curr_user" not in session:
        utils.redirect_signin_error(session, "home_display")
        return redirect(url_for("signin_user"))

    print(session["curr_user"])
    return render_template("homepage.html")


# http://127.0.0.1:8000/gallery_display
@app.route("/gallery_display", methods=["GET", "POST"])
def gallery_display():
    if "curr_user" not in session:
        utils.redirect_signin_error(session, "gallery_display")
        return redirect(url_for("signin_user"))

    _filter = request.args.getlist("_filter")
    min_price = request.form.get("min-value")
    max_price = request.form.get("max-value")

    if _filter:
        response = requests.get(
            BASE + "/gallery",
            {
                f"{_filter[0]}_filter": _filter[1],
            },
        )
    elif min_price and max_price:
        response = requests.get(
            BASE + "/gallery",
            {
                "min_value_filter": f"{min_price}-{max_price}",
            },
        )
    else:
        response = requests.get(BASE + "/gallery")

    response = response.json()

    return render_template("gallery.html", value=response)


# http://127.0.0.1:8000/img_display
@app.route("/img_display/")
def img_display():
    if "curr_user" not in session:
        utils.redirect_signin_error(session, "img_display", False)
        return redirect(url_for("signin_user"))

    img_id = request.args.get("img_id")
    response = requests.get(
        BASE + "/artwork/get", json={"data": {"uid": int(img_id)}}
    )

    if response.status_code == 200:
        session["curr_img_min_val"] = response.json()["info"]["min_value"]

    response = response.json()
    return render_template("information.html", value=response)


# http://127.0.0.1:8000/buy_art/
@app.route("/buy_art", methods=["GET", "POST"])
def buy_art():
    if "curr_user" not in session:
        utils.redirect_signin_error(session, "buy_art", False)
        return redirect(url_for("signin_user"))

    img_uid = request.args.get("img_id")
    response = requests.get(
        BASE + "/artwork/get", json={"data": {"uid": int(img_uid)}}
    )
    response = response.json()

    if request.method == "POST":
        buyer_uid = session["curr_user"]["uid"]
        buyer_password = session["curr_user"]["password"]

        min_value = session["curr_img_min_val"]

        card_number = request.form.get("card-number")
        expiration_year, expiration_month = request.form.get(
            "expiration-date").split("-")
        cvv_code = request.form.get("cvv-code")
        shipping_address = request.form.get("shipping-address")

        response = requests.post(
            BASE + "/artwork/buy",
            json={
                "data": {
                    "buyer_uid": buyer_uid,
                    "buyer_password": buyer_password,
                    "artwork_uid": img_uid,
                    "card_number": card_number,
                    "expire_date": f"{expiration_month}{expiration_year[2:]}",
                    "cvv_code": cvv_code,
                    "paid_amount": min_value,
                }
            },
        )

        print(response.json())
        # TODO: give user message when buy success, fix type error for the
        #  request

    return render_template("buy.html", value=response)


def main():
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
