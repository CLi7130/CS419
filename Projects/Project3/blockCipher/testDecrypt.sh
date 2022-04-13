#! /bin/bash

#assumes start from vignere folder
#files:
# alice.txt
# clown.jpg
# poem.txt
# test-15.txt
# test-16.txt
# test-41.txt
# test-a.txt
# test-abc.txt
# test-null.txt

#assumes plaintext files are in p3/samples folder
password="0189723509187235q;asdioghap;oiwe"
#original text file - make sure this is the same as message var in testEncrypt.sh
plaintext="alice.txt"

provSamplePath="../samples"
genSamplePath="../p3/samples"

#file that ./sbdecrypt outputs - make sure this is the same as message var in testEncrypt.sh
provCipherFile="bash-provided-SBEncryptResults"
#decrypted output plaintext from ./sbdecrypt
provOutputFile="bash-provided-SBDecryptResults"

#file that sbdecrypt.py outputs - make sure this is the same as message var in testEncrypt.sh
genCipherFile="bash-generated-SBEncryptResults"
#decrypted output plaintext from sbdecrypt.py
genOutputFile="bash-generated-SBDecryptResults"

#paths for ./sbdecrypt
provPathToPlaintext="$provSamplePath/$plaintext"
provPathToBlockCipher="../../blockCipher"
provCipherPath="$provPathToBlockCipher/$provCipherFile"
provOutputPath="$provPathToBlockCipher/$provOutputFile"

#paths for sbdecrypt.py
genPathToPlaintext=$genSamplePath/$plaintext
genCipherPath=$genCipherFile

./testEncrypt.sh

echo "---------------------------------"
echo
echo "Running Block Cipher Decryption.."
echo

cd ../p3/linux
echo "Running Provided Block Cipher Decryption"
echo "./sbdecrypt $password $provCipherPath $provOutputPath"
./sbdecrypt $password $provCipherPath $provOutputPath
echo

cd $provPathToBlockCipher
echo "Running Generated Block Cipher Decryption:"
echo "./sbdecrypt $password $genCipherPath $genOutputFile"
./sbdecrypt $password $genCipherPath $genOutputFile
echo

echo "Diff between Provided Decryption and Original Plaintext:"
echo "diff -c -s -q $provOutputFile $genSamplePath/$plaintext"
diff -c -s -q $provOutputFile $genSamplePath/$plaintext
echo

echo "Diff between Generated Decryption and Original Plaintext:"
echo "diff -c -s -q $genOutputFile $genSamplePath/$plaintext"
diff -c -s -q $genOutputFile $genSamplePath/$plaintext
echo

echo "Diff between object dump of Generated Decryption and Provided Decryption:"
echo "diff -c -s -q <(od -t xC $genOutputFile) <(od -t xC $provOutputFile)"
diff -c -s -q <(od -t xC $genOutputFile) <(od -t xC $provOutputFile)
echo