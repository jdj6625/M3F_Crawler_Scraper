import os
import regex as re
import time


def findFilesForSerials(directories: list, serial_numbers: dict, choice: str) -> dict:
    """
    Function to find files for serials
    :param list directories: List of file directories on PC you would like to scan
    :param dict serial_numbers: A dictionary of serial numbers to be searched for
    :param str choice: 1 to grab the oldest file, 2 to grab the newest
    :return: Dictionary of all files with matching serial numbers
    """
    filename_pattern = r"M3-F__(\d+)__(\d{4}-\d{2}-\d{2})__"
    filename_regex = re.compile(filename_pattern)
    filesForSerials = {}
    for directory in directories:
        rtf_files = {f for f in os.listdir(directory) if f.endswith('.rtf')}
        print(f"Total RTF files in {directory}: {len(rtf_files)}")
        for filename in rtf_files:
            match = filename_regex.search(filename)
            if match:
                file_id, file_date = match.groups()
                if file_id in serial_numbers:
                    mtime = os.path.getmtime(os.path.join(directory, filename))
                    if file_id not in filesForSerials:
                        filesForSerials[file_id] = (directory, filename, mtime, file_date)
                    elif choice == '1':
                        if mtime > filesForSerials[file_id][2]:
                            filesForSerials[file_id] = (directory, filename, mtime, file_date)
                    elif choice == '2':
                        if mtime < filesForSerials[file_id][2]:
                            filesForSerials[file_id] = (directory, filename, mtime, file_date)
    return filesForSerials


def fileParser(filesForSerials: list) -> dict:
    """
    Function to extract data from files
    :param list filesForSerials: A list containing tuples with (Filepath Directory, Serial Number, Date Created)
    :return: dict results: A dictionary with extracted data from the files
    """
    start_time = time.time()
    max_gain_pattern = r"Max Gain: (\d+)"
    mechanical_travel_pattern = r"Mechanical Travel: \d+(\.\d+)? <= (\d+(\.\d+)?) <= \d+(\.\d+)?"
    dynamic_tip_tilt_pattern = r"Dynamic Tip/Tilt [a-zA-Z]+: ([\d.]+)deg"
    static_tip_tilt_pattern = r"Static Tip/Tilt [a-zA-Z]+: ([\d.]+)deg"
    motor_frequency_pattern = r"Motor frequency \(([\d.]+)\)"
    motor_current_pattern = r"Motor current (\d+(\.\d+)?) mA"
    absolute_tip_tilt_max_direction_pattern = r"Absolute Tip/Tilt Max Direction: ([\d.]+)"
    regex_mechanical_travel = re.compile(mechanical_travel_pattern)
    regex_dynamic_tip_tilt = re.compile(dynamic_tip_tilt_pattern)
    regex_static_tip_tilt = re.compile(static_tip_tilt_pattern)
    regex_motor_frequency = re.compile(motor_frequency_pattern)
    regex_motor_current = re.compile(motor_current_pattern)
    regex_max_gain = re.compile(max_gain_pattern)
    regex_absolute_tip_tilt = re.compile(absolute_tip_tilt_max_direction_pattern)
    results = {'Max Gain - Upright': [], 'Max Gain - Inverted': [], 'Max Gain - Horizontal': []}

    for filePath, serialNumber, creationDate in filesForSerials:
        with open(filePath, 'r') as file:
            content = file.read()
            max_gain_matches = regex_max_gain.findall(content)
            if len(max_gain_matches) == 1:
                max_gain_upright = max_gain_matches[0]
                max_gain_inverted = max_gain_horizontal = "N/A"
            elif len(max_gain_matches) == 2:
                max_gain_upright, max_gain_inverted = max_gain_matches
                max_gain_horizontal = "N/A"
            elif len(max_gain_matches) == 3:
                max_gain_upright, max_gain_inverted, max_gain_horizontal = max_gain_matches
            else:
                max_gain_upright = max_gain_inverted = max_gain_horizontal = "N/A"

        match_mechanical_travel = regex_mechanical_travel.search(content)
        match_dynamic_tip_tilt = regex_dynamic_tip_tilt.search(content)
        match_static_tip_tilt = regex_static_tip_tilt.search(content)
        match_absolute_tip_tilt = regex_absolute_tip_tilt.search(content)
        if match_mechanical_travel:
            middle_number = match_mechanical_travel.group(2)
            dynamic_value = match_dynamic_tip_tilt.group(1) if match_dynamic_tip_tilt else "N/A"
            absolute_value = match_absolute_tip_tilt.group(1) if match_absolute_tip_tilt else "N/A"
            static_value = match_static_tip_tilt.group(1) if match_static_tip_tilt else "N/A"
            motor_frequency_value = regex_motor_frequency.search(content).group(
                1) if regex_motor_frequency.search(content) else "N/A"
            motor_current_match = regex_motor_current.search(content)
            motor_current_value = motor_current_match.group(1) if motor_current_match else "N/A"
            results[serialNumber] = (
                creationDate, middle_number, dynamic_value, static_value, absolute_value, motor_frequency_value,
                motor_current_value,
                max_gain_upright, max_gain_inverted, max_gain_horizontal)
            print(f"Data extracted for {serialNumber} from {filePath}")
        else:
            print(f"No match found in file {filePath} for {serialNumber}. Trying the next file...")
    print("--- %s seconds ---" % (time.time() - start_time))
    return results
