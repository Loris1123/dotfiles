#!/bin/sh
/usr/bin/xset s 300 5
XSECURELOCK_NO_COMPOSITE=1 XSECURELOCK_LIST_VIDEOS_COMMAND="ls ~/.dotfiles/screensaver.webm" XSECURELOCK_SAVER=saver_mpv XSECURELOCK_DISCARD_FIRST_KEYPRESS=0 /usr/bin/xss-lock -n /usr/lib/xsecurelock/dimmer -l -- /usr/bin/xsecurelock &
/usr/bin/nm-applet &
/usr/bin/pasystray &
/usr/bin/picom &
/usr/bin/dunst &
