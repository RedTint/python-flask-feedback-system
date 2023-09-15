# Python + Flask Simple Feedback System

Nothing too special. Just a simple Python + Flask feedback system.

## How to Setup
1. cd `./api`
1. Run `python3 -m venv env`
2. Run `source env/bin/activate`
2. Install libraries via `pip3 install -r requirements.txt`
4. Run `python3 app.py`
    * Note: The database would be immediately instantiated if it is not yet setup

## How to Use

1. Navigate to `http://localhost/qr` to generate QR Codes. This QR codes redirect to `http://localhost/feedback?department={department}`.
2. Navigate to `http://localhost/feedback?department={department}` to provide feedback.
3. Navigate to `http://localhost/review-feedback` to view records

## Customization
1. You can change the icons available inside the `./api/static/` folder.
