BASE=/home/alex/Code/pokecards
cd $BASE
. .pcenv/bin/activate

SD_SERV_ID="pk_sd"
HW_ABS_SVC_ID="hwab"
SDINT="sdint"

(tmux kill-session -t $SD_SERV_ID) || true
(tmux kill-session -t $HW_ABS_SVC_ID) || true
(tmux kill-session -t $SDINT) || true

# netstat -an | grep 8000 | grep LISTEN

# start showdown server
tmux new-session -d -s $SD_SERV_ID "cd $BASE/pokemon/pokemon-showdown; node pokemon-showdown start --no-security"

# start hw abstraction
tmux new-session -d -s $HW_ABS_SVC_ID "cd $BASE/nfc/py/pokemon/core/; python hardware_abstraction_svc.py "

# start showdown connector
tmux new-session -d -s $SDINT "./runsvc.sh"
