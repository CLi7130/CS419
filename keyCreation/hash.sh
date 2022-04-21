#!/bin/bash

#writes all possible hashed values of password into hashed.txt based on choices given


compareStrings () {
    if [ "$1" == "$2" ]; then
        echo "match" >> hashed.txt
    fi
}


givenPass="\$6\$RvCA3xDS\$yVf9acc1kBgvIFnUzDsc/z262MjYho6dmdYDb3iyUuTVh7a6B0e/9LSbMWgVqYg29GUs3h2zJPreo2jhcUMpu."
echo "Alice's Password:" > hashed.txt
echo $givenPass >> hashed.txt
echo >> hashed.txt


echo "1234567" >> hashed.txt
openssl passwd -6 -salt RvCA3xDS 1234567 >> hashed.txt
$tempPass=`openssl passwd -6 -salt RvCA3xDS 1234567`
#compareStrings "$givenPass" "$tempPass"
echo >> hashed.txt

echo "sunshine" >> hashed.txt
openssl passwd -6 -salt RvCA3xDS sunshine >> hashed.txt
$tempPass=`openssl passwd -6 -salt RvCA3xDS sunshine`
#compareStrings "$givenPass" "$tempPass"
echo >> hashed.txt

echo "password1" >> hashed.txt
openssl passwd -6 -salt RvCA3xDS password1 >> hashed.txt
$tempPass=`openssl passwd -6 -salt RvCA3xDS password1`
#compareStrings "$givenPass" "$tempPass"
echo >> hashed.txt

echo "qwerty123" >> hashed.txt
openssl passwd -6 -salt RvCA3xDS qwerty123 >> hashed.txt
$tempPass=`openssl passwd -6 -salt RvCA3xDS qwerty123`
#compareStrings "$givenPass" "$tempPass"
echo >> hashed.txt

#https://www.youtube.com/watch?v=LJ5nV9aKthU
echo "letmein" >> hashed.txt
openssl passwd -6 -salt RvCA3xDS letmein >> hashed.txt
$tempPass=`openssl passwd -6 -salt RvCA3xDS letmein`
#compareStrings "$givenPass" "$tempPass"

echo "Nine10ofSpades" >> hashed2.txt
openssl passwd -6 -salt saltPassword Nine10ofSpades >> hashed2.txt
