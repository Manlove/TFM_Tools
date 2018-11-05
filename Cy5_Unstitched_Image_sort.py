from os import chdir, listdir, mkdir, rename
from os.path import isfile, join

path = 'E:\\Annie\\181023_114147_Annie_TFM_10-23-18_Plate-1\\181023_175144_Plate 2 - Copy'
chdir(path)
dir_list = [f for f in listdir(path) if isfile(join(path, f))]

wells = {}
for i,j in enumerate(dir_list):
    parts = j.split('_')
    if parts[0] not in wells.keys():
        wells[parts[0]] = {}
        wells[parts[0]][parts[3]] = {}
        wells[parts[0]][parts[3]][parts[2]] = [j]
    else:
        if parts[3] not in wells[parts[0]].keys():
            wells[parts[0]][parts[3]] = {}
            wells[parts[0]][parts[3]][parts[2]] = [j]
        else:
            if parts[2] not in wells[parts[0]][parts[3]].keys():
                wells[parts[0]][parts[3]][parts[2]] = [j]
            else:
                wells[parts[0]][parts[3]][parts[2]].append(j)
                
for i,well in enumerate(wells.keys()):
    try:
        mkdir(well)
    except:
        pass
    well_path = join(path,well)

    for position in wells[well].keys():
        chdir(well_path)
        try:
            mkdir(position)
        except:
            pass
        pos_path = join(well_path, position)
        chdir(path)

        for channel in wells[well][position].keys():
            if channel == '1':
                sub = 'image0'
                num_images = len(wells[well][position][channel]) - 1
            else:
                sub = 'phase0'
                num_images = len(wells[well][position][channel])
                
            for num,image in enumerate(wells[well][position][channel]):
                if num < num_images:
                    rename(join(path, image), join(pos_path, '{}{}.tif'.format(sub, num+1)))
                else:
                    rename(join(path, image), join(pos_path, 'trypsin.tif'))





    
# 0     1    2        3        4      5
#well-read-channel-position-channel-time.tiff
