import sys

def change_booking_dates(booking_id, new_check_in, new_check_out):
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
