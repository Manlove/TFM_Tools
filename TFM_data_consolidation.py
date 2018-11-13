import pandas as pd
from os import chdir, listdir
from os.path import isdir, join
from tkinter import Tk
from tkinter.filedialog import askdirectory
from openpyxl import Workbook


Tk().withdraw()
path= askdirectory()


book = Workbook()
writer = pd.ExcelWriter(book, engine='openpyxl')
writer.book = book
time_points = 5

chdir(path)
well_list = [f for f in listdir(path) if isdir(join(path, f))]
well_list.sort()

for well in well_list:
    print("~~~~~~~~~~~~{}~~~~~~~~~~~~".format(well))
    well_path = join(path, well)
    chdir(well_path)
    position_list = [f for f in listdir(well_path) if isdir(join(well_path, f))]
    data = []
    for position in position_list:
        pos_path = join(well_path, position)
        chdir(pos_path)
        try:
            chdir(join(pos_path, "Tractions"))
        except:
            print("{}, {}: No Tractions Folder".format(well, position))
            continue
        try:
            traction_file = pd.read_excel('Tractions.xlsx', sheet_name='Sheet2')
        except:
            print("{}, {}: No Tractions.xlsx File".format(well, position))
            continue
        try:
            RMS = traction_file['Unnamed: 8'][1:time_points + 2]
            MAX = traction_file['Unnamed: 11'][1:time_points + 2]
            Merged_data = pd.concat([RMS, pd.Series(['']), MAX], axis = 0)
            Merged_data.name = position
            data.append(Merged_data)
        except:
            print("{}, {}: Something broke".format(well, position))
            continue

    chdir(well_path)
    try:
        data_out = pd.concat(data, axis = 1)
    except:
        print("No data to write\n")
        continue
    try:
        data_out.to_excel('{}.xlsx'.format(well))
        print("Data Written to well")
    except:
        print("Failed to write data to well folder")
    try:
        data_out.to_excel(writer, sheet_name = '{}'.format(well))
        print("Data added to summary sheet")
    except:
        print("Failed to add data to summary sheet")

    print("")

chdir(path)
book.save('summary.xlsx')
