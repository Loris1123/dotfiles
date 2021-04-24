# Keyboard Layout
Make umlauts with auo keys and map the lvl3 switch to capslock

    sudo localectl set-x11-keymap us pc105 de_se_fi lv3:caps_switch
    # Or with setxkbmap
    setxkbmap -model pc105 -layout us -variant de_se_fi -option lv3:caps_switch

## Use section symbol
Edit file `/usr/share/X11/xkb/symbols/us`. In section de_se_fi, replace the following line:

    //key <AC02> {[ s,            S,          ssharp,     U1E9E      ]};
    key <AC02> {[ s,            S,          ssharp,     section      ]};

# Touchpad Settings
Use xinput to set the touchpad properties. First get the ID of touchpad with `xinput --list`.
Available properties with `xinput --list-probs <ID>`

    xinput --set-prop <ID> "libinput Tapping Enabled" 1
    xinput --set-prop <ID> "libinput Natural Scrolling Enabled" 1


