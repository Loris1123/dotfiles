#!/bin/sh
# Move a complete desktop to the next/previous monitor.

# Because we have dynamic desktops, it must first be checked if there is another desktop on the current monitor. If not, create a new one with the next empty number.
if [ "$(bspc query -D -m | wc -l)" = "1" ]; then
	bspc monitor $(bspc query -M -m) -a $($HOME/.config/bspwm/new_desktop.py)
fi

desk=`bspc query -D -d focused`;
if [ "$1" = "next" ]; then
    bspc desktop -m next
    bspc monitor -f next
else 
    bspc desktop -m prev
    bspc monitor -f prev
fi
bspc desktop -f $desk

# Cleanup empty desktops
$HOME/.config/bspwm/dynamic_desktops.sh --c 1
