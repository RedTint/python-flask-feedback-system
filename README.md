# Python + Flask Simple Feedback System

Nothing too special. Just a simple Python + Flask feedback system.

## How to Setup (Mac / Linux)
1. cd `./api`
1. Run `python3 -m venv env`
2. Run `source env/bin/activate`
2. Install libraries via `pip3 install -r requirements.txt`
4. Run `python3 app.py`
    * Note: The database would be immediately instantiated if it is not yet setup

## How to Use

1. Navigate to `http://localhost/qr` to generate QR Codes. This QR codes redirect to `http://localhost/feedback?department={department}`. You can also download the QR Code, print and display. All up to you.
2. Use the QR Code or navigate to `http://localhost/feedback?department={department}` to provide feedback.
3. Navigate to `http://localhost/review-feedback` to view records

## Database Access
If you want to access the database and load it into another application, you can find it in the `./api/instance/` folder with file name `feedback.db`.

## Customization
1. You can change the icons available inside the `./api/static/` folder.
