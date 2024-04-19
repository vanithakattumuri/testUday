rm -rf ./sphinx/*
cd sphinx
sphinx-quickstart
cp ../conf.py .
cd ..
sphinx-apidoc -o sphinx PAMI
cp index.rst ./sphinx
cd sphinx
make html


