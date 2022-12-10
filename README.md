# Artket: Ebay for artwork

## Setup

The project was developed and tested with `python3.9.5`. However, any version
of `python` after `3.8` (need f-string) should be sufficient. An exception to
this is when the server and client code is run on ARM architecture family (like
M1 chip), then require `python` version larger or equal to `3.9.1`. `python3.9`
is required due to `3.9.1` is the first version of `python` that support ARM
architecture.

We suggest the developer running this project with a virtual environment
using `python>=3.9.1`. The project also require the modules listed bellow to be
installed in the environment, this list of module can also be found
at `root/requirements.txt`. Required modules are:

* `aniso8601==9.0.1`
* `certifi==2022.12.7`
* `charset-normalizer==2.1.1`
* `click==8.1.3`
* `Flask==2.2.2`
* `Flask-RESTful==0.3.9`
* `Flask-SQLAlchemy==3.0.2`
* `idna==3.4`
* `importlib-metadata==5.1.0`
* `itsdangerous==2.1.2`
* `Jinja2==3.1.2`
* `MarkupSafe==2.1.1`
* `phonenumbers==8.13.2`
* `Pillow==9.3.0`
* `pytz==2022.6`
* `requests==2.28.1`
* `six==1.16.0`
* `SQLAlchemy==1.4.44`
* `urllib3==1.26.13`
* `Werkzeug==2.2.2`
* `zipp==3.11.0`

## Build & Run

One all the requirements are satisfy and the setup done correctly as mention
from the Setup section, the developer can build and run the project. Keep in
mind Artket project is separate into 2 main components -- the server program
(source code is in the backend directory) and the client program (source code
is in the frontend directory).

The server program can be run independently, while the client program require
the server program to be in running/listening at `http://127.0.0.1:5000` (which
is defined with variable `BASE` in `root/frontend/client_app.py`). More on
implementation detail in the Code Structure section.

To run the server and client program, the developer must change their current
working directory to the root directory for this project, namely
`microgoo-final-project`. One in the directory, the developer can run the
server program and the client program with the environment setup from the
Setup section as follows:

* The server program: `python backend/server_app.py`
* The client program: `python frontend/client_app.py`

One done correctly, the developer can try to use the app like a user by go
to `http://127.0.0.1:8000`.

### Notes for Tester

* To test the register functionality, please use the following invitation
  code: `dev_default_invite_code_{i}` where the value of `{i}` is 0 to 10. Keep
  in mind that each invitation code will be removed when a new accounts created
  with it.
* To test the purchase functionality, please use a valid credit card to try to
  purchase it. The program use a luhn checksum to check for credit card number,
  so the card must be valid but can be expired. For testing purpose, we suggest
  using the following card number `3716820019271998` with the CVV code is any 3
  digits number.

> Do NOT read this the remaining of this subsection if the tester want to
> experience the app like a targeted user

* The Artket website store login info based on browser session. When the user
  go to `http://127.0.0.1:8000`, they can either be redirected to the login
  page if they have not logged in yet or redirect to the homepage otherwise.
  Close a browser tab alone will not remove the session, thus allow the user to
  revisit the site without the need of login again. On the other hand, if close
  all active window of the browser or close the entire browser application will
  remove the browser session, thus require the user to login again.
* The Artket website, use a sqlitte3 database to store information about the
  artwork, registered user, and available invitation code. Therefore, new user
  accounts and purchasing artwork will update the database and thus allow to
  keep these information across Artket application session.

## Code Structure

The project is divided into 2 main part, the server side code (stored in
backend directory) and the client side code (stored in frontend directory)

### Server Side

The server of the Artwork is design to run independently of the client side.

The server responsible for handling all query to the database from the client
side. The server perform some query validation to make sure all required
information are available and have the correct data type. The server then
perform data format before commit them to the database.

For each query, the server will respond with a dictionary and a status code. If
the status code is not 200, then the response is a dict with the following form
`{"error_msg: {(str) some error message}}`. If the status code is 200, that
mean the query performed successfully and thus the response is a dict that
contain all the information that the client request in that query.

The server code start from `root/backend/server_app.py`, where it config the
server flask app, the database, generate some dummy data for testing, and set
up the endpoint for each server functionality. Note that each of the server
functionality have their own `.py` file. Additionally, all the server data like
the sqlitte3 database, history.json, and the picture of the artwork (in base64
text) are stored in the `root/backend/instance` directory.

### Client Side

The client of Artwork required the server in running/listening on
`http://127.0.0.1:5000` for it to work.

The client side handling all query from the browser, try transform those
received data to correct data type, and create a corresponding query to the
server side.

One the query go through, the server will respond back with some data, the
client side will then check the status code of the response and parse the
response accordingly.

The client side endpoint and logic are in `root/frontend/client_app.py`. These
functions will pass data to jinja2 templates store in `root/frontend/templates`
directory. The Artket website using some static image and icon, these are
stored in `root/frontend/static` directory.