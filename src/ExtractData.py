from math import inf


def extract_and_filter_data(input_filepath: list[tuple[str, str, str]]) -> dict:
    """
    Read the file line by line and extract data between "ZGC2" and "ZGC3" then write the difference between the min and
    max of all the third columns
    :param input_filepath:
    :return: Dictionary of [Serial Number] = Tip Tilt Deviation
    """
    dataMarker = ['ZGC2Data,4', 'ZGC2Data,5', 'ZGC2Data,6', 'ZGC2Data,7']
    data_between_markers = []
    difference = {}
    capture_data = False
    for i in range(len(input_filepath)):
        lowest = 0
        highest = 0
        data_between_markers.clear()
        try:
            with open(input_filepath[i][0], 'r') as infile:
                for line in infile:
                    if any(marker in line for marker in dataMarker):
                        capture_data = True
                        continue
                    if 'ZGC3' in line:
                        capture_data = False
                    if capture_data:
                        lowest = min(lowest, float(line.split(',')[2]))
                        highest = max(highest, float(line.split(',')[2]))
        except FileNotFoundError:
            print(f"Invalid filename: {input_filepath}")
        difference[input_filepath[i][1]] = (str(abs(highest-lowest)))

    return difference
