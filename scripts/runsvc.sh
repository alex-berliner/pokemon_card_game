while true; do
    if netstat -an | grep 8000 | grep LISTEN; then
        break
    fi
done

if [ -z ${VIRTUAL_ENV} ]; then
    cd $PCO_BASE
    . .pco/bin/activate
fi

cd $PCO_BASE/nfc/py/pokemon/core/
python showdown_interface_svc.py
