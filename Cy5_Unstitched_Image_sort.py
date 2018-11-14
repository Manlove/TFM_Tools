"""
Cy5_Unstitched_Image_sort.py
Logan Manlove
11/12/2018


"""


from os import chdir, listdir, mkdir, rename
from os.path import isfile, join

##############################################################################
# - Given path should be to the main folder containing all of the images outputted
#   by the cytation 5
# - Bead_channel should be whichever channel is indicated in the bead image at
#   Position 2 in the filename.
# - Cell_channel should be whichever channel is indicated by the Cell image
#   at Position 2 in the filename.
#  0    1     2       3        4      5
# well-read-channel-position-channel-time.tiff
path = ''
Bead_channel = '2'
Cell_channel = '1'
##############################################################################


chdir(path)
# Retrieve a list of files in the directory given in PATH
image_list = [f for f in listdir(path) if isfile(join(path, f))]

# Retrieves the file names and splits the strings by '-' producing 6 pieces with the following designations:
#   0    1     2       3        4      5
# well-read-channel-position-channel-time.tiff
# Sorts the images into a set of nested dictionaries for each well,imaging position and then channel
# creating the dictionary as new keys are found.
# The dictionary has the form of {Well:{Position:{Channel}}}
plate_wells = {}
for file in image_list:
    filename = file.split('_')
    well = filename[0]
    position = filename[3]
    channel = filename[2]
    if well not in plate_wells.keys():
        plate_wells[well] = {}
        plate_wells[well][position] = {}
        plate_wells[well][position][channel] = [file]
    else:
        if position not in plate_wells[well].keys():
            plate_wells[well][position] = {}
            plate_wells[well][position][channel] = [file]
        else:
            if channel not in plate_wells[well][position].keys():
                plate_wells[well][position][channel] = [file]
            else:
                plate_wells[well][position][channel].append(file)

# steps through each well in the dictionary. Creates a directory named for the
# well and changes the working directory to the new well directory
for plate_well in plate_wells.keys():
    print("~~~~~{}~~~~~".format(plate_well))
    try:
        mkdir(plate_well)
    except:
        pass
    well_path = join(path,plate_well)

    # Steps through each position in the well. Creates a directory for the Position
    # and changes the working directory to the directory
    for position in plate_wells[plate_well].keys():
        chdir(well_path)
        try:
            mkdir(position)
        except:
            pass
        pos_path = join(well_path, position)
        chdir(path)

        # Steps through the channels at the position and assigns the image prefix
        # image for fluorescent bead images
        # phase for cell images

        for channel in plate_wells[plate_well][position].keys():
            num_images = len(plate_wells[plate_well][position][channel]) - 1
            if channel == '{}'.format(Bead_channel):
                prefix = 'image'
            elif channel == '{}'.format(Cell_channel):
                prefix = 'phase'
            else:
                prefix = 'rfp'
                num_images = len(plate_wells[plate_well][position][channel])

            # For each image in the channel list moves the file from the main
            # Folder into the folder for the well and position. Names the file
            # With the prefix and the number of the image.
            plate_wells[plate_well][position][channel].sort()
            for num,image in enumerate(plate_wells[plate_well][position][channel]):
                image_num = num + 1
                if image_num < 10:
                    image_num = "0" + str(image_num)
                else:
                    image_num = str(image_num)
                if num < num_images:
                    try:
                        rename(join(path, image), join(pos_path, '{}{}.tif'.format(prefix, image_num)))
                    except:
                        print("Error with {}".format(image))
                elif num == num_images and channel == '{}'.format(Bead_channel):
                    try:
                        rename(join(path, image), join(pos_path, 'trypsin.tif'))
                    except:
                        print("Error with {}".format(image))
