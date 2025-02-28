. scripts/default_vars.sh

if [ ! -d "$PCO_BASE" ]; then
    echo "\$PCO_BASE=$PCO_BASE does not exist"
    echo "Set \$PCO_BASE to base directory"
fi

scripts/stop_game.sh

# start showdown server
tmux new-session -d -s $PCO_SD_SERV_ID "scripts/start_showdown_srv.sh"

# start hw abstraction
tmux new-session -d -s $PCO_HW_ABS_SVC_ID "scripts/start_hw_abstr.sh"

# start showdown connector
tmux new-session -d -s $PCO_SDINT "scripts/runsvc.sh"

echo tmux servers active
