cp -TRv val_tests/ tests/val_tests/
source .venv/bin/activate
./run.sh > kos.txt
final_score="$(grep  -Eo '^[0-9]+$' kos.txt | tail -1)"
rm kos.txt
if [ ${final_score} -eq 4 ]
then
    echo Success
else
    echo Failure
fi
rm -r tests/val_tests/