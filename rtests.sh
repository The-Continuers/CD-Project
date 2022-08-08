#!/bin/bash
echo "start"
date
scores=(4 3 5 2 4 3 3 3 5 2 3 3 7 5 4 5 5 3 4 2 3)
mkdir -p out
mkdir -p report
cd ./tests
prefix="" ;
score=0;
dirlist=(`ls`) ;
subtasks=("${dirlist[@]}")
subtasks=$dirlist
OUTPUT_DIRECTORY="out/"
TEST_DIRECTORY="tests/"
REPORT_DIRECTORY="report/"
FAILED_TESTS=()

cd ../
for folder in ${dirlist[*]}
do
	NUMBER_OF_PASSED=0
	NUMBER_OF_FAILED=0
	echo "Subtask $folder -------------------------------------"
	cd ./out
	mkdir -p $folder
	cd ../report
	mkdir -p $folder
	cd ..
	cd ./tests
	cd $folder
	testlist=(`ls ${prefix}*.d`);
	cd ../../
	for filelist in ${testlist[*]}
	do
		filename=`echo $filelist | cut -d'.' -f1`;
		output_filename="$filename.out"
		output_asm="$filename.s"
		program_input="$filename.in"
		report_filename="$filename.report.txt"
		echo "Running Test $filename -------------------------------------"
		if command -v python3; then
			python3 main.py -i "$folder/$filelist" -o "$folder/$output_asm"
		else
			python main.py -i "$folder/$filelist" -o "$folder/$output_asm"
		fi
		if [ $? -eq 0 ]; then
			echo "MIPS Generated Successfuly!"
		spim -a -f "$OUTPUT_DIRECTORY$folder/$output_asm" < "$TEST_DIRECTORY$folder/$program_input" > "$OUTPUT_DIRECTORY$folder/$output_filename"
		if [ $? -eq 0 ]; then
			echo "Code Executed Successfuly!"
			if command -v python3; then
				python3 comp.py -a "$OUTPUT_DIRECTORY$folder/$output_filename" -b "$TEST_DIRECTORY$folder/$output_filename" -o "$REPORT_DIRECTORY$folder/$report_filename"
			else
				python comp.py -a "$OUTPUT_DIRECTORY$folder/$output_filename" -b "$TEST_DIRECTORY$folder/$output_filename" -o "$REPORT_DIRECTORY$folder/$report_filename"
			fi
			if [[ $? = 0 ]]; then
				((NUMBER_OF_PASSED++))
				echo "++++ test passed"
			else
				((NUMBER_OF_FAILED++))
				FAILED_TESTS+=("$folder/$filename")
				echo "---- test failed !"
			echo
			fi
			fi
		else
			echo "Code did not execute successfuly!"
			FAILED_TESTS+=("$folder/$filename")
			((NUMBER_OF_FAILED++))
		fi

	done

	echo "Passed : $NUMBER_OF_PASSED"
	echo "Failed : $NUMBER_OF_FAILED"

	echo "Subtask score: "
	len=${#subtasks[@]}
	for (( i=0; i<$len; i++ ))
	do
		if [[ "${subtasks[$i]}" == "$folder" ]]; then
			subtask_score=$(( ${scores[$i]} * $NUMBER_OF_PASSED/($NUMBER_OF_PASSED + $NUMBER_OF_FAILED) ));
			echo $subtask_score;
			(( score+= ${scores[$i]} * $NUMBER_OF_PASSED/($NUMBER_OF_PASSED + $NUMBER_OF_FAILED) ));
		fi
	done


	echo "Subtask $folder done ------------------------------"
	echo $'\n\n'


done

echo "Failed Tests:"
echo ${FAILED_TESTS[*]}

echo "Final score: "
echo "$score"

echo "finish"
date
