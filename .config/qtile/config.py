# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
from Xlib import display as xdisplay
import os
import subprocess

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Screen, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
from libqtile import hook

mod = "mod4"
terminal = guess_terminal()
screens = []

################################################################################
# Helper functions
################################################################################
def get_num_monitors():
    """
    Returns the number of attached monitors. Useful for different setups with a different number of monitors
    """
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception as e:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors


def focus_empty_group():
    """
    Sets focus to a group, that has no windows
    """
    def callback(qtile):
        for name,group in qtile.groups_map.items():
            if len(group.windows) == 0:
                group.cmd_toscreen(toggle=False)
                return
    return lazy.function(callback)


def focus_screen(direction):
    """
    Sets the focus to the next or the prvious screen
    """
    def callback(qtile):
        if qtile.current_screen.index == 0 and direction == "prev":
            # Do not loop back to the previous screen, if already at first
            return

        if direction == "prev":
            qtile.cmd_to_screen(qtile.current_screen.index - 1)
            pass
        elif direction == "next":
            qtile.cmd_to_screen(qtile.current_screen.index + 1)
            pass
        else:
            logger.warning("Focus screen: Unknown direction. Only 'prev' and 'next' are allowed")

        if len(qtile.current_group.windows) == 0:
            # No windows on the focused screen. Set cursor to the middle
            subprocess.run(["xdotool", 
                "mousemove", 
                str(qtile.current_screen.x + qtile.current_screen.width / 2 ),
                str(qtile.current_screen.y + qtile.current_screen.height / 2),
                ])

    return lazy.function(callback)


################################################################################
# Setup Keybindings
################################################################################
keys = [
    # Switch between windows 
    Key([mod], "h", lazy.layout.left(),
        desc="Focus the left window"),
    Key([mod], "j", lazy.layout.down(),
        desc="Focus the window below"),
    Key([mod], "k", lazy.layout.up(),
        desc="Focus the upper window"),
    Key([mod], "l", lazy.layout.right(),
        desc="Focus the right window"),

    # Switch between screens
    Key([mod, "shift"], "h", focus_screen("prev"),
        desc="Focus previous screen"),
    Key([mod, "shift"], "l", focus_screen("next"),
        desc="Focus next screen"),

    Key([mod], "n", focus_empty_group(),
        desc="Focus an empty group"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "d", lazy.spawn("rofi -show combi -theme solarized_alternate"),
        desc="Start Rofi"), 

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "Escape", lazy.spawn("xset s activate"),
        desc="Lock screen")
]

################################################################################
# Setup Layouts
################################################################################
layouts = [
    layout.MonadTall(new_at_current=True),
    layout.Stack(num_stacks=2),
    layout.Max(),
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

################################################################################
# Setup Groups
################################################################################
groups = []
groups.append(Group("1", label="1: Term"))
groups.append(Group("2", 
    label="2: Web", 
    matches=[Match(wm_class=["firefox", "google-chrome" ])],
    layout="max",
    ))
groups.append(Group("3", label="3: Work"))
groups.append(Group("4", label="4: Work"))
groups.append(Group("5", label="5: Work"))
groups.append(Group("6", label="6: Work"))
groups.append(Group("7", label="7: Text"))
groups.append(Group("8", label="8: Chat"))
groups.append(Group("9", 
    label="9: Mail",
    matches=[Match(wm_class=["thunderbird"])],
    layout="max",
    ))
groups.append(Group("0", label="10: Office"))

for group in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], group.name, lazy.group[group.name].toscreen(toggle=False),
#        Key([mod], group.name, focus_group(group.name),
            desc="Switch to group {}".format(group.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], group.name, lazy.window.togroup(group.name),
        #     desc="move focused window to group {}".format(group.name)),
    ])

################################################################################
# Setup Screens
# Will automatically detect the number of attached monitors and add a screen for each
################################################################################
num_monitors = get_num_monitors()
for m in range(num_monitors):
    # 10 Groups are created initially. However the bar is set only to show occupied groups.
    # Consequently, <num_monitors> groups are shown. 
    # To simulate i3-like workspaces, for each screen, one group is set to be displayed.
    #groups_on_screens[str(m+1)] = (m, False)  # Groups start at index 1, screens at index 0

    screens.append(
        Screen(
            top=bar.Bar(
                [
                    widget.CurrentLayout(),
                    widget.GroupBox(hide_unused=True),
                    widget.Sep(padding=5),
                    widget.TaskList(),
                    widget.Prompt(),
                    widget.TextBox(text="Volume:"),
                    widget.Volume(),
                    widget.Systray(),
                    widget.Clock(format='%k:%M - %a %e. %b %Y'),
                    widget.QuickExit(),
                ],
             24,
           )
       )
    )



widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

################################################################################
# Autostart
################################################################################
@hook.subscribe.startup
def autostart_always():
    home = os.path.expanduser('~/.config/qtile/autostart_once.sh')
    subprocess.call([home])

@hook.subscribe.startup_once
def autostart_once():
    home = os.path.expanduser('~/.config/qtile/autostart_always.sh')
    subprocess.call([home])


################################################################################
# Configuration Variables
################################################################################
cursor_warp = True
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


