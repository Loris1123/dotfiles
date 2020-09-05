# Keyboard Layout
Make umlauts with auo keys and map the lvl3 switch to capslock

    sudo localectl set-x11-keymap us pc105 de_se_fi lv3:caps_switch

# Touchpad Settings
Use xinput to set the touchpad properties. First get the ID of touchpad with `xinput --list`.
Available properties with `xinput --list-probs <ID>`

    xinput --set-prop <ID> "libinput Tapping Enabled" 1
    xinput --set-prop <ID> "libinput Natural Scrolling Enabled" 1


