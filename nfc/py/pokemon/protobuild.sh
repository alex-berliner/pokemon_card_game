BUILDDIR=/home/alex/Code/pokecards/nfc/py/circuitpython/build/proto
PROTOPATH=/home/alex/Code/pokecards/nfc/py/pokemon/proto
mkdir -p $BUILDDIR
python -m grpc_tools.protoc \
    --proto_path=$PROTOPATH \
    --python_out=$BUILDDIR \
    --pyi_out=$BUILDDIR \
    --grpc_python_out=$BUILDDIR $PROTOPATH/pokemon_interface.proto
