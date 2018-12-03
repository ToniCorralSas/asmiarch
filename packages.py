#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
# os.system does command and if this gives error code, does not happens 
# nothing
import subprocess
# subprocess.check_output does command and if this gives error code, raises 
# subprocess.CalledProcessError exception



def applications(aur=False, gnome=False, gtk=False, qt=False):
  # for GNOME Shell Theme look "Uranus"
  # for KDE Plasma icons look "Uniform+"
  # put firetray for Linux in project folder
  pacman = ["akregator", "android-file-transfer", "ark", "artwiz-fonts", "atom", "bison", "bleachbit", "bzr", "calibre", "chromium", "cpanminus", "diffpdf", "expect", "fakechroot", "firefox", "firefox-i18n-es-es", "fish", "flashplugin", "flex", "geckodriver", "gimp", "git", "gnome-disk-utility", "gparted", "gst-libav", "gst-plugins-bad", "gst-plugins-base", "gst-plugins-base-libs", "gst-plugins-good", "gst-plugins-ugly", "gstreamer", "gvfs-mtp", "hunspell-es", "ipython", "ipython2", "kdeconnect", "kmail", "libappindicator-gtk2", "libappindicator-gtk3", "libreoffice-fresh", "libreoffice-fresh-es", "mlocate", "networkmanager-vpnc", "ntfs-3g", "numix-gtk-theme", "octave", "onboard", "openssh", "papirus-icon-theme", "pepper-flash", "python-crypto", "python-dateutil", "python-paramiko", "python-pexpect", "python-selenium", "python-setproctitle", "python-unidecode", "python2-crypto", "r", "remmina", "rhythmbox", "screenfetch", "sqlitebrowser", "sublime-text-dev", "thunderbird", "thunderbird-i18n-es-es", "tk", "virtualbox", "vlc", "wicd-gtk", "wine", "zsh", "xscreensaver"]
  pacman_gtk = ["alacarte", "transmission-gtk", "wireshark-gtk"]
  pacman_qt = ["arc-kde", "dolphin", "gwenview", "kcalc", "konsole", "latte-dock", "spectacle", "transmission-qt", "wireshark-qt"]

  # ccat
  # vbam-git only can downloaded by yaourt and now not works
  yaourt = ["cmaptools", "numix-circle-icon-theme-git", "perlconsole", "python-sshtunnel", "skypeforlinux-stable-bin", "spotify", "teamviewer", "terminator-bzr", "update-grub", "visual-studio-code-bin"]
  yaourt_gnome = ["clipit-gtk3"]
  yaourt_gtk = ["gtk-theme-arc-git", "pamac-aur"]

  if gtk:
    pacman = pacman + pacman_gtk
  if qt:
    pacman = pacman + pacman_qt
  for package in pacman:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm --needed'".format(package)
    print(command)
    subprocess.check_output(command, shell=True)

  # for perlconsole
  command = "arch-chroot /mnt /bin/bash -c 'cpanm Module::Install'"
  print(command)
  subprocess.check_output(command, shell=True)

  # for gcc / gcc-multilib, for skype
  command = 'echo -e "y\\ny\\nY" | pacman -S gcc-multilib'
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)

  # check if we are in a virtual machine, to install virtualbox guest dkms
  command = "grep -q ^flags.*\ hypervisor\ /proc/cpuinfo && " \
            'echo "This is a virtual machine'
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  if subprocess.check_output(command, shell=True) != None:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S linux-headers " \
              "--noconfirm --needed'"
    print(command)
    subprocess.check_output(command, shell=True)
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S " \
              "virtualbox-guest-dkms --noconfirm --needed'"
    print(command)
    subprocess.check_output(command, shell=True)

  if gnome:
    yaourt = yaourt + yaourt_gnome
  if gtk:
    yaourt = yaourt + yaourt_gtk
  if aur:
    for package in yaourt:
      command = 'sudo -u toni yaourt --m-arg "--skipchecksums ' \
                '--skippgpcheck" -S {} --noconfirm --needed'.format(package)
      command += "arch-chroot /mnt /bin/bash -c '{}'".format(command)
      print(command)
      subprocess.check_output(command, shell=True)
  """
  command = "rm -rf /home/toni/yaourt-tmp-toni"
  command = "arch-chroot /mnt /bin/bash -c '{}'".format(command)
  print(command)
  subprocess.check_output(command, shell=True)
  """



def budgie():
  packages = ["budgie-desktop"]
  optional_dependencies = ["gnome-backgrounds", "gnome-control-center", \
                           "gnome-screensaver", "network-manager-applet", \
                           "gnome-extra"]

  for p in packages + optional_dependencies:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm'".format(p)
    print(command)
    os.system(command)

  applications()



def cinnamon():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S cinnamon --noconfirm'"
  print(command)
  os.system(command)

  applications()



def deepin():
  packages = ["deepin", "deepin-extra"]

  for p in packages:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm'".format(p)
    print(command)
    os.system(command)

  applications()



def gnome():
  packages = ["gnome", "gnome-extra"]

  for p in packages:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm'".format(p)
    print(command)
    os.system(command)

  applications(gnome=True, gtk=True)



def i3():
  pass



def lxde():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S lxde --noconfirm'"
  print(command)
  os.system(command)



def lxqt():
  packages = ["lxqt", "lxqt-panel", "breeze-icons"]

  for p in packages:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm'".format(p)
    print(command)
    os.system(command)



def mate():
  packages = ["mate", "mate-extra"]

  for p in packages:
    command = "arch-chroot /mnt /bin/bash -c 'pacman -S {} " \
              "--noconfirm'".format(p)
    print(command)
    os.system(command)



def openbox():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S openbox --noconfirm'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S python2-xdg " \
            "--noconfirm'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'sudo -u toni mkdir -p " \
            "/home/toni/.config/openbox'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'sudo -u toni cp -p " \
            "/etc/xdg/openbox/{autostart,environment,menu.xml,rc.xml} " \
            "/home/toni/.config/openbox'"
  print(command)
  os.system(command)
  f = open("/mnt/home/toni/.xinitrc", "w")
  f.write("#!/bin/sh\n#\n# ~/.xinitrc\n#\n")
  f.write("# Executed by startx (run your window manager from here)\n\n")
  f.write("if [ -d /etc/X11/xinit/xinitrc.d ]; then\n")
  f.write("  for f in /etc/X11/xinit/xinitrc.d/*; do\n")
  f.write('    [ -x "$f" ] && . "$f"\n')
  f.write("  done\n  unset f\nfi\nexec openbox-session\n")
  f.close()



def pantheon():
  pass
  # pantheon-session-bzr
  # yauort pantheon-default-settings-bzr
  # contractor
  # yaourt gnome-settings-daemon-elementary
  # yaourt gnome-settings-daemon-ubuntu
  # yaourt elementary-dpms-helper-bzr
  # and more to see...



def plasma():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S plasma --noconfirm " \
            "--needed'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S kde-l10n-es " \
            "--noconfirm'"
  print(command)
  subprocess.check_output(command, shell=True)
  
  applications(qt=True)



def unity():
  pass
  """
  # https://github.com/chenxiaolong/Unity-for-Arch
  dependencies = ["systemd", "dbus-activation-env", "gtk2-ubuntu", \
                  "gtk3-ubuntu", "libdbusmenu-ubuntu", "ido", \
                  "libindicator", "libindicate", "libindicate-qt", \
                  "libappindicator", "unity-gtk-module", "dee-ubuntu", \
                  "libunity", "libunity-misc", "indicator-messages", \
                  "bamf-ubuntu", "libtimezonemap", \
                  "gsettings-desktop-schemas-ubuntu", \
                  "gsettings-ubuntu-schemas", \
                  "gnome-settings-daemon-ubuntu", "gnome-session-ubuntu", \
                  "gnome-screensaver-ubuntu", "unity-settings-daemon", \
                  "libgeonames", "unity-control-center", "properties-cpp", \
                  "lightdm-ubuntu", "unity-api", "appmenu-qt", \
                  "appmenu-qt5", "indicator-application", \
                  "indicator-appmenu", "indicator-datetime", \
                  "indicator-keyboard", "indicator-power", \
                  "indicator-printers", "indicator-session", \
                  "indicator-sound", "gsettings-qt", "dee-qt", \
                  "libcolumbus", "hud", "network-manager-applet-ubuntu", \
                  "overlay-scrollbar", "frame", "grail", "geis", \
                  "glew-unity", "nux", "unity-asset-pool", \
                  "nautilus-ubuntu", "zeitgeist-ubuntu", "libzeitgeist", \
                  "unity-lens-applications", "unity-lens-files", \
                  "unity-lens-music", "unity-lens-photos", \
                  "unity-lens-video", "unity-scope-home", "unity-scopes", \
                  "compiz-ubuntu", "lightdm-unity-greeter", "unity", \
                  "unity-language-packs"]
  # DO NOT WORK systemd!!!
  """



def xfce():
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S artwiz-fonts " \
            "--noconfirm'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S xfce4 --noconfirm'"
  print(command)
  os.system(command)
  command = "arch-chroot /mnt /bin/bash -c 'pacman -S xfce4-goodies " \
            "--noconfirm'"
  print(command)
  os.system(command)

  #applications(gtk=True)
