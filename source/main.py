# Importing dependencies
from os import listdir, mkdir
from os.path import isfile, isdir, join
import io
import argparse

# Parser code
parser = argparse.ArgumentParser(description='Desc: Python script to convert' +\
'from ZBSpac output to subdir in my MAST format')
parser.add_argument('o', nargs='?', default = False, 
                    help="(Optional) Specify subdirectory")
args = parser.parse_args()

# Conversion code
# INPUT: s -- full path of given subdir
# OUTPUT: error -- 0 on success, 1 on exception
def convert(s):
  # Get the folder name
  dir_name = s.split('\\')[-1]
  if not (isfile(join(s, dir_name + '.bin')) and isfile(join(s, 'script.txt'))):
    print "Invalid subdirectory (need properly named bin and script.txt"
    return 1
  
  # Check if conversion is possible
  
  # terminate_early will be True when '\x00\x00\x00SC' is in the script.txt
  terminate_early = False
  
  with io.open(join(s,'script.txt'), 'r', encoding='utf-16') as f: 
    to_process = f.readlines()
  clean = []
  for line in to_process:
    clean.append(line.encode('cp932'))
  
  # Array that will number based on contents of file
  enum_arr = ''
  ctr = 0
  for line in clean:
    ctr += 1
    if len(line.strip()) > 0:
      if 'NULL 3' in line.strip(): terminate_early = True
      enum_arr += str(ctr)
    else:
      if terminate_early: break
      ctr = 0
      enum_arr += '0'
  if len(enum_arr) == 0:
    print "Empty script.txt!"
    return 1;
  # Set up to delete first two lines of ZBSpac output
  enum_arr = '55' + enum_arr[2:]

  substring0 = clean[enum_arr.find('2')].strip()
  substring1 = clean[enum_arr.rfind('2')].strip()
  with open(join(s, dir_name + '.bin'), 'rb') as f: raw = f.read()
  count0 = raw.count(substring0)
  count1 = raw.count(substring1)
  if count0 != 1 or (count1 != 1 and not terminate_early):
    print "ERROR: Substrings appear more than once. Change script.txt or" +\
    "convert manually. \nSubstring0 appears: " + str(count0) + "\nSubstring1 " +\
    "appears: " + str(count1)
    return 1
  
  # If made it here, conversion is possible, so convert
  i0 = raw.find(substring0)
  if terminate_early:  i1 = raw[i0:].find('\x00\x00\x00') + len(raw[:i0])
  else: i1 = raw.find(substring1) + len(substring1)
  head = raw[:i0]
  tail = raw[i1:]
  path = "EDIT\\" + dir_name
  try: mkdir(path)
  except OSError:
    print (path) + ' already exists! Skipping...'
    return 1
  else:
    with open(path + '\\head.bin', 'wb') as f: f.write(head)
    with open(path + '\\tail.bin', 'wb') as f: f.write(tail)
    # Convert script to MAST format
    with open('source\\script_ex.txt', 'r') as f: 
      script = f.read()
    for i in range(len(enum_arr)):
      if enum_arr[i] != '0' and enum_arr[i] != '4' and enum_arr[i] != '5':
        script += '# ' + clean[i].strip() + '\n'
      elif enum_arr[i] == '5': pass
      else: script += clean[i].strip() + '\n'
    with open(path + '\\script.txt', 'w') as f: f.write(script)
  return 0

# If a subdir is specified only convert that subdir
if args.o:
  if convert(args.o) == 0: print "Conversion successful"
  else: print "Conversion failed!"
# Otherwise, convert all subdirectories in IN directory
else:
  sdirs = [s for s in listdir("IN") if isdir(join("IN",s))]
  for s in sdirs: convert(join('IN',s))