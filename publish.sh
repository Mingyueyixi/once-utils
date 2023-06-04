result=$(pip list |grep 'twine')
if [ -z "$result" ]
then
  pip install twine
fi
python -m twine upload dist/*.tar.gz