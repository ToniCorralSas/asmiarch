#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import fileinput
import os
# os.system does command and if this gives error code, does not happens 
# nothing
import subprocess
# subprocess.check_output does command and if this gives error code, raises 
# subprocess.CalledProcessError exception



def change_string_in_file(fileToSearch, textToSearch, textToReplace):
  with fileinput.FileInput(fileToSearch, inplace=True, \
                                         backup=".bak") as file:
      for line in file:
          print(line.replace(textToSearch, textToReplace), end="")



def change_string_in_file(fileToSearch, textToSearch, textToReplace, \
                                                      count=0):
  """MAKE IT TO REPLACE ONLY FIRST OCCURENCE"""
  # "https://stackoverflow.com/questions/17140886/" \
  # "how-to-search-and-replace-text-in-a-file-using-python"
  # "https://stackoverflow.com/questions/4664850/" \
  # "find-all-occurrences-of-a-substring-in-python"
  
  name_file = fileToSearch[fileToSearch.rfind("/") + 1:]
  directory = fileToSearch[:fileToSearch.rfind("/") + 1]
  # copy file to /tmp
  command = "cp -p {} /tmp".format(fileToSearch)
  subprocess.check_output(command, shell=True)
  # open original file with read-mode
  f = open(fileToSearch, "r")
  # take all str from original file
  s = ""
  for line in f.readlines():
    s = s + line
  f.close()
  # use str.replace() method taking only first occurence
  if count == 0:
    s = s.replace(textToSearch, textToReplace)
  else:
    s = s.replace(textToSearch, textToReplace, count)
  # open file in /tmp, write string in file
  f = open("/tmp/{}".format(name_file), "w")
  f.write(s)
  f.close()
  # copy original file to .bak
  command = "cp -p {0} {0}.bak".format(fileToSearch)
  subprocess.check_output(command, shell=True)
  # mv /tmp file to original file
  command = "mv /tmp/{} {}".format(name_file, fileToSearch)
  subprocess.check_output(command, shell=True)




if __name__ == "__main__":
  pass
