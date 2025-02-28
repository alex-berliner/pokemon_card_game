if [ -z ${VIRTUAL_ENV} ]; then
    cd $PCO_BASE
    . .pco/bin/activate
fi

cd $PCO_BASE/nfc/py/pokemon/core/
python hardware_abstraction_svc.py
