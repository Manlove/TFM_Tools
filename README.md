# TFM_Tools
Scripts for facilitating traction force microscopy work flow with images
produced with a Biotek Cytation 5 and processed with TractionsForAll (http://tractionsforall.wixsite.com/tractionsforall-blog/about).


Cy5_Unstitched_Image_sort
  (Used for preprocessing of traction force images before analysis with TractionsForAll)

  Takes an imaging folder with the raw, un-stitched cytation5 image files and sorts
  the files into corresponding well and position folders while renaming the files
  with the names required by TractionsForAll.
  TractionsForAll requires brightfield or fluorescent images of cells to be
  labeled phase01, phase02, ..., phase10 and so on while the fluorescent images of beads
  are labeled image01, image02, ... , image10.

  ~ Notes Before Running ~
    The success of this script will depend on the run parameters for the traction
    force experiment that was run. While I tried to make the script as universal
    as I could for the experiments that we were running, variations in the run protocol
    may create problems for the sorting.

    I would recommend copying a subset of the files to a new directory for testing
    before running the script on a full experiment.

  ~ To Use ~
    Users must provide a path to the directory containing their images along with
    the channel number for both the bead and cell images.

    path = '' <- give the path to the directory
    Bead_channel = '2' <- enter the number for the bead channel
    Cell_channel = '1' <- enter the number for the cell channel

    Image files from the Cytation 5 are labeled in the following way:
      well-read-channel-position-channel-time.tiff
    The first channel is the number while the second has a verbal description
    of the channel. Make sure to use the number.

  ~ Output ~
    Once this script has run, the imaging files in the main folder will have been
    renamed and moved to a set of subdirectories. Nothing should output to the
    command line unless a problem was encountered.


TFM_data_consolidation
  (Used to collect data from the individual TractionForAll analysis runs)

  When TractionForAll is used to analyze traction force experiments it creates
  subdirectories for the cropped files, displacements and tractions with the
  final tractions data in an excel sheet in the tractions folder.

  TFM_data_consolidation was created to retrieve the data from those subdirectories
  and collect them into individual well excel files along with a summary file for
  the plate.

  ~ Notes Before Running ~
    This script was built for the distinct purpose of collecting data from files
    produced by the TractionForAll analysis done on cells split into subdirectories
    by Cy5_Unstitched_Image_sort. Usage of the script to retrieve data that was
    produced by a work flow that does not include those distinct steps my not succeed.

  ~ To Use ~ 
    Users must provide the number of time points that were run during the traction
    force experiment including the baseline point but not including the trypsin
    time point. This can be identified by the number of phase**.tiff images in
    one of the position subfolders. Once run the script will ask the user to
    identify the directory that contains the sorted image files. This directory
    should include all well subdirectories.

  ~ Output ~
    Once the script has run each well folder will have an excel sheet with the
    data from the positions that contained tractions.xlsx files. There will also
    be a summary file in the main directory.

    While the script runs it will print the well that is currently being collected
    to the command line and will print the well and position for any position
    directory that does not contain a tractions.xlsx file.
