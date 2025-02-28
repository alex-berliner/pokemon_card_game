. scripts/default_vars.sh

if [ ! -d "$PCO_BASE" ]; then
    echo "\$PCO_BASE=$PCO_BASE does not exist"
    echo "Set \$PCO_BASE to base directory"
fi

(tmux kill-session -t $PCO_SD_SERV_ID) || true
(tmux kill-session -t $PCO_HW_ABS_SVC_ID) || true
(tmux kill-session -t $PCO_SDINT) || true
