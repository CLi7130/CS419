#! /bin/bash

#make sure these are the same as testScrypt.sh
password="whatwhatwhat"
plaintext="alice.txt"

pathToSamples="../p3/samples"

#input
providedCipherText="bash-providedScryptResults"
generatedCipherText="bash-generatedScryptResults"

#output
provPlaintext="bash-rev-provScryptPlaintext"
genPlaintext="bash-rev-genScryptPlaintext"

#paths for ./scrypt
provCipherPath="../../streamCipher/$providedCipherText"
provPlaintextPath="../../streamCipher/$provPlaintext"

#paths for scrypt.py
genCipherPath=$generatedCipherText
genPlaintextPath=$genPlaintext


./testScrypt.sh
echo "-----------------------"
echo "Testing Stream Cipher Decryption"
echo

cd ../p3/linux
echo "./scrypt $password $provCipherPath $provPlaintextPath"
./scrypt $password $provCipherPath $provPlaintextPath
echo

cd ../../streamCipher
echo "./scrypt $password $genCipherPath $genPlaintextPath"
./scrypt $password $genCipherPath $genPlaintextPath
echo

echo "Generated/Provided File Differences: "
echo "diff -c -s -q $provPlaintext $genPlaintext"
diff -c -s -q $provPlaintext $genPlaintext
echo

echo "Generated/Provided Object Dump differences: "
echo "diff -c -s -q <(od -t xC $provPlaintext) <(od -t xC $genPlaintext)"
diff -c -s -q <(od -t xC $provPlaintext) <(od -t xC $genPlaintext)
echo

echo "Original Plaintext and Generated File Differences:"
echo "diff -c -s -q $genPlaintext $pathToSamples/$plaintext"
diff -c -s -q $genPlaintext $pathToSamples/$plaintext
echo

echo "Differences in Object Dump between Generated File and Original Plaintext:"
echo "diff -c -s -q <(od -t xC $genPlaintext) <(od -t xC $pathToSamples/$plaintext)"
diff -c -s -q <(od -t xC $genPlaintext) <(od -t xC $pathToSamples/$plaintext)
echo




