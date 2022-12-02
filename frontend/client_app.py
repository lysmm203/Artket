import requests
from flask import Flask, render_template, request, redirect, url_for, flash, g, session


from frontend.utils import convert_artpic_to_base64str

app = Flask(__name__)
app.secret_key = "client_app"
BASE = "http://127.0.0.1:5000"


# http://127.0.0.1:8000/img_display
@app.route("/home")
def home_display():
    return render_template("homepage.html")

@app.route("/img_display/")
def img_display():
    img_id = request.args.get('img_id')
    response = requests.get(BASE + "/artwork/get", json={"data": {"uid": int(img_id)}})
    response = response.json()

    return render_template("information.html", value=response)

# http://127.0.0.1:8000/buy_art
@app.route("/buy_art")
def buy_art():
    img_id = request.args.get('img_id')
    response = requests.get(BASE + "/artwork/get", json={"data": {"uid": int(img_id)}})
    response = response.json()
    # response = requests.post(
    #     BASE + "/artwork/buy",
    #     json={
    #         "data": {
    #             "buyer_uid": 2,
    #             "buyer_password": "dev_pw_test",
    #             "artwork_uid": 3,
    #             "card_number": 378282246310005,
    #             "expire_date": "11/25",
    #             "cvv_code": 498,
    #             "paid_amount": 100000000,
    #         }
    #     },
    # )

    return render_template("buy.html", value=response)


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

    return f"{response.json()}"





# http://127.0.0.1:8000/gallery_display
@app.route("/gallery_display")
def gallery_display():
    response = requests.get(BASE + "/gallery")

    # response = requests.get(BASE + "/gallery", {
    #     "artwork_num": 5,
    #     "artist_filter": [
    #         "Vincent Van Gogh",
    #     ],
    #     "medium_filter": [
    #         "gold leaf",
    #         "graphite",
    #     ],
    #     "created_date_filter": "1485-1565",
    #     "min_value_filter": "240000-25000000",
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
    abc = 1


    return render_template("gallery.html", value=response)

# http://127.0.0.1:8000/sign_in
@app.route("/", methods=['GET', 'POST'])
def signin_user():
    if request.method == "POST":
        email_or_phone = request.form.get('email-or-phone')
        password = request.form.get('password')

        response = requests.post(
            BASE + "/user/get",
            json={
                "data": {
                    # If @ is in string, it's email. Otherwise, it's phone
                    "email": email_or_phone,
                    "mobile": email_or_phone,
                    "password": password,
                }
            },
        )

        if request.form['submit-button'] == 'register':
            return redirect(url_for('signup_user'))
        elif request.form['submit-button'] == 'login':
            if response.status_code == 200:
                return redirect(url_for('home_display'))
            else:
                error_message = response.json()['error_msg']
                flash(error_message, 'error')


    return render_template("login.html")

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

        print(
            f"Name: {name} Email: {email} Password: {password} Invitation code: {invitation_code} Phone Number: {phone_number}")

        return redirect(url_for('signin_user'))

    return render_template("register.html")

# http://127.0.0.1:8000/user_saved
@app.route("/user_saved")
def get_user_saved():
    response = requests.get(
        BASE + "/user/saved",
        json={
            "data": {
                "user_uid": 2,
                "user_password": "dev_pw_test",
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


# http://127.0.0.1:8000/user_saved_add
@app.route("/user_saved_add")
def add_to_user_saved():
    response = requests.put(
        BASE + "/user/saved",
        json={
            "data": {
                "user_uid": 2,
                "user_password": "dev_pw_test",
                "artwork_uid": 1,
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


# http://127.0.0.1:8000/user_saved_remove
@app.route("/user_saved_remove")
def remove_from_user_saved():
    response = requests.delete(
        BASE + "/user/saved",
        json={
            "data": {
                "user_uid": 2,
                "user_password": "dev_pw_test",
                "artwork_uid": 1,
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
