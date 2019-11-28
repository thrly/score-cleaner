#! /usr/bin/env python

from gimpfu import *
import os
import re
#
def XCF2PDF(srcPath, tgtPath):
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
        xform = re.compile('\.xcf', re.IGNORECASE)

        # Find all of the XCF files in the list & make PDF file names
        for fname in allFileList:
            fnameLow = fname.lower()
            if fnameLow.count('.xcf') > 0:
                srcFileList.append(fname)
                tgtFileList.append(xform.sub('.pdf',fname))

        # Dictionary - source & target file names
        tgtFileDict = dict(zip(srcFileList, tgtFileList))

        # Loop on PNGs, open each & save as xcf
        for srcFile in srcFileList:
            # Don't overwrite existing, might be work in Progress
            if tgtFileDict[srcFile] not in existingList:
                # os.path.join inserts the right kind of file separator
                tgtFile = os.path.join(tgtPath, tgtFileDict[srcFile])
                srcFile = os.path.join(srcPath, srcFile)

                img = pdb.gimp_file_load(srcFile, srcFile)
                new_name = srcFile.rsplit(".",1)[0] + ".pdf"
                layer = pdb.gimp_image_merge_visible_layers(img, 0)

                pdb.gimp_file_save(img, layer, new_name, new_name)
                pdb.gimp_image_delete(img)
#
############################################################################
#
register (
    "XCF2PDF",         # Name registered in Procedure Browser
    "Convert XCF files to PDF", # Widget title
    "Convert and clean PNG files to XCF", #
    "oliver thurley",         # Author
    "oliver thurley",         # Copyright Holder
    "Nov 2019",            # Date
    "2) Import XCF to PDF (Directory)", # Menu Entry
    "",     # Image Type - No image required
    [
    ( PF_DIRNAME, "srcPath", "PNG Originals (source) Directory:", "" ),
    ( PF_DIRNAME, "tgtPath", "XCF Working (target) Directory:", "" ),
    ],
    [],
    XCF2PDF,   # Matches to name of function being defined
    menu = "<Image>/thrly"  # Menu Location
    )   # End register

main()
