#! /bin/bash

password="whatwhatwhat"
plaintext="alice.txt"

#paths for provided ./scrypt
providedPlaintextFile="../samples/$plaintext"
providedOutputFile="bash-providedScryptResults"
providedOutputFilePath="../../streamCipher/$providedOutputFile"

#paths for generated scrypt.py
generatedPlaintextFile="../p3/samples/$plaintext"
generatedOutputFile="bash-generatedScryptResults"


echo "Testing Stream Cipher Encryption:"
echo

cd ../p3/linux
echo "./scrypt $password $providedPlaintextFile $providedOutputFilePath"
./scrypt $password $providedPlaintextFile $providedOutputFilePath
echo

cd ../../streamCipher
echo "./scrypt $password $generatedPlaintextFile $generatedOutputFile"
./scrypt $password $generatedPlaintextFile $generatedOutputFile
echo

echo "File Differences: "
diff -c -s $generatedOutputFile $providedOutputFile
echo

echo "Object Dump differences: "
diff -c -s <(od -t xC $generatedOutputFile) <(od -t xC $providedOutputFile)
echo





