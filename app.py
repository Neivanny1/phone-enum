from flask import Flask, request, render_template, flash, redirect, url_for
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

def get_phone_info(phone_number):
    """
    Gets the carrier, country, location, and time zone for a given phone number.

    Args:
        phone_number (str): The phone number to check.

    Returns:
        dict: A dictionary containing phone number details or an error message.
    """
    invalid = "Invalid phone number.Use format E164_format eg. +254790909090"
    try:
        parsed_number = phonenumbers.parse(phone_number, None)  # Parse without country code
    except phonenumbers.NumberParseException:
        return None, invalid

    # Check if the number is valid
    if not phonenumbers.is_valid_number(parsed_number):
        return None, invalid

    # Get E.164 format
    e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    # Get country
    country = geocoder.description_for_number(parsed_number, "en")

    # Get carrier
    carrier_name = carrier.name_for_number(parsed_number, "en")

    # Get time zones
    time_zones = timezone.time_zones_for_number(parsed_number)

    return {
        "e164_format": e164_format,
        "country": country,
        "carrier": carrier_name,
        "time_zones": time_zones
    }, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        phone_info, error = get_phone_info(phone_number)
        
        if phone_info:
            flash("Phone number information retrieved successfully.", 'success')
            return render_template('index.html', phone_info=phone_info)
        else:
            flash(error, 'danger')

        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
