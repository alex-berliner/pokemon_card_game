BASE=/home/alex/Code/pokecards
while true; do 
    if netstat -an | grep 8000 | grep LISTEN; then 
        break 
    fi
done
cd $BASE/nfc/py/pokemon/core/
python showdown_interface_svc.py