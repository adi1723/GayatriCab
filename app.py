from flask import Flask, request, render_template, redirect, jsonify,url_for
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, redirect, flash
import smtplib
from email.message import EmailMessage
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
HEADERS = {
    'User-Agent': 'GayatriCab/1.0 (admin@gayatricab.com)'  # Required by Nominatim
}
EMAIL_SENDER = os.getenv('MAIL_USERNAME') or 'your-email@gmail.com'
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or 'your-email-password'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL') or EMAIL_SENDER

@app.route('/')
def home():
    status = request.args.get('status')
    return render_template('index.html', status=status)

@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    pickup = request.form.get('pickupaddress')
    drop = request.form.get('dropaddress')
    date = request.form.get('date')
    time = request.form.get('time')
    passengers = request.form.get('passengers')
    cab_type = request.form.get('cab_type')
    package = request.form.get('package')  # New field from modal form

    subject = 'New Cab Booking Confirmation'
    body = f"""
Subject: 🚖 New Booking Received - Gayatri Tours and Travels

Hello Admin,

A new booking has been received via the Gayatri Tours and Travels website. Below are the customer details:

Name: {name}
Mobile: {mobile}
Pickup Address: {pickup}
Drop Address: {drop}
Date: {date}
Time: {time}
Number of Passengers: {passengers}
Cab Type: {cab_type}
Package: {package}

Please review the booking and contact the customer at your earliest convenience to confirm the ride.

Regards,
Gayatri Tours and Travels System
"""

    try:
        send_email(subject, body, ADMIN_EMAIL)
        return redirect('/?status=success')
    except Exception as e:
        print(f"Failed to send email: {e}")
        return redirect('/?status=fail')

def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/packages')
def packages():
    return render_template('packages.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/packages2')
def packages2():
    return render_template('packages2.html')

@app.route('/terms')
def terms_and_conditions():
    return render_template('terms&conditions.html')

@app.route('/cancel')
def cancel():
    print("User cancelled booking")
    return redirect(url_for('home'))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy&policy.html')

@app.route('/refund-policy')
def refund_policy():
    return render_template('RefundPolicy.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/ToursPackages')
def ToursPackages():
    return render_template('ToursPackages.html')

@app.route('/Gallery')
def Gallery():
    return render_template('Gallery.html')

@app.route('/Details_Mahabaleshwar')
def Details_Mahabaleshwar():
    return render_template('Details_Mahabaleshwar.html')

# Location search for autocomplete
@app.route('/search_location')
def search_location():
    q = request.args.get('q', '')
    if not q:
        return jsonify([])
    params = {'q': q, 'format': 'json', 'limit': 5}
    try:
        resp = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers=HEADERS)
        return jsonify(resp.json())
    except Exception as e:
        print("Error in /search_location:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)