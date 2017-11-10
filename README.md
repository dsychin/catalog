# Item Catalog Project
## Description
This project is one of Udacity's Full Stack Web Developer Nanodegree projects.
This is a web application which shows items in an item catalog, it also allows 
users to register and login using email or OAuth 2.0 and make changes to an item
catalog.

## Prerequisites
1. [Python 3](https://www.python.org/)
2. [Python Package Index (pip)](https://pypi.python.org/pypi/pip)
2. A modern web browser

## Installation
1. Clone/Download this repository.
2. With the root folder as the working directory, run `pip install -r requirements.txt` in your terminal.
3. Go to [Google Developer Console](https://console.developers.google.com/) and create a client ID for a web application.
4. Under Authorized JavaScript origins, add `http://localhost:8000` if running on your local machine, or replace it with your web address if running on a server.
5. Under Authorized redirect URIs, add `http://localhost:8000/login` and `http://localhost:8000/gconnect`. Replace localhost:8000 with your own web address or port.
6. Download the client secret as a json file, put it in the root folder and rename it to `client_secrets.json`.
7. In your terminal run `python database_setup.py` to set up the sqlite file.

## Running the web server
1. In your terminal run `python application.py`