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

#assumes key/message are in p3/samples folder
key="clown.jpg"
#original text file - make sure this is the same as message var in testEncrypt.sh
plaintext="file.txt"

provSamplePath="../samples"
genSamplePath="../p3/samples"

#file that ./vencrypt outputs - make sure this is the same as message var in testEncrypt.sh
provCipherFile="bash-Encrypt-Provided.txt"
#decrypted output plaintext from ./vdecrypt
provOutputFile="bash-Decrypt-Provided.txt"

#file that vencrypt.py outputs - make sure this is the same as message var in testEncrypt.sh
genCipherFile="bash-Encrypt-Generated.txt"
#decrypted output plaintext from vdecrypt.py
genOutputFile="bash-Decrypt-Generated.txt"

#paths for ./vdecrypt
provKeyPath="$provSamplePath/$key"
provPathToVignere="../../vignere"
provCipherPath="$provPathToVignere/$provCipherFile"
provOutputPath="$provPathToVignere/$provOutputFile"

#paths for vdecrypt.py
genKeyPath=$genSamplePath/$key
genCipherPath=$genCipherFile

./testEncrypt.sh

echo
echo "---------------------------------"
echo "Running Vignere Decryption.."
echo

cd ../p3/linux
echo "Running Provided Vignere Decryption"
echo "./vdecrypt $provKeyPath $provCipherPath $provOutputPath"
./vdecrypt $provKeyPath $provCipherPath $provOutputPath
echo

cd $provPathToVignere
echo "Running Generated Vignere Decryption:"
echo "./vdecrypt $genKeyPath $genCipherPath $genOutputFile"
./vdecrypt $genKeyPath $genCipherPath $genOutputFile
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