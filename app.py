from flask import Flask, render_template, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file (if present)
load_dotenv()

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # environment variable name here
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # environment variable name here
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # default sender is your email


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
            # Prepare email notification to yourself
            msg = Message('New Cab Booking',
                          sender=app.config['MAIL_DEFAULT_SENDER'],
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
