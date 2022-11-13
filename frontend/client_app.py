import requests
from flask import Flask

app = Flask(__name__)
BASE = "http://127.0.0.1:5000"


@app.route('/img_display')
def img_display():
    response = requests.get(BASE + "/artwork", {"uid": 10})
    return f'''
        <html>
          <body>
            <div>
              <p>{response.json()["info"]}</p>
              <img src="data:image/png;base64,{response.json()["artpic"]}"/>
            </div>
          </body>
        </html>
        '''


@app.route('/gallery_display')
def gallery_display():
    response = requests.get(BASE + "/gallery", {"artwork_num": 5})
    response = response.json()

    html_div_str = str()
    for item in response:
        html_div_str += f'<p>{item["info"]}</p> ' \
                        f'<img src="data:image/png;base64,{item["artpic"]}"/>'

    return f'''
        <html>
          <body>
            <div>
              {html_div_str}
            </div>
          </body>
        </html>
        '''


def main():
    # http://127.0.0.1:8000/img_display
    # http://127.0.0.1:8000/gallery_display
    app.run(debug=True, port=8000)


if __name__ == "__main__":
    main()
