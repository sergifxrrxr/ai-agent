import sys
import sqlite3

DB_PATH = "/data/data.db"

def change_booking_dates(booking_id, new_check_in, new_check_out):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM booking WHERE booking_id = ?", (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return f"Booking ID {booking_id} not found."

    cursor.execute("""
        UPDATE booking
        SET check_in = ?, check_out = ?
        WHERE booking_id = ?
    """, (new_check_in, new_check_out, booking_id))

    conn.commit()
    conn.close()
    return f"Your booking with ID {booking_id} dates have been changed to check-in: {new_check_in}, check-out: {new_check_out}"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: Missing parameters for date change")
        sys.exit(1)
    
    booking_id = sys.argv[1]
    new_check_in = sys.argv[2]
    new_check_out = sys.argv[3]
    
    result = change_booking_dates(booking_id, new_check_in, new_check_out)
    print(result)
    sys.exit(0)
