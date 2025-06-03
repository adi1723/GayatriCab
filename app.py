from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Mail configuration using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # ✅ default sender

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        pickup = request.form.get('pickup')
        destination = request.form.get('destination')
        date = request.form.get('date')
        time = request.form.get('time')
        cab_type = request.form.get('cab-type')
        passengers = request.form.get('passengers')

        try:
            msg = Message('New Cab Booking',
                          recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
New Cab Booking:
Pickup Location: {pickup}
Destination: {destination}
Date: {date}
Time: {time}
Cab Type: {cab_type}
Number of Passengers: {passengers}
            """
            mail.send(msg)
            message = "✅ Booking available. Please confirm via Contact section."
        except Exception as e:
            message = f"❌ Error sending email: {str(e)}"

    return render_template("index.html", message=message)

if __name__ == '__main__':
    app.run(debug=True)
