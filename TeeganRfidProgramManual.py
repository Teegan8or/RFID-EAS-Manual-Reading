import os
import csv
import datetime
import time

FileName = "TMRWVialGoodList"                          # Threw a random name in here
Date = datetime.datetime.now().strftime("%Y%m%d")
Ids = set()                                            # A temp variable to be used in the main loop to lookup the column


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
            writer.writerow(['Scanned Tag', 'Employee Number', 'Date', 'Time', 'Second Scan', 'Third Scan', 'Fourth Scan', 'Fith Scan', 'Sixth Scan'])
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

def SecondTimeStamp(HexValue):                         # Function to handle multiple scans
    rows = []
    updated = False

    try:
        with open(FileName + ".csv", 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows.append(header)

            for row in reader:
                if row[0] == HexValue:
                    for i in range(4, 9):              # Update the scan time columns
                        if row[i] == '':
                            row[i] = TakeTimeStamp()
                            updated = True
                            break
                rows.append(row)

        if updated:
            with open(FileName + ".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"Another time has been recorded for this tag.")
        else:
            print(f"Tag {HexValue} not found to update scan time.")
    except IndexError:
        print(f"Error: The CSV file does not have the expected number of columns for tag {HexValue}.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    EmployeeNum = GetEmployeeNum()
    print("Press Ctrl+C to exit the program")
    ReadCSVMakeSet()

    while True:
        try:
            DecimalValue = input("Scan the RFID tag please. Press Ctrl+C to exit.\n")
            HexValue = ReaderIdConvert(DecimalValue)

            if len(HexValue) != 16:
                print("The number scanned is not valid. Please scan a tag with a 16 digit Hex.\n")
                continue

            if HexValue in Ids:
                SecondTimeStamp(HexValue)
            else:
                Ids.add(HexValue)
                MakeCSV()

                with open(FileName + ".csv", 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([HexValue, EmployeeNum, Date, TakeTimeStamp(), '', '', '', '', ''])

                print("A tag has been recorded")

        except ValueError:
            print("The tag that was scanned is invalid")
        except PermissionError:
            print("You don't have the proper permissions to write to or open this file")
        except KeyboardInterrupt:
            print("Closing the program")
            break
            
if __name__ == "__main__":
    main()
