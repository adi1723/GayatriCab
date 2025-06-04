from flask import Flask, request, render_template, redirect
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL_SENDER = os.getenv('MAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

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


    subject = 'New Cab Booking Confirmation'
    body = f"""
Subject: 🚖 New Booking Received Gayatri Tours and Travels

Message:

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

Please review the booking and contact the customer at your earliest convenience to confirm the ride.

Regards,
Gayatri Tours and Travels System
"""

    try:
        send_email(subject, body, EMAIL_SENDER)
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

if __name__ == '__main__':
    app.run(debug=True)
