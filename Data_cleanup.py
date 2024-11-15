import pandas as pd
import re

# Function to clean email (simple check to ensure valid email format)
def clean_email(email):
    if isinstance(email, str) and re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return email
    else:
        return None  # In case email format is incorrect

# Function to clean phone numbers (simplifying to remove non-numeric characters)
def clean_phone(phone):
    if isinstance(phone, str):
        cleaned = re.sub(r'\D', '', phone)  # Remove non-numeric characters
        return cleaned if len(cleaned) == 10 else None  # Ensure 10 digits
    return None

# Main function to clean the data
def clean_data(file_path):
    try:
        # Now We're Going to Load the data (assuming the file is a CSV or text file)
        data = pd.read_csv(file_path, delimiter='|', header=None)
        data.columns = ['ID', 'Date', 'Time', 'Name', 'Email', 'Phone', 'Status']  # Assign column names

        # Print status message :)
        print("Data loaded successfully. Starting cleanup process...\n")

        # Clean the 'Email' column :P
        data['Email'] = data['Email'].apply(clean_email)
        print("Email addresses cleaned...")

        # Clean the 'Phone' column
        data['Phone'] = data['Phone'].apply(clean_phone)
        print("Phone numbers cleaned...")

        # Handle missing values or invalid entries by removing rows where necessary columns are None
        data = data.dropna(subset=['Email', 'Phone'])
        print(f"Removed rows with missing or invalid email/phone. {len(data)} rows remaining...")

        # Convert 'Date' and 'Time' columns to proper datetime format (if needed)
        data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], errors='coerce')
        data = data.dropna(subset=['DateTime'])  # Remove rows where datetime couldn't be parsed
        print("Date and Time columns cleaned...\n")

        # Optionally drop the original 'Date' and 'Time' columns after combining them
        data = data.drop(columns=['Date', 'Time'])

        # Just Gonna go Preview the Data
        print("Preview of cleaned data:\n", data.head())

        # Ask for output file name/path
        output_file = input("Enter the name (or full path) of the output CSV file (e.g., cleaned_data.csv): ")

        # Save the cleaned data to a CSV file Yay.
        data.to_csv(output_file, index=False)
        print(f"\nData saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point of the program :)
if __name__ == "__main__":
    # Ask the user for the input file name or path
    input_file = input("Enter the full path or name of the file to be cleaned (e.g., data.txt): ")
    clean_data(input_file)