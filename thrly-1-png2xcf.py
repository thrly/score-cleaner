#! /usr/bin/env python

from gimpfu import *
import os
import re
#
def PNG2XCF(srcPath, tgtPath):
    """For processing scans. Converts all of the
    PNGs in the source directory into XCF files in a target
    directory.

    Auto-levels and adds a blank 'background' layer on the way

    Requires two arguments, the paths to the source and
    target directories.  DOES NOT require an image to be open.

    a hack of Stephen Kiel's 'exampleJpgToXcf.py'
    """
    ###
    open_images, image_ids = pdb.gimp_image_list()
    if open_images > 0:
        pdb.gimp_message ("Close open Images & Rerun")
    else:
        # list all of the files in source & target directories
        allFileList = os.listdir(srcPath)
        existingList = os.listdir(tgtPath)
        srcFileList = []
        tgtFileList = []
        xform = re.compile('\.png', re.IGNORECASE)
        # Find all of the PNG files in the list & make xcf file names
        for fname in allFileList:
            fnameLow = fname.lower()
            if fnameLow.count('.png') > 0:
                srcFileList.append(fname)
                tgtFileList.append(xform.sub('.xcf',fname))
        # Dictionary - source & target file names
        tgtFileDict = dict(zip(srcFileList, tgtFileList))
        # Loop on PNGs, open each & save as xcf
        for srcFile in srcFileList:
            # Don't overwrite existing, might be work in Progress
            if tgtFileDict[srcFile] not in existingList:
                # os.path.join inserts the right kind of file separator
                tgtFile = os.path.join(tgtPath, tgtFileDict[srcFile])
                srcFile = os.path.join(srcPath, srcFile)

                theImage = pdb.file_png_load(srcFile, srcFile)
                theDrawable = theImage.active_drawable
######
                width = theImage.width # get width and height of the original image
                height = theImage.height

                #pdb.gimp_drawable_equalize(theDrawable, TRUE) #equalize is probably too extreme
                pdb.gimp_drawable_levels_stretch(theDrawable) # auto balance the levels
                theDrawable.name = "Main" #rename the main layer

                # create a new "Background" layer, add it to back, set colour to white
                bgLayer = gimp.Layer(theImage, "Background", width, height, RGB_IMAGE, 100, NORMAL_MODE)
                theImage.add_layer(bgLayer, 1)
                gimp.set_background(255,255,255)
                pdb.gimp_edit_fill(bgLayer, BACKGROUND_FILL)

                pdb.gimp_image_set_active_layer(theImage,theDrawable) # set the 'main' layer as active

######
                pdb.gimp_xcf_save(0, theImage, theDrawable, tgtFile, tgtFile)
                pdb.gimp_image_delete(theImage)
#
############################################################################
#
register (
    "PNG2XCF",         # Name registered in Procedure Browser
    "Convert and clean PNG files to XCF", # Widget title
    "Convert and clean PNG files to XCF", #
    "oliver thurley",         # Author
    "oliver thurley",         # Copyright Holder
    "Nov 2019",            # Date
    "1) Import PNG to XCF (Directory)", # Menu Entry
    "",     # Image Type - No image required
    [
    ( PF_DIRNAME, "srcPath", "PNG Originals (source) Directory:", "" ),
    ( PF_DIRNAME, "tgtPath", "XCF Working (target) Directory:", "" ),
    ],
    [],
    PNG2XCF,   # Matches to name of function being defined
    menu = "<Image>/thrly"  # Menu Location
    )   # End register

main()
