#!/bin/sh
xset s 300 5
XSECURELOCK_DISCARD_FIRST_KEYPRESS=0 xss-lock -n /usr/lib/xsecurelock/dimmer -l -- xsecurelock &
nm-applet &
pasystray &
compton &
