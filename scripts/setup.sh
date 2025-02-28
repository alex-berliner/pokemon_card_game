# set -euo
echo asd
. scripts/default_vars.sh

if [ ! -d "$PCO_BASE" ]; then
    echo "\$PCO_BASE=$PCO_BASE does not exist"
    echo "Set \$PCO_BASE to base directory"
fi

cd $PCO_BASE

# deactivate || true

rm -rf .pco
python -m venv .pco
. .pco/bin/activate
pip install -r requirements.txt

./scripts/protobuild.sh
