import sqlite3
from datetime import datetime
from geopy.distance import geodesic  # To calculate the distance between two locations
from databse import log_scan

# Function to calculate the distance between two sets of GPS coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

# Function to scan and log attendance
def scan_qr_code(session_id, scanner_latitude, scanner_longitude):
    conn = sqlite3.connect('attendance_system.db')
    cursor = conn.cursor()

    # Retrieve session details from the database
    cursor.execute('SELECT latitude, longitude, max_range FROM sessions WHERE session_id = ?', (session_id,))
    session = cursor.fetchone()

    if session:
        session_latitude, session_longitude, max_range = session
        distance = calculate_distance(session_latitude, session_longitude, scanner_latitude, scanner_longitude)
        
        if distance <= max_range:
            scan_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_scan(session_id, scanner_latitude, scanner_longitude, scan_timestamp)
            print(f"Attendance logged successfully for session {session_id}. Distance: {distance:.2f} meters")
        else:
            print(f"Scan failed. You are too far from the session location ({distance:.2f} meters away).")
    else:
        print(f"Session {session_id} not found.")

    conn.close()

# Example usage of scanning a QR code
def main():
    session_id = input("Enter the session ID from the QR code: ")
    scanner_latitude = float(input("Enter your current latitude: "))
    scanner_longitude = float(input("Enter your current longitude: "))

    scan_qr_code(session_id, scanner_latitude, scanner_longitude)

if __name__ == "__main__":
    main()
