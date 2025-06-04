from flask import Flask, request, render_template, redirect, jsonify
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
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


# Get distance between two places
@app.route('/get_distance')
def get_distance():
    pickup = request.args.get('pickup')
    dest = request.args.get('destination')
    if not pickup or not dest:
        return jsonify({'error': 'Missing pickup or destination'}), 400

    try:
        # Get coordinates for pickup
        p_resp = requests.get('https://nominatim.openstreetmap.org/search', 
                              params={'q': pickup, 'format': 'json', 'limit': 1}, headers=HEADERS)
        p_data = p_resp.json()
        if not p_data:
            return jsonify({'error': 'Pickup location not found'}), 404
        p_lat, p_lon = p_data[0]['lat'], p_data[0]['lon']

        # Get coordinates for destination
        d_resp = requests.get('https://nominatim.openstreetmap.org/search', 
                              params={'q': dest, 'format': 'json', 'limit': 1}, headers=HEADERS)
        d_data = d_resp.json()
        if not d_data:
            return jsonify({'error': 'Destination location not found'}), 404
        d_lat, d_lon = d_data[0]['lat'], d_data[0]['lon']

        # Use OSRM API to get driving distance (in meters)
        osrm_url = f"http://router.project-osrm.org/route/v1/driving/{p_lon},{p_lat};{d_lon},{d_lat}"
        osrm_params = {'overview': 'false'}
        osrm_resp = requests.get(osrm_url, params=osrm_params)
        osrm_data = osrm_resp.json()

        if osrm_data.get('code') != 'Ok' or not osrm_data.get('routes'):
            return jsonify({'error': 'Route not found'}), 404

        distance_m = osrm_data['routes'][0]['distance']
        distance_km = distance_m / 1000.0

        return jsonify({'distance_km': round(distance_km, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
