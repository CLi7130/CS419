#! /bin/bash

password="0189723509187235q;asdioghap;oiwe"
plaintext="alice.txt"

#paths for provided ./scrypt
providedPlaintextFile="../samples/$plaintext"
providedOutputFile="bash-provided-SBEncryptResults"
providedOutputFilePath="../../blockCipher/$providedOutputFile"

#paths for generated scrypt.py
generatedPlaintextFile="../p3/samples/$plaintext"
generatedOutputFile="bash-generated-SBEncryptResults"


echo "Testing Block Cipher Encryption:"
echo

cd ../p3/linux
echo "./sbencrypt $password $providedPlaintextFile $providedOutputFilePath"
./sbencrypt $password $providedPlaintextFile $providedOutputFilePath
echo

#not finished, don't run
cd ../../blockCipher
echo "./sbencrypt $password $generatedPlaintextFile $generatedOutputFile"
./sbencrypt $password $generatedPlaintextFile $generatedOutputFile
echo

echo "File Differences: "
diff -c -s $generatedOutputFile $providedOutputFile
echo

echo "Object Dump differences: "
diff -c -s <(od -t xC $generatedOutputFile) <(od -t xC $providedOutputFile)
echo





