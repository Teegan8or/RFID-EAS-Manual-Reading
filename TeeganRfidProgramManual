import os
import csv
import datetime
import time

FileName = "TMRWVialGoodList"                          # Threw a random name in here
Date = datetime.datetime.now().strftime("%Y%m%d")
Ids = set()

def ReaderIdConvert(DecimalValue):                     # Kevin's code to convert to hexadecimal
    HexValue = hex(int(DecimalValue))[2:].upper()      # Remove '0x' and convert to uppercase
    return HexValue

def GetEmployeeNum():                                  # Function to get the employee number, and make sure its correct
    while True:
        EmployeeNum = input("Enter employee number: ")
        ConfirmEmployeeNum = input("Confirm employee number: ")
        if EmployeeNum == ConfirmEmployeeNum:
            return EmployeeNum
        else:
            print("Numbers do not match. Please try again.")

def MakeCSV():                                         # Check for existing file, if it does not exist, make one with the proper headers
    if not os.path.exists(FileName + ".csv") or os.stat(FileName + ".csv").st_size == 0:
        with open(FileName + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Scanned Tag', 'Employee Number', 'Date', 'Time'])
            print("The file has been created")

def ReadCSVMakeSet():                                  # Reads the file if already present, and writes the ids in the file to the set
    if os.path.exists(FileName + ".csv") and os.stat(FileName + ".csv").st_size > 0:
        with open(FileName + ".csv", 'r', newline='') as file:
            print("file has been opened")
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                Ids.add(row[0])


def TakeTimeStamp():                                   # Function to take a timestamp eveytime a tag is enterd into the set
    TimeStamp = time.time()
    DateTimeObject = datetime.datetime.fromtimestamp(TimeStamp)
    Time = DateTimeObject.strftime("%H:%M:%S")
    return Time

def main():
    EmployeeNum = GetEmployeeNum()                     # Get the user's employees number
    print("Press Ctrl+C to exit the program")          # Let the user know how to exit
    ReadCSVMakeSet()                                   # Make sure that the file already exists
    
    while True:
        try:
            DecimalValue = input("Scan the RFID tag please. Press Ctrl+C to exit. ") # Tag entry
            HexValue = ReaderIdConvert(DecimalValue)   # Convert the tags value
            
            if len(HexValue) != 16:                    # Check for invalid input
                print("The number scanned is not valid. Please scan a tag with a 16 digit Hex.")
                continue                               # Skip this iteration if the hex is invalid
            
            if HexValue in Ids:                        # Make sure that the tag had not already been scanned
                print("This tag has already been scanned.")
            else:
                Ids.add(HexValue)                      # Add the tag value to the set

                try:
                    MakeCSV()                          # Create the File if it does not exist 

                                                       # Append the new data to the CSV
                    with open(FileName + ".csv", 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([HexValue, EmployeeNum, Date, TakeTimeStamp()])

                    print("A tag has been recorded")   # Let the user know that a tag has been scanned and enter into the file

                except PermissionError:                # Likely the file is open in Excel, and thus you wont be able to write to it
                    print("You don't have the proper permissions to write to or open this file")
                    Ids.remove(HexValue)               # Ensure that the id value is not recorded, and can be scanned again

        except ValueError:
            print("The tag that was scanned is invalid")
        except KeyboardInterrupt:
            print("Closing the program")
            break
            
if __name__ == "__main__":
    main()
