# My scanned scores cleaning process
A workflow for cleaning and editing PDF scans using GIMP and Python, ImageMagick and ghostscript


A topic that’s probably of limited use for most people, and limited interest for even fewer: **how I batch-process scans of my scores for digital editing**.

I write all my scores by hand. Always have. I wish I could wax lyrical about Craft, or Thinking Through One’s Own Hand… but it’s a bit of a pain in the arse and, honestly, it just happens to work for the way I think and my process. I don’t think there’s anything special about handwriting over digital, it just happens to work for me. \[EDIT 2022: I've finally started to explore Dorico and move away from this...]\[EDIT 2024: I miss ink and rulers]

The workflow has been the same for years: sketch in notebooks; mock-up frameworks and structures; write the draft; rewrite the draft; ink it; scan it; digital post-processing to clean up, make tweaks and, ultimately, send it off the PDF. While it might not be the sexiest bit of the workflow, dealing with pages of scans, and cleaning them up always feels the most time-consuming. So I have some automated tricks as a workaround.

Okay, this post is really just for me to record my workflow. For some reason I keep losing the .txt file on my computer that reminds me of the command-line arguments.  I’ve recently made the move away from using Photoshop with macros. I’m now using GIMP, and I’ve got a simple little set of Python plug-ins to help automate the process. Here’s the process (files below):

## process
1. Scan the score (a single, multi-page, PDF file).
2. Split the PDF into individual PNG files (pages). 
	- This is easiest in the command-line using ImageMagick and Ghostscript: `convert -density 300 input-file.pdf %02d-output-page.png`
        - You could add an `-auto-level` call in between the input and output files to have ImageMagick handle the level balance.
	- In the past, I’ve also had a lot of luck with the pdftk server
3. Automatically balance levels of the PNG, prepare it for editing (XCF file).
        I made a GIMP-python script to do this: thrly-1-png2xcf.py
4. I do my editing/clean-up in GIMP.
5. Flatten the XCF files down to PDFs. I made another GIMP-python script to do this bit: thrly-2-xcf2pdf.py
6. Merge the individual PDF pages back into a single PDF document. This is easy: if I’m on a Mac, Preview can do it. Otherwise, Ghostscript:
	`gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dDownsampleMonoImages=false -dDownsampleGrayImages=false -sOutputFile=finalEditedPages-Merged.pdf *.pdf`
7. Done.

Pretty riveting stuff. This is always the point in the process where I swear that I’ll learn Dorico for the next piece…

## requirement:
* [ImageMagick](https://imagemagick.org/)
* [Ghostscript](https://www.ghostscript.com/)
* [GIMP](https://www.gimp.org/)
* python scripts:
  * [thrly-1-png2xcf.py](https://github.com/thrly/score-cleaner/blob/master/thrly-1-png2xcf.py)
  * [thrly-2-xcf2pdf.py](https://github.com/thrly/score-cleaner/blob/master/thrly-2-xcf2pdf.py)
  	* (both need to be loaded into GIMP plug-ins folder. 
		* OS X: `Applications/GIMP-2.10.app/Contents/Resources/lib/gimp/2.0/plug-ins/`
		* Windows: `Program Files\GIMP 2\lib\gimp\2.0\plug-ins\`

## steps (alt)
* Split raw-scan PDF into separate PNG files with ImageMagick and gs:
  ```convert -density 300 raw-pages-scan.pdf [[-auto-level // can skip this]] %02d-raw-pages-scan.png```
* Load GIMP, with python scripts. Drop down from ‘thrly’ custom menu:
  * Run THRLY>1)… From directory of PNG files, convert to XCF and auto-level and add ‘background’ layer
* Ready for editing and cleaning in GIMP
* Close all files, then run THRLY>2)… to covert all XCF files to PDF pages
* Final individual PDF files can been combined in Preview (OS X) or ImageMagick
* make sure that the folders edited PDF files (the ones you want to merge) are in a folder on their own (not with the original scan PDF:
    ```gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dDownsampleMonoImages=false -dDownsampleGrayImages=false -sOutputFile=finalEditedPages-Merged.pdf *.pdf```

## notes:
* ensure the python scripts are correctly loaded into the GIMP filepath
* sometimes new python scrips need to have their permissions updated to make it executable: `chmod +x <filepath>`

## alternative option:
use ImageMagick to convert from XCF to PDF: `convert *.xcf %02d-edited-xcf.pdf` (the file will be massive?)

_oliverthurley.co.uk
oliver thurley, november 2019_
