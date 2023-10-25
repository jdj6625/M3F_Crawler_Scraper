import csv

from ExtractData import *
from SearchFile import *
from soupsieve.util import lower
from datetime import datetime

from M3F_Crawler_v01 import *

endTest = False
output_dir = "../Output"
current_time = datetime.now().strftime('%m-%d-%y_%I-%M-%p')

directories = [
    "N:/Test Data/07034-3-0000 M3-F-1p8-1p5-M12-LQ/TestRunOutput",
    "N:/Test Data/05516-3-0000 M3-F-1.8-1.5-M12/TestRunOutput"
]
directories2 = [
    "N:/Test Data/07034-3-0000 M3-F-1p8-1p5-M12-LQ/ScanData",
    "N:/Test Data/05516-3-0000 M3-F-1.8-1.5-M12/ScanData"
]


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
    if '-' in serial_numbers_input:
        minimum, maximum = serial_numbers_input.replace(" ", "").split('-')
        serialNumbers = [*range(int(minimum), int(maximum) + 1)]

    else:
        serialNumbers = serial_numbers_input.replace(" ", "").split(',')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extractedInfo = fileParser(find_file_by_serial(directories, serialNumbers, choice))

    inputFilepath = find_file_by_serial(directories2, serialNumbers, choice)

    if inputFilepath:
        tipTiltDeviation = extract_and_filter_data(inputFilepath)

    if choice == "1":
        csv_filename = os.path.join(output_dir, f'oldest_test_output_{batch_note}_{current_time}.csv')
    else:
        csv_filename = os.path.join(output_dir, f'newest_test_output_{batch_note}_{current_time}.csv')

    # Writing Data to CSV

    script_directory = os.path.dirname(os.path.realpath(__file__))
    csv_file_path = os.path.join(script_directory, "../Output", csv_filename)

    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ["Serial Number", "Date", "Mechanical Travel", "Dynamic Tip/Tilt", "Static Tip/Tilt", "Absolute Tip/Tilt "
                                                                                                  "Direction",
             "Motor Frequency", "Motor Current", "Max Gain - Vertical", "Max Gain - Inverted", "Max Gain - Horizontal",
             "Tip/Tilt Deviation"])
        for i, (file_id, values) in enumerate(extractedInfo.items()):
            # Check if the extracted values match the expected format
            if len(values) == 10:
                if file_id in tipTiltDeviation:
                    writer.writerow([file_id] + list(values) + [tipTiltDeviation[file_id]])
                else:
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
