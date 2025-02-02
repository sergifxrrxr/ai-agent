import sys
import uuid
import random

def book_hotel(hotel, check_in, check_out, adults, children):
    booking_id = str(random.randint(100000, 999999))
    return f"Your booking for {hotel} from {check_in} until {check_out} for {adults} adults and {children} children has been created successfully! Your booking id is {booking_id}."

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Error: Missing arguments")
        sys.exit(1)
    
    hotel = sys.argv[1]
    check_in = sys.argv[2]
    check_out = sys.argv[3]
    adults = sys.argv[4]
    children = sys.argv[5]

    booking_id = book_hotel(hotel, check_in, check_out, adults, children)
    print(booking_id)
    sys.exit(0)
