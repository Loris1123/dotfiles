#!/bin/sh

# Kill running instances
killall -q polybar
while pgrep -u $UID -x polybar > /dev/null; do sleep 1; done

if type "xrandr"; then
  for m in $(/usr/bin/xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m /usr/bin/polybar --reload main 2>/dev/null &
  done
else
  /usr/bin/polybar --reload main &
fi
