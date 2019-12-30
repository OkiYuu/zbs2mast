This is a python-2.7-based program set up to convert the scripts from ZBSpac to subdirectories
in the same format as my MAST (MajiKoi A Script Translator) project

The Google archive for ZBSpac can be found at https://code.google.com/archive/p/zbspac/,
which was in turn based off of crass by jzhang0 and exchpac by asmodean. 

This program assumes that the first and last ripped lines from the given script are unique
strings in the given subdirectory.

USAGE: Put a subdirectory in the IN folder with original .bin folder and ZBSpac script.txt,
and run the supplied .bat file. If successful, this will make a new subdirectory in EDIT in
the same format as the subdirectories made from MAST.

EXAMPLE SUBDIRECTORY FOR .\IN\
m1_1007_0 (directory must be named after the .bin involved!)
  >script.txt (ZBSpac output)
  >m1_1007_0.bin (original raw .bin file)


DEFAULT FOLDER STRUCTURE:
ROOT FOLDER
  >IN
    >>SUBDIRECTORIES TO TRANSFER TO MAST FORMAT
  >EDIT
    >>OUTPUTTED SUBDIRECTORIES IN MAST FORMAT
  >source
    >>main.py (python 2.7 source file this program)
    >>main.exe (compiled code to run without python needed on host OS)
    >>script_ex.txt (example block to put at top of outputted script.txt)
  >README.txt (this file)
  >zbs2mast.bat (file to run this program)
