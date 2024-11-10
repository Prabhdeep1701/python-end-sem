import sqlite3

# Function to initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect('attendance_system.db')  # This creates or connects to attendance_system.db
    cursor = conn.cursor()

    # Create sessions table to store QR code session details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,     -- Unique session ID
            latitude REAL,                   -- Latitude of the QR code generation location
            longitude REAL,                  -- Longitude of the QR code generation location
            max_range INTEGER,               -- Maximum allowed scanning range (in meters)
            timestamp TEXT                   -- Time the QR code was generated
        )
    ''')

    # Create attendance table to store scan details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            scan_id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Auto-incremented scan ID
            session_id TEXT,                             -- Session ID linked to the QR code
            scanner_latitude REAL,                       -- Latitude of the scanner
            scanner_longitude REAL,                      -- Longitude of the scanner
            scan_timestamp TEXT,                         -- Timestamp when the scan occurred
            FOREIGN KEY(session_id) REFERENCES sessions(session_id)  -- Foreign key linking to sessions
        )
    ''')

    conn.commit()  # Commit the changes
    conn.close()   # Close the connection

# Function to store QR code session details in the database
def store_session(session_id, latitude, longitude, max_range, timestamp):
    conn = sqlite3.connect('attendance_system.db')  # Connect to the database
    cursor = conn.cursor()

    # Insert session details into the sessions table
    cursor.execute('''
        INSERT INTO sessions (session_id, latitude, longitude, max_range, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, latitude, longitude, max_range, timestamp))

    conn.commit()  # Commit the transaction
    conn.close()   # Close the connection

# Function to log attendance when a QR code is scanned
def log_scan(session_id, scanner_latitude, scanner_longitude, scan_timestamp):
    conn = sqlite3.connect('attendance_system.db')  # Connect to the database
    cursor = conn.cursor()

    # Insert scan details into the attendance table
    cursor.execute('''
        INSERT INTO attendance (session_id, scanner_latitude, scanner_longitude, scan_timestamp)
        VALUES (?, ?, ?, ?)
    ''', (session_id, scanner_latitude, scanner_longitude, scan_timestamp))

    conn.commit()  # Commit the transaction
    conn.close()   # Close the connection

# Initialize the database when this script is run
if __name__ == "__main__":
    initialize_database()  # Call the function to initialize the database
