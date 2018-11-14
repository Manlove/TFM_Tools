import pandas as pd
from os import chdir, listdir
from os.path import isdir, join
from tkinter import Tk
from tkinter.filedialog import askdirectory
from openpyxl import Workbook

# Tkinter call to allow user to select a directory
Tk().withdraw()
path = askdirectory()

# Setting up the workbook to allow writing to multiple sheets.
book = Workbook()   # Workbook from openpyxl
writer = pd.ExcelWriter(book, engine='openpyxl')  # Assign the openpyxl workbook to the pandas excel writer
writer.book = book
time_points = 5

# Changes the path to the directory selected, should be the main plate folder
chdir(path)
# Retrieves a list of well folders from the current directory
well_list = [f for f in listdir(path) if isdir(join(path, f))]
well_list.sort()

# Steps through the wells in the directory
for well in well_list:
    # Updates user on the current well that is being collected
    print("~~~~~~~~~~~~{}~~~~~~~~~~~~".format(well))

    # Changes the directory to the current well
    well_path = join(path, well)
    chdir(well_path)

    # Retrieves a list of position folders from the well directory
    position_list = [f for f in listdir(well_path) if isdir(join(well_path, f))]

    # Creates a list to hold the excel data for the well from all the positions
    well_data = []

    # Steps through the positions in the well
    for position in position_list:

        # Changes the directory to the current position.
        pos_path = join(well_path, position)
        chdir(pos_path)

        # Attempts to move to the "Tractions" directory within the current position askdirectory
        # If no "Tractions" directory is found the user is notified of the well and position
        try:
            chdir(join(pos_path, "Tractions"))
        except:
            print("{}, {}: No Tractions Folder".format(well, position))
            continue

        # Attempts to retrieve the data from Sheet2 of the tractions.xlsx files
        # If this fails the user is notified of the well and position.
        try:
            traction_file = pd.read_excel('Tractions.xlsx', sheet_name='Sheet2')
        except:
            print("{}, {}: No Tractions.xlsx File".format(well, position))
            continue

        # Attempts to write the data from select row and columns to the well_data list
        # At this point this should not fail unless there is an error in how Tractionsforall
        # wrote the excel file.
        try:
            RMS = traction_file['Unnamed: 8'][1:time_points + 2]
            MAX = traction_file['Unnamed: 11'][1:time_points + 2]
            Merged_data = pd.concat([RMS, pd.Series(['']), MAX], axis = 0)
            Merged_data.name = position
            well_data.append(Merged_data)
        except:
            print("{}, {}: Something broke".format(well, position))
            continue

    # Once all positions are complete changes the directory back to the well directory
    chdir(well_path)

    # Attempts to concatinate the data in the well_data list into a sheet.
    # This will fail nd alert the user if no tractions files were found in any of the positions
    try:
        data_out = pd.concat(well_data, axis = 1)
    except:
        print("No data to write\n")
        continue

    # Attempts to write data to the excel sheet with the same name as the current well
    try:
        data_out.to_excel('{}.xlsx'.format(well))
        print("Data Written to well")
    except:
        print("Failed to write data to well folder")

    # Attemps to write data to a sheet with the same name as the current well
    # in the summary excel file.
    try:
        data_out.to_excel(writer, sheet_name = '{}'.format(well))
        print("Data added to summary sheet")
    except:
        print("Failed to add data to summary sheet")

    print("")

chdir(path)
book.save('summary.xlsx')
