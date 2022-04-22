#! /bin/bash


# README
#
# assumes you are in a directory that has the folder "p4-samples", containing the subdirirectories "headerfiles" 
# and "testfiles" respectively (this is the sample download from the writeup).
#
# assumes you have your executables in the same directory as "p4-samples"
#
# assumes you've already changed your program to an executable (IE - you can run your program with ./pow-create)
#
# be sure to run chmod +rwx testValidCreateCheck.sh prior to attempting to run this program, as well as on your executables
#
# program can be run by the command ./testValidCreateCheck.sh

# program tests pow-create for the files in the sample folder at nbits of values [1, 5, 10, 15, 20] (this array can be edited),
# writing their values to the respective files. pow-check is then run on each of these files.
# all of the output files are contained in a folder "bash-outputFiles"

# number of nbits required/difficulty for each test
# apparently we're only being tested on up to 20 nbits, Compute-time must be less than one minute for 20 nbits.
nbits=(1 5 10 15 20)

# paths to folders containing samples
headerfilesPath="./p4-samples/headerfiles"
testfilesPath="./p4-samples/testfiles"
outputFolder="bash-outputFiles"
outputFolderPath="./$outputFolder"


: '
if [ ! -d "$outputFolder" ]
    then
        mkdir "$outputFolder"
fi



for f in "$testfilesPath"/*;
do
    # sanity check that all files exist/is a regular file
    if [ -f "$f" ]
        then
            echo
            echo "Processing $f"
            for i in ${nbits[@]}; do
                echo "./pow-create $i $f"
                ./pow-create $i $f > "$outputFolderPath/bash-$i-$(basename ${f}.txt)"
            done

        else
            echo "Warning: Problem with File \"$f\""
    fi
done
'
count=0
for f in "$outputFolderPath"/*;
do
    # sanity check that all files exist/is a regular file
    if [ -f "$f" ]
        then
            echo
            echo "Processing $f"

            # editing generated bash filename so that we can get the original filename
            file=${f##*/}
            base=${file%%.txt}
            base=${base//[[:digit:]]}
            originalFilename=${base:6}
            pathToOriginalFile="$testfilesPath/$originalFilename"

            echo "./pow-check $f $pathToOriginalFile"
            ./pow-check $f $pathToOriginalFile
            output=$(./pow-check $f $pathToOriginalFile)
            
            status= $output | tail -c 5
            echo "status: $status"

            echo $output



            pass="pass"
            fail="fail"
            if [[ "$status" == "$pass" ]]
            then
                echo "passed test"
                count=$((count+1))
            else
                echo "failed test for $f"
            fi
            

        else
            echo "Warning: Problem with File \"$f\""
    fi
done

echo "$count/30 tests passed"

# ./pow-check ./bash-outputFiles/bash-10-abc.txt ./bash-outputFiles/./bash-outputFiles/bash-10-abc.txt.txt