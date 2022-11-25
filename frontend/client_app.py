import requests
from flask import Flask, render_template, request, redirect, url_for

from frontend.utils import convert_artpic_to_base64str

app = Flask(__name__)
BASE = "http://127.0.0.1:5000"


# http://127.0.0.1:8000/img_display
@app.route("/home")
def home_display():
    return render_template("homepage.html")

@app.route("/img_display")
def img_display():
    response = requests.get(BASE + "/artwork/get", json={"data": {"uid": 1}})

    print(response)
    return f"""
        <html>
          <body>
            <div>
              <p>{response.json()["info"]}</p>
              <img src="data:image/png;base64,{response.json()["artpic"]}"/>
            </div>
          </body>
        </html>
        """


# http://127.0.0.1:8000/sell_art
@app.route("/sell_art")
def sell_art():
    response = requests.put(
        BASE + "/artwork/sell",
        json={
            "data": {
                "artpic": convert_artpic_to_base64str(
                    "/Users/dukedao/Downloads/git_style.png"
                ),
                "name": "GitHub Guild Line",
                "genre": "post-impressionism",
                "medium": "oil painting",
                "surface": "canvas",
                "width": 921,
                "height": 737,
                "artist": "Vincent Van Gogh",
                "created_date": "1889",
                "created_location": "France",
                "min_value": 100000000,
                "seller_uid": 1,
                "seller_password": "dev_pw_test",
            }
        },
    )

    print(response)
    print(response.json())

    return f"{response.json()}"


# http://127.0.0.1:8000/buy_art
@app.route("/buy_art")
def buy_art():
    response = requests.post(
        BASE + "/artwork/buy",
        json={
            "data": {
                "buyer_uid": 2,
                "buyer_password": "dev_pw_test",
                "artwork_uid": 1,
                "card_number": 378282246310005,
                "expire_date": "11/25",
                "cvv_code": 498,
                "paid_amount": 100000000,
            }
        },
    )

    print(response)
    print(response.json())

    return f"{response.json()}"


# http://127.0.0.1:8000/gallery_display
@app.route("/gallery_display")
def gallery_display():
    response = requests.get(BASE + "/gallery")
    # response = requests.get(BASE + "/gallery", {
    #     # "artwork_num": 5,
    #     # "artist_filter": [
    #     #     "Vincent Van Gogh",
    #     #     "Gustav Klimt",
    #     # ],
    #     # "medium_filter": [
    #     #     "gold leaf",
    #     #     "graphite",
    #     # ],
    #     # "created_date_filter": "1485-1565",
    #     # "min_value_filter": "240000-25000000",
    #     # "width_filter": "390-920",
    #     "height_filter": "445-737",
    #     "order_by": "artist",
    #     "order_decrease": "True",
    # })
    # response = requests.get(BASE + "/gallery", {
    #     "artwork_num": 10,
    #     "artist_filter": "Gustav Klimt",
    #     "medium_filter": "gold leaf",
    #     "created_date_filter": "1908-1908",
    #     "min_value_filter": "240000-240000",
    #     "width_filter": "1800-1800",
    #     "height_filter": "1800-1800",
    # })

    print(response)
    response = response.json()

    html_div_str = str()
    for item in response:
        html_div_str += (
            f'<p>{item["info"]}</p> '
            f'<img src="data:image/png;base64,{item["artpic"]}"/>'
        )

    return f"""
        <html>
          <body>
            <div>
              {html_div_str}
            </div>
          </body>
        </html>
        """


# http://127.0.0.1:8000/sign_in
@app.route("/sign_in", methods=['GET', 'POST'])
def signin_user():
    if request.method == "POST":
        email_or_phone = request.form.get('email-or-phone')
        password = request.form.get('password')

########## Issue: Redireects user to homepage regardless of whether credentials are correct or not ###########

        return redirect(url_for('home_display'))


    return render_template("login.html")

    response = requests.post(
        BASE + "/user/get",
        json={
            "data": {
                # "email": "dev02@artket.com",
                # "mobile": "+13308575092",
                "password": "dev_pw_test",
            }
        },
    )

    print(response)
    return f"""
        <html>
          <body>
            <div>
              <p>{response.json()}</p>
            </div>
          </body>
        </html>
        """


# http://127.0.0.1:8000/sign_up
@app.route("/sign_up", methods=['GET', 'POST'])
def signup_user():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        invitation_code = request.form.get('invitation-code')
        phone_number = request.form.get('phone-number')

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

        return render_template("login.html")


    return render_template("register.html")

    print(response)
    return f"""
        <html>
          <body>
            <div>
              <p>{response.json()}</p>
            </div>
          </body>
        </html>
        """


def main():
    # http://127.0.0.1:8000/img_display
    # http://127.0.0.1:8000/sell_art
    # http://127.0.0.1:8000/buy_art
    # http://127.0.0.1:8000/gallery_display
    # http://127.0.0.1:8000/sign_in
    # http://127.0.0.1:8000/sign_up
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
