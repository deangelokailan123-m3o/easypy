# easypy.py
import os
import time
from datetime import datetime

def interactive_time_travel():
    """
    Asks the user for a date/time and a file path using ONLY built-in Python tools.
    Enforces the 1998 limit and applies the timestamp.
    """
    # 1. Ask for the date/time
    user_date_input = input("Enter a date (e.g., 1999) or date + time (e.g., 6/3/1999 10:07 AM): ").strip()
    
    parsed_date = None
    
    # Define the formats we want to support
    formats_to_try = [
        "%m/%d/%Y %I:%M %p",  # 6/3/1999 10:07 AM
        "%m/%d/%Y %I:%M%p",   # 6/3/1999 10:07AM (no space)
        "%Y"                  # 1999
    ]
    
    # Try parsing the input using the formats above
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(user_date_input, fmt)
            break  # Stop looking if we successfully matched a format
        except ValueError:
            continue

    # If none of the formats matched, throw an error
    if not parsed_date:
        print("❌ Error: Couldn't understand that format. Please use 'YYYY' or 'M/D/YYYY HH:MM AM/PM'.")
        return

    # Enforce our strict 1998 floor limit
    if parsed_date.year < 1998:
        print(f" No way! {parsed_date.year} is too old. Capping the year limit to 1998.")
        parsed_date = parsed_date.replace(year=1998)

    # 2. Ask for the file target
    file_path = input("What file do you want to apply the date and time to?: ").strip()

    # 3. Verify the file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: The file '{file_path}' does not exist.")
        return

    try:
        # Convert our parsed datetime into an OS-compatible timestamp
        timestamp = time.mktime(parsed_date.timetuple())
        
        # Apply changes to Last Accessed and Last Modified times
        os.utime(file_path, (timestamp, timestamp))
        
        # Format a nice success message
        formatted_final = parsed_date.strftime("%m/%d/%Y %I:%M %p")
        print(f" Success! Applied {formatted_final} to '{file_path}'.")
        
    except Exception as e:
        print(f"❌ An error occurred while modifying the file: {e}")