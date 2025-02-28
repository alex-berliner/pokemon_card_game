. scripts/default_vars.sh

if [ ! -d "$PCO_BASE" ]; then
    echo "\$PCO_BASE=$PCO_BASE does not exist"
    echo "Set \$PCO_BASE to base directory"
fi

BUILDDIR=$PCO_BASE/nfc/py/pokemon/build/proto
PROTOPATH=$PCO_BASE/nfc/py/pokemon/proto
mkdir -p $BUILDDIR
python -m grpc_tools.protoc \
    --proto_path=$PROTOPATH \
    --python_out=$BUILDDIR \
    --pyi_out=$BUILDDIR \
    --grpc_python_out=$BUILDDIR $PROTOPATH/pokemon_interface.proto
