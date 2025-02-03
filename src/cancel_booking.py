import sys
import sqlite3

DB_PATH = "/data/data.db"

def cancel_booking(booking_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return f"Booking ID {booking_id} not found. Please try again with a valid booking ID."

    cursor.execute("DELETE FROM booking WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return f"Your booking with ID {booking_id} has been cancelled successfully."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Missing booking ID")
        sys.exit(1)
    
    booking_id = sys.argv[1]
    
    result = cancel_booking(booking_id)
    print(result)
    sys.exit(0)
