#!/bin/sh
xset s 300 5
XSECURELOCK_NO_COMPOSITE=1 XSECURELOCK_LIST_VIDEOS_COMMAND="ls ~/.dotfiles/screensaver.webm" XSECURELOCK_SAVER=saver_mpv XSECURELOCK_DISCARD_FIRST_KEYPRESS=0 xss-lock -n /usr/lib/xsecurelock/dimmer -l -- xsecurelock &
nm-applet &
pasystray &
compton &
