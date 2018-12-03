#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
# os.system does command and if this gives error code, does not happens 
# nothing
import subprocess
# subprocess.check_output does command and if this gives error code, raises 
# subprocess.CalledProcessError exception



def lightdm():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S " \
            "lightdm-gtk-greeter --noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S " \
            "lightdm-gtk-greeter-settings --noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable " \
            "lightdm.service'"
  print(command)
  subprocess.check_output(command, shell=True)



def sddm():
  # additional fonts
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S ttf-freefont " \
            "--noconfirm --needed'"
  print(command)
  subprocess.check_output(command, shell=True)

  command = "arch-chroot /mnt /bin/bash -c 'pacman -S sddm --noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable sddm'"
  print(command)
  subprocess.check_output(command, shell=True)
  
  # modify Xsetup file from sddm to use spanish keyboard 
  command = '''arch-chroot /mnt /bin/bash -c "echo 'setxkbmap \"es\"' ''' \
            '>> /usr/share/sddm/scripts/Xsetup"'
  print(command)
  subprocess.check_output(command, shell=True)



def slim():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S slim --noconfirm'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable slim.service'"
  print(command)
  os.system(command)




if __name__ == "__main__":
  pass
