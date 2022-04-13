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
message="file.txt"

#paths for ./vencrypt
provKeyPath="../samples/$key"
provMsgPath="../samples/$message"
provOutputFile="bash-Encrypt-Provided.txt"
provOutputPath="../../vignere/$provOutputFile"

#paths for vencrypt.py
genKeyPath="../p3/samples/$key"
genMsgPath="../p3/samples/$message"
genOutputFile="bash-Encrypt-Generated.txt"

echo "Testing Vignere Encryption.."
echo
cd ../p3/linux
echo "Provided Vignere Encryption:"
echo "./vencrypt $provKeyPath $provMsgPath $provOutputPath"
./vencrypt $provKeyPath $provMsgPath $provOutputPath
echo

cd ../../vignere
echo "Personal Vignere Encryption:"
echo "./vencrypt $genKeyPath $genMsgPath $genOutputFile"
./vencrypt $genKeyPath $genMsgPath $genOutputFile
echo

echo "diff between file output:"
echo "diff -c -s -q $provOutputFile $genOutputFile"
diff -c -s -q $provOutputFile $genOutputFile
echo

echo "diff between object dumps of file output:"
echo "diff -c -s -q <(od -t xC $provOutputFile) <(od -t xC $genOutputFile)"
diff -c -s -q <(od -t xC $provOutputFile) <(od -t xC $genOutputFile)

