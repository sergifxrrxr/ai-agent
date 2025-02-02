import sys

def cancel_booking(booking_id):
    return f"Your booking with ID {booking_id} has been cancelled successfully."

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Missing booking ID")
        sys.exit(1)
    
    booking_id = sys.argv[1]
    
    result = cancel_booking(booking_id)
    print(result)
    sys.exit(0)
