import csv
import datetime

from soupsieve.util import lower

from M3F_Crawler_v01 import *

endTest = False


def main():
    print("Choose an option:")
    print("1. Run 1st_test_crawler functionality")
    print("2. Run most_recent_test_crawler functionality")
    choice = input("Enter your choice (1/2): ")
    print(choice)
    while choice != "1" and choice != "2":
        choice = input("Please enter a valid number: ")

    batch_note = input("Please enter the Batch Note: ")
    serial_numbers_input = input("Please enter the serial numbers separated by commas (e.g., 12345, 67890): ")
    serial_numbers = {sn.strip(): None for sn in serial_numbers_input.split(",")}
    output_dir = "Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    directories = [
        "N:/Test Data/07034-3-0000 M3-F-1p8-1p5-M12-LQ/TestRunOutput",
        "N:/Test Data/05516-3-0000 M3-F-1.8-1.5-M12/TestRunOutput"
    ]
    files_for_serials = {}
    for directory_path in directories:
        print(f"\nProcessing directory: {directory_path}")
        if choice == "1":
            find_files_for_serials(directory_path, serial_numbers, files_for_serials, False)
        elif choice == "2":
            find_files_for_serials(directory_path, serial_numbers, files_for_serials, True)
    results = fileParser(files_for_serials)
    current_time = datetime.datetime.now().strftime('%m-%d-%y_%I-%M-%p')
    if choice == "1":
        csv_filename = os.path.join(output_dir, f'1st_test_output_{batch_note}_{current_time}.csv')
    else:
        csv_filename = os.path.join(output_dir, f'most_recent_test_output_{batch_note}_{current_time}.csv')

    # Writing Data to CSV

    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_directory, "Output", csv_filename)

    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["Serial Number", "Date", "Mechanical Travel", "Dynamic Tip/Tilt", "Static Tip/Tilt", "Absolute Tip/Tilt "
                                                                                                  "Direction",
             "Motor Frequency", "Motor Current", "Max Gain - Vertical", "Max Gain - Inverted", "Max Gain - Horizontal"])
        for file_id, values in results.items():

            # Check if the extracted values match the expected format
            if len(values) == 10:
                writer.writerow([file_id] + list(values))

    print("\nResults written to:", csv_file_path)


if __name__ == "__main__":
    while True:
        main()
        endTest = input("Would you like to parse more data? (Y/N)")
        while lower(endTest) != "y" and lower(endTest) != "n":
            endTest = input("Please type Y or N")
        if endTest == "n":
            break
        else:
            continue
