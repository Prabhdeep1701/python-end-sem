import qrcode
from datetime import datetime
from geopy.geocoders import Nominatim
from databse import store_session  # Import the function to store session details

# Function to fetch current location using geopy with error handling
def fetch_current_location():
    try:
        geolocator = Nominatim(user_agent="attendance_system")
        location = geolocator.geocode("Bennett University, Greater Noida, Uttar Pradesh, India")
        if location:
            return location.latitude, location.longitude
        else:
            return 28.4595, 77.5003  # Fallback coordinates
    except Exception as e:
        return 28.4595, 77.5003  # Fallback coordinates

# Function to generate QR code with session ID, location, and range data
def generate_qr_code(session_id, latitude, longitude, max_range):
    try:
        qr_data = f"{session_id}_{latitude},{longitude}_{max_range}m"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(f'qr_codes/{session_id}.png')
        print(f"QR code generated and saved as 'qr_codes/{session_id}.png'")
    except Exception as e:
        print(f"Error generating QR code: {e}")

# Generate QR code for a session and store session details in the database
def main():
    session_id = f"CSE101_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    latitude, longitude = fetch_current_location()
    max_range = 50  # Example range in meters
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if latitude is not None and longitude is not None:
        generate_qr_code(session_id, latitude, longitude, max_range)
        store_session(session_id, latitude, longitude, max_range, timestamp)  # Store session in database

if __name__ == "__main__":
    main()
