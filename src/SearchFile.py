import os
import time
import regex as re


def find_file_by_serial(directories: list[str], serialNumbers: list[str], choice: str) -> list[tuple[str, str, str]]:
    """
    Searches through file directories to find files associated with inputted serial numbers
    :param directories: List of directories to search
    :param serialNumbers: List of serial numbers to search for in the filename
    :param choice: Choose to sort from the oldest file or the newest file
    :return: Returns the oldest or newest files matching the serial numbers you input and the output filepath
    """
    # Filepath to location of matching files
    matchingFiles = []

    # Used to get the newest or oldest version. Value = date/time created, filepath
    fileDictionary = {}

    for serialNum in serialNumbers:
        serialFound = False
        for directory in directories:
            for filename in os.listdir(directory):
                if f"M3-F_{serialNum}_" in filename or f"M3-F__{serialNum}__" in filename:
                    t_obj = time.strptime(time.ctime(os.path.getmtime(os.path.join(directory, filename))))
                    T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
                    if serialNum not in fileDictionary:
                        fileDictionary[serialNum] = (os.path.getmtime(os.path.join(directory, filename)),
                                                     os.path.join(directory, filename), serialNum, T_stamp)
                    else:
                        if choice == "2":
                            if fileDictionary[serialNum][0] <= os.path.getmtime(os.path.join(directory, filename)):
                                fileDictionary[serialNum] = ((os.path.getmtime(os.path.join(directory, filename)),
                                                              os.path.join(directory, filename),serialNum, T_stamp))
                        else:
                            if fileDictionary[serialNum][0] >= os.path.getmtime(os.path.join(directory, filename)):
                                fileDictionary[serialNum] = ((os.path.getmtime(os.path.join(directory, filename)),
                                                              os.path.join(directory, filename), serialNum, T_stamp))
        if serialNum in fileDictionary:
            serialFound = True
        if not serialFound:
            print(f"Serial Number {serialNum} not found")

    # Create list of filepaths from final values in dictionary
    for filepath in fileDictionary.values():
        matchingFiles.append(filepath[1::])

    if not matchingFiles:
        print("No matching files found")
        return None

    return matchingFiles
