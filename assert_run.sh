#!/bin/bash
cp -TR val_tests/ tests/val_tests/
source .venv/bin/activate
temp_execution_file="kos.txt"
./run.sh > ${temp_execution_file}
final_score="$(grep  -Eo '^[0-9]+$' ${temp_execution_file} | tail -1)"
rm ${temp_execution_file}
if [ ${final_score} -eq 4 ]
then
    echo Success
    exit 0
else
    echo Failure
    exit -1
fi
rm -r tests/val_tests/