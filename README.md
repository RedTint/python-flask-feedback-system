# Python3 + React Simple Feedback System

Nothing too special. Just a simple Python Flask API + React feedback system.

## How to Setup

### Python Flask API
1. cd `./api`
1. Run `python3 -m venv env`
2. Run `source env/bin/activate`
2. Install libraries via `pip3 install -r requirements.txt`
4. Run `python3 app.py`
    * Note: The database would be immediately instantiated if it is not yet setup

## To Do List
- [ ] Set up Python API
  - [ ] Return list of departments `GET /departments`
  - [ ] Store `POST /feedback`
  - [ ] Return QR Code based on inputted route: `GET /qr={text}`
- [ ] Set up React Frontend
- [ ] Create QR Code Provider
- [ ] Create Feedback Form
