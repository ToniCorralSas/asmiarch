#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
# os.system does command and if this gives error code, does not happen 
# nothing
import re
import subprocess
# subprocess.check_output does command and if this gives error code, raises 
# subprocess.CalledProcessError exception
from packages import *
from display_managers import *
from utils import *


# check if we executing UEFI
# https://behindthecodigo.wordpress.com/2016/07/06/instalar-archlinux-con-uefi/
# https://www.youtube.com/watch?v=u5XCGu19TIs
UEFI = False



def configure_keyboard_language():
  command_list = [
    "loadkeys es", \
    "timedatectl set-ntp true", \
    '#sed -i "s/#es_ES.UTF-8/es_ES.UTF-8/g" /etc/locale.gen', \
    'sed -i "s/#es_ES ISO-8859-1/es_ES ISO-8859-1/g" /etc/locale.gen', \
    '#sed -i "s/#en_US.UTF-8/en_US.UTF-8/g" /etc/locale.gen', \
    'sed -i "s/#en_US ISO-8859-1/en_US ISO-8859-1/g" /etc/locale.gen', \
    "export LANG=es_ES.UTF-8", \
    "locale-gen"
  ]

  for command in command_list:
    print(command)
    subprocess.check_output(command, shell=True) 



def disk_partitioning():
  command_list = [
    "wipefs -a /dev/sda1", \
    "wipefs -a /dev/sda2", \
    "wipefs -a /dev/sda3", \
    "wipefs -a /dev/sda4"
  ]

  #for command in command_list:
    #print(command)
    #os.system(command)

  command = "wipefs -a /dev/sda"
  print(command)
  subprocess.check_output(command, shell=True)
  # to Ctrl+C does not have any effect
  #command = "trap '' SIGINT"
  #print(command)
  #subprocess.check_output(command, shell=True)
  # to disable this, do $ trap SIGINT
  
  # http://www.rodsbooks.com/gdisk/sgdisk-walkthrough.html
  # format /dev/sda as GPT, GUID Partition Table
  # this remove partition table from disk: erase everything in disk
  command = "sgdisk -Z /dev/sda"
  print(command)
  subprocess.check_output(command, shell=True)
  # usually first sector of disk is 2048
  command = "sgdisk -F /dev/sda | tail -1"
  print(command)
  aux = subprocess.check_output(command, shell=True)
  aux = aux[:-1]
  first_sector = int(aux)
  # recomendation size partitions:
  #"http://elblogdeliher.com/" \
  #"mi-recomendacion-para-hacer-las-particiones-para-instalar-ubuntu/"
  boot_partition_size = 1   # in GB
  num_sectors_partition = (boot_partition_size * 1024 * 1024 * 1024) / 512
  num_sectors_partition = int(num_sectors_partition)
  last_sector = first_sector + num_sectors_partition - 1
  # sgdisk do not accept decimals in partition's size indicator
  if UEFI:
    command = 'sgdisk -n 1:{}:{} -t 1:ef00 -c 1:"efi_boot" ' \
              "/dev/sda".format(first_sector, last_sector)
  else:
    command = 'sgdisk -n 1:{}:{} -t 1:ef02 -c 1:"bios_boot" ' \
              "/dev/sda".format(first_sector, last_sector)
  print(command)
  subprocess.check_output(command, shell=True)
  first_sector = last_sector + 1
  root_partition_size = 8   # in GB
  num_sectors_partition = (root_partition_size * 1024 * 1024 * 1024) / 512
  num_sectors_partition = int(num_sectors_partition)
  last_sector = first_sector + num_sectors_partition - 1
  command = 'sgdisk -n 2:{}:{} -t 2:8300 -c 2:"root" ' \
            "/dev/sda".format(first_sector, last_sector)   # 60%
  print(command)
  subprocess.check_output(command, shell=True)
  first_sector = last_sector + 1
  home_partition_size = 4   # in GB
  num_sectors_partition = (home_partition_size * 1024 * 1024 * 1024) / 512
  num_sectors_partition = int(num_sectors_partition)
  last_sector = first_sector + num_sectors_partition - 1
  # 8302 Linux /home
  command = 'sgdisk -n 3:{}:{} -t 3:8300 -c 3:"home" ' \
            "/dev/sda".format(first_sector, last_sector)   # 40%
  print(command)
  subprocess.check_output(command, shell=True)
  first_sector = last_sector + 1
  aux = subprocess.check_output("sgdisk -E /dev/sda | tail -1", shell=True)
  aux = aux[:-1]
  last_sector = int(aux)
  command = 'sgdisk -n 4:{}:{} -t 4:8200 -c 4:"linux_swap" ' \
            "/dev/sda".format(first_sector, last_sector)
  print(command)
  subprocess.check_output(command, shell=True)
  command = "fdisk -l"
  print(command)
  print(subprocess.check_output(command, shell=True).decode("utf-8"))



def enable_dhcp():
  """
  THIS ONLY WORK NOW FOR A VIRTUAL MACHINE!!!
  """
  # https://www.youtube.com/watch?v=sZrTssGN3RQ

  command = "arch-chroot /mnt /bin/bash -c 'ip link'"
  print(command)
  output = subprocess.check_output(command, shell=True).decode("utf-8")
  pattern = re.compile("\n2: (\w+):")
  res = re.search(pattern, output)
  interface = res.group(1)

  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable " \
            "dhcpcd@enp0s3.service'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable " \
            "dhcpcd.service'"
  print(command)
  subprocess.check_output(command, shell=True)



def formatting_partitions():
  command_list = [
    "mkfs.fat -F32 /dev/sda1" if UEFI else "mkfs.ext4 /dev/sda1", \
    "mkfs.ext4 /dev/sda2", \
    "mkfs.ext4 /dev/sda3", \
    "mkswap /dev/sda4 && swapon /dev/sda4"
  ]

  for command in command_list:
    print(command)
    subprocess.check_output(command, shell=True)



def generate_fstab():
  command = "genfstab -U -p /mnt >> /mnt/etc/fstab"
  print(command)
  subprocess.check_output(command, shell=True)



def graphic_driver():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S xf86-video-vesa " \
            "--noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)



def installation():
  preliminars()
  configure_keyboard_language()
  disk_partitioning()
  formatting_partitions()
  mount_partitions()
  install_base_system()
  generate_fstab()
  root_configuration()
  enable_dhcp()
  #graphic_driver()
  #xorg()
  last_steps()
  #budgie()
  #cinnamon()
  #deepin()
  #lxde()
  #lxqt()
  #gnome()
  #mate()
  #openbox()
  #plasma()
  #xfce()
  #networkmanager()
  #sddm()
  #lightdm()

  command = "umount -R /mnt"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "reboot"
  print(command)
  subprocess.check_output(command, shell=True)



def install_base_system():
  command = "pacstrap -i /mnt base base-devel --noconfirm"
  print(command)
  os.system(command)



def last_steps():
  # add Spain mirrors at top, but commented
  command = 'sed -i "7i## Spain\\n' \
            "#Server = http://osl.ugr.es/archlinux/\$repo/os/\$arch\\n" \
            "#Server = http://sunsite.rediris.es/mirror/archlinux/\$repo/" \
            'os/\$arch\\n" /etc/pacman.d/mirrorlist'
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)

  # enable archlinuxfr repository to install yaourt
  command = 'echo -e "\\n[archlinuxfr]\\nSigLevel = Never\\n' \
            'Server = http://repo.archlinux.fr/\$arch" >> /etc/pacman.conf'
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)

  # enable multilib repository
  command = "arch-chroot /mnt /bin/bash -c 'cp /etc/pacman.conf .'"
  print(command)
  subprocess.check_output(command, shell=True)
  f = open("/mnt/etc/pacman.conf", "r")
  res = open("/mnt/pacman.conf", "w")
  s = ""
  for line in f.readlines():
    s += line
  f.close()
  index = s.find("#[multilib]\n#Include = /etc/pacman.d/mirrorlist")
  len_str = len("#[multilib]\n#Include = /etc/pacman.d/mirrorlist")
  s = s[:index] + "[multilib]\nInclude = /etc/pacman.d/mirrorlist" + \
      s[index + len_str:]
  res.write(s)
  res.close()
  command = "mv pacman.conf /etc/pacman.conf"
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)

  # make alias commands for system upgrades in .bashrc
  f = open("/mnt/home/toni/.bashrc", "a")
  f.write("alias actualizar='sudo pacman -Syyu; " \
          "yaourt -Syyu'\n")
  f.write("alias actualizar_auto='sudo pacman -Syyu --noconfirm; " \
          "yay -Syyu --noconfirm'\n")
  f.write("alias huerfanos='sudo pacman -Rsdn $(pacman -Qqdt)'\n")
  f.close()

  # enable sudo for users and disable asking password in wheel users
  # "https://www.reddit.com/r/archlinux/comments/3xg3wp/" \
  # "yaourt_trying_to_authenticate_as_root_how_to/"
  """
  command = 'sed -i "s/^# %wheel ALL=(ALL) ALL/' \
            '%wheel ALL=(ALL) ALL/g" /etc/sudoers'
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)
  """
  change_string_in_file("/mnt/etc/sudoers", \
                        "# %wheel ALL=(ALL) NOPASSWD: ALL\n", \
                        "Cmnd_Alias  PACMAN = /usr/bin/pacman, " \
                        "/usr/bin/yay\n" \
                        "%wheel ALL=(ALL) NOPASSWD: PACMAN\n")

  # upgrade and update repositories
  command = "arch-chroot /mnt /bin/bash -c 'pacman -Syyu --noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)

  # install yaourt
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S git --noconfirm " \
            "--needed'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S package-query " \
            "--noconfirm --needed'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/su - toni -c '" \
            "git clone https://aur.archlinux.org/yay.git /home/toni/yay'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/su - toni -c 'cd /home/toni/yay/; " \
            "makepkg -si --noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/su - toni -c 'rm -rf /home/toni/yay/'"
  print(command)
  subprocess.check_output(command, shell=True)

  # https://wiki.archlinux.org/index.php/GRUB/EFI_examples
  if UEFI:
    command = "cp -p /boot/efi/EFI/grub/grubx64.efi " \
              "/boot/efi/EFI/Boot/bootx64.efi"
    print(command)
    subprocess.check_output(command, shell=True)



def mount_partitions():
  command_list = [
    "mkdir -p /mnt/boot/efi; " \
    "mount /dev/sda1 /mnt/boot/efi" if UEFI else "mkdir /mnt/home", \
    "mount /dev/sda2 /mnt", \
    "mkdir /mnt/home", \
    "mount /dev/sda3 /mnt/home"
  ]

  for command in command_list:
    print(command)
    os.system(command)



def networkmanager():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S networkmanager " \
            "--noconfirm --needed'"
  print(command)
  subprocess.check_output(command, shell=True)
  command = "arch-chroot /mnt /bin/bash -c 'systemctl enable NetworkManager'"
  print(command)
  subprocess.check_output(command, shell=True)



def preliminars():
  # if we mount partitions and abort installation, kernel can have problems
  # to recognize changes in /dev/sda


  # $ mount | grep sda   # to know mounted dispositives

  #https://github.com/tom5760/arch-install
  # $ umount /mnt/boot
  # $ umount /mnt
  # $ swapoff /dev/vg00/swap
  # $ vgchange -an
  # $ vgremove vg00

  #subprocess.check_output("reboot", shell=True)     # reboot system
  #subprocess.check_output("poweroff", shell=True)   # halt system

  global UEFI
  subprocess.check_output("loadkeys es", shell=True)
  print("loadkeys es")
  try:
    output = subprocess.check_output("ls /sys/firmware/efi/efivars", \
                                     shell=True)
  except (subprocess.CalledProcessError):
    print("NO UEFI")
  else:
    UEFI = True
  os.system("umount -R /dev/sda2")
  os.system("umount -R /dev/sda3")
  os.system("umount -R /mnt/home")
  os.system("umount -R /mnt")
  os.system("swapoff /dev/sda4")
  os.system("vgchange -an")
  os.system("rm -rf /mnt/home")



def root_configuration():
  command_list = [
    # configure keyboard language
    'sed -i "s/#es_ES.UTF-8/es_ES.UTF-8/g" /etc/locale.gen', \
    'sed -i "s/#es_ES ISO-8859-1/es_ES ISO-8859-1/g" /etc/locale.gen', \
    'sed -i "s/#en_US.UTF-8/en_US.UTF-8/g" /etc/locale.gen', \
    'sed -i "s/#en_US ISO-8859-1/en_US ISO-8859-1/g" /etc/locale.gen', \
    "locale-gen", \
    "echo LANG=es_ES.UTF-8 > /etc/locale.conf", \
    "export LANG=es_ES.UTF-8", \
    'echo "KEYMAP=es" > /etc/vconsole.conf'
  ]

  for aux in command_list:
    # enter in system as root
    command = "arch-chroot /mnt /bin/bash -c '{}'".format(aux)
    print(command)
    subprocess.check_output(command, shell=True)

  # configure zoneinfo and system's clock
  command = "ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime"
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  os.system(command)

  command_list = [
    # syncronize date
    "hwclock --systohc --utc", \
    # rename hostname
    'echo "archlinux" > /etc/hostname', \
    # create password
    'echo -e "root\\nroot" | passwd root', \
    # create user
    "useradd -m -g users -G storage,power,users,wheel -s /bin/bash toni", \
    'echo -e "toni\\ntoni" | passwd toni', \
    # install grub
    "pacman -S grub --noconfirm", \
    "grub-install --target=x86_64-efi --efi-directory=/boot/efi " \
    "--bootloader-id=grub --recheck" if UEFI else "grub-install " \
    "--recheck /dev/sda", \
    "grub-mkconfig -o /boot/grub/grub.cfg"
  ]

  for aux in command_list:
    command = "arch-chroot /mnt /bin/bash -c '{}'".format(aux)
    print(command)
    subprocess.check_output(command, shell=True)



def xorg():
  # --needed -> option to avoid reinstall up-to-date packages
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S xorg xorg-server "
            "--noconfirm --needed'"
  print(command)
  subprocess.check_output(command, shell=True)




if __name__ == "__main__":
  installation()
