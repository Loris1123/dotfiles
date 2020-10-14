#i3-msg workspace $(($(i3-msg -t get_workspaces | tr , '\n' | grep '"num":' | cut -d : -f 2 | sort -rn | head -1) + 1))

workspaces=$(i3-msg -t get_workspaces | tr , '\n' | grep '"num":' | cut -d : -f 2 | sort)

NEW_WS_INDEX=1

echo $workspaces | grep -q '\b'$NEW_WS_INDEX'\b'

while [ $? -eq 0 ]; do
	NEW_WS_INDEX=$(( $NEW_WS_INDEX + 1 ))
	echo $workspaces | grep -q '\b'$NEW_WS_INDEX'\b'
done

i3-msg workspace $NEW_WS_INDEX Work

