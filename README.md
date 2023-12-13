# Description:

M3F_Crawler_Scraper is a program used to extract and summarize archived ST80 test data for M3-F modules. 
It allows the user to enter a range or list of serial numbers, select if they would like to extract the most recent, 
or the oldest test data for these modules, and summarizes the data found for the specified serial numbers in a CSV file.

# Language:
Python 3

# Necessary Modules:
soupsieve.util lower
regex

# Structure:
M3F_Crawler Scraper uses regular expressions to search through RTF and CSV output files from ST80 tests. The data is then
summarized in an output CSV. The target directories are as follows:
    "N:/Test Data/07034-3-0000 M3-F-1p8-1p5-M12-LQ/TestRunOutput"
    "N:/Test Data/05516-3-0000 M3-F-1.8-1.5-M12/TestRunOutput"
    "N:/Test Data/07034-3-0000 M3-F-1p8-1p5-M12-LQ/ScanData"
    "N:/Test Data/05516-3-0000 M3-F-1.8-1.5-M12/ScanData"

# How to Use:
Run main.py. When prompted select either "Run 1st_test_crawler functionality" or "Run most_recent_test_crawler functionality." 
You may enter a batch note which will be included in the output filename. Simply hit enter to leave this blank. 
Next, enter the serial numbers you would like to extract data for as either a comma seperated list (e.g. 1,2,3,4) or a
hyphenated list (e.g. 1-4). If files corosponding to those serial numbers are found in any of the target directories, the data
will be written to the CSV.

# Parameters Recorded:

**Serial Number**; the S/N of the module tested

**Date**; Date of test from which data was extracted

**Mechanical Travel**; The maximum travel achieved, hard stop to hard stop, of a given module

**Dynamic Tip/Tilt**; The maximum deviation, in degrees, of the target relative to itself as it moves through the travel

**Static Tip/Tilt**; The maximum deviation, in degrees, of the target relative to the calibration block as it moves through the travel

**Absolute Tip/Tilt Direction**; The direction in which the module is tilted when the maximum static tip/tilt is recorded. This is a
polar angle which increases counterclockwise with the zero at the back of the module (where the board is). For example, tilting
towards the operator, in the direction of the board when the module is inserted into the test fixture, this value would be 0 degrees. 
Tilting to the operator's right would be 90 degrees, and tilting away from the operator would be 180 degrees.

**Motor Frequency**; The motor default frequency in kHz

**Motor Current**; The maximum motor current in mA

**Max Gain** - Vertical; The maximum gain value tested in the upright position
	
**Max Gain** - Inverted; The maximum gain value tested in the inverted position
	
**Max Gain** - Horizontal; The maximum gain value tested in the horizontal position

**Tip/Tilt Deviation**; This is value meant to quantify the nature of a module's tip tilt. It is the difference between the 
polar direction of the maximum static tip/tilt, and the polar direction of the minimum static tip/tilt (in degrees). This value has 
some issues and should not be considered statistically significant, as some modules may change direction from slightly past 0 degrees
to slightly less than 360 degrees, giving a value close to 360 when, in, reality, the tip/tilt direction only changed by a few degrees.

    

