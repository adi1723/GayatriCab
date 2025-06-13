from flask import Flask, request, render_template, redirect, jsonify,url_for
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


from flask import Flask, request, redirect, flash
import smtplib
from email.message import EmailMessage
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
HEADERS = {
    'User-Agent': 'GayatriCab/1.0 (admin@gayatricab.com)'  # Required by Nominatim
}

@app.route('/')
def home():
    status = request.args.get('status')
    return render_template('index.html', status=status)



# Load environment variables from .env file
load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')        # .env मधून वाचेल

def send_booking_email(data):
    subject = 'New Booking Received'
    body = f"""
    Name: {data.get('name')}
    Mobile: {data.get('mobile')}
    Pickup Address: {data.get('pickup')}
    Drop Address: {data.get('drop')}
    Pickup Date: {data.get('pickupDate')}
    Return Date: {data.get('returnDate')}
    Pickup Time: {data.get('pickupTime')}
    Passengers: {data.get('passengers')}
    Cab Type: {data.get('cabType')}
    Fare: {data.get('fare')}
    """


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print('Error sending email:', e)
        return False

@app.route('/send-booking-email', methods=['POST'])
def send_booking_email_route():
    data = request.json
    if send_booking_email(data):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'}), 500


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

@app.route('/Details_Shirdi')
def Details_Shirdi():
    return render_template('Details_Shirdi.html')

@app.route('/Details_Lavasa')
def Details_Lavasa():
    return render_template('Details_Lavasa.html')

@app.route('/Details_Lonavala')
def Details_Lonavala():
    return render_template('Details_Lonavala-Khandala.html')

@app.route('/review', methods=['GET'])
def review():
    return render_template('review.html')

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