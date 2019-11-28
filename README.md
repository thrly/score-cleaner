# score-cleaner
A workflow for cleaning and editing PDF scans using GIMP and Python, ImageMagick and ghostscript

oliver thurley, november 2019

## Needed:
* ImageMagick
* Ghostscript
* GIMP
* python scripts:
  * thrly-1-png2xcf.py
	*	thrly-1-xcf2pdf.py
	  *	(both need to be loaded into GIMP plug-ins folder. OS X: `Applications/GIMP-2.10.app/Contents/Resources/lib/gimp/2.0/plug-ins/`

## Steps
* Split raw-scan PDF into separate PNG files with ImageMagick and gs:
  ```convert -density 300 raw-pages-scan.pdf [[-auto-level // can skip this]] %02d-raw-pages-scan.png```
* Load GIMP, with python scripts. Drop down from ‘thrly’ custom menu:
  * Run THRLY>1)… From directory of PNG files, convert to XCF and auto-level and add ‘background’ layer
* Ready for editing and cleaning in GIMP
* Close all files, then run THRLY>2)… to covert all XCF files to PDF pages
* Final individual PDF files can been combined in Preview (OS X) or ImageMagick
* make sure that the folders edited PDF files (the ones you want to merge) are in a folder on their own (not with the original scan PDF:
    ```gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dDownsampleMonoImages=false -dDownsampleGrayImages=false -sOutputFile=finalEditedPages-Merged.pdf *.pdf```

## NOTES:
* ensure the python scripts are correctly loaded into the GIMP filepath. [/Applications/GIMP-2.10.app/Contents/Resources/lib/gimp/2.0/plug-ins/]
* sometimes, new python scrips need to have their permissions updated to make it executable: chmod +x <filepath>

*ALTERNATIVE:* use ImageMagick to convert from XCF to PDF: `convert *.xcf %02d-edited-xcf.pdf` (the file will be massive?)


oliverthurley.co.uk
