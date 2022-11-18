from pprint import pprint

import requests
from flask import Flask

app = Flask(__name__)
BASE = "http://127.0.0.1:5000"


@app.route("/img_display")
def img_display():
    response = requests.get(BASE + "/artwork", {"uid": 10})
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


@app.route("/sign_in")
@app.route("/")
def signin_user():
    response = requests.post(
        BASE + "/get_user",
        json={
            "data": {
                # "uid": 1,
                # "email": "dev01@artket.com",
                "mobile": "+13308575093",
                "password": "dev_pw_test",
            }
        },
    )

    pprint(response.json())
    return f"""
        <html>
          <body>
            <div>
              <p>{response.json()}</p>
            </div>
          </body>
        </html>
        """


@app.route("/sign_up")
def signup_user():
    response = requests.put(
        BASE + "/create_user",
        json={
            "data": {
                "email": "dev03@artket.com",
                "mobile": "+133---098(85)09-3",
                "username": "dev03",
                "password": "dev_pw_test",
                "invitation_code": "w~G.^zz!YO0>/KwBUBIX",
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
    # http://127.0.0.1:8000/gallery_display
    # http://127.0.0.1:8000/sign_in
    # http://127.0.0.1:8000/sign_up
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
