from os import chdir, listdir, mkdir, rename
from os.path import isfile, join

path = 'E:\\Annie\\181023_114147_Annie_TFM_10-23-18_Plate-1\\181023_175144_Plate 2 - Copy'
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
    filename = i.split('_')
    well = filename[0]
    position = filename[3]
    channel = filename[2]
    if well not in plate_wells.keys():
        plate_wells[well] = {}
        plate_wells[well][position] = {}
        plate_wells[well][position][channel] = [i]
    else:
        if position not in plate_wells[well].keys():
            plate_wells[well][position] = {}
            plate_wells[well][position][channel] = [i]
        else:
            if channel not in plate_wells[well][position].keys():
                plate_wells[well][position][channel] = [i]
            else:
                plate_wells[well][position][channel].append(i)

# steps through each well in the dictionary. Creates a directory named for the
# well and changes the working directory to the new well directory
for plate_well in plate_wells.keys():
    try:
        mkdir(well)
    except:
        pass
    well_path = join(path,well)

    # Steps through each position in the well. Creates a directory for the Position
    # and changes the working directory to the directory
    for position in plate_wells[well].keys():
        chdir(well_path)
        try:
            mkdir(position)
        except:
            pass
        pos_path = join(well_path, position)
        chdir(path)

        # Steps through the channels at the position and assigns the image prefix
        # image0 for GFP bead images
        # phase0 for brightfield cell images
        for channel in plate_wells[well][position].keys():
            if channel == '1':
                sub = 'image0'
                num_images = len(plate_wells[well][position][channel]) - 1
            else:
                sub = 'phase0'
                num_images = len(plate_wells[well][position][channel])

            # For each image in the channel list moves the file from the main
            # Folder into the folder for the well and position. Names the file
            # With the prefix and the number of the image.
            for num,image in enumerate(plate_wells[well][position][channel]):
                if num < num_images:
                    rename(join(path, image), join(pos_path, '{}{}.tif'.format(sub, num+1)))
                else:
                    rename(join(path, image), join(pos_path, 'trypsin.tif'))






# 0     1    2        3        4      5
#well-read-channel-position-channel-time.tiff
