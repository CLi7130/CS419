import argparse

#alice:$6$RvCA3xDS$yVf9acc1kBgvIFnUzDsc/z262MjYho6dmdYDb3iyUuTVh7a6B0e/9LSbMWgVqYg29GUs3h2zJPreo2jhcUMpu.:18565:0:99999:7:::

#separated by ':' character:

#1. username: alice
#2. hashed password: $6$RvCA3xDS$yVf9acc1kBgvIFnUzDsc/z262MjYho6dmdYDb3iyUuTVh7a6B0e/9LSbMWgVqYg29GUs3h2zJPreo2jhcUMpu.
    # separated by $:
    # $6
        # $6 means that SHA-512 is being used
    # $RvCA3xDS
        # RvCA3xDS is the salt value
    # yVf9acc1kBgvIFnUzDsc/z262MjYho6dmdYDb3iyUuTVh7a6B0e/9LSbMWgVqYg29GUs3h2zJPreo2jhcUMpu.
        # Above is the hash value of the salt + user password

#3. days since UNIX time that password was changed: 18565
#4. specifies number of days required between password changes: 0
#5. Number of days after which you are required to change the password: 99999
#6. Number of days before the required password change that user gets a warning: 7

#7. Not used - (if a password is expired, account will be disabled after this many days)
#8. not used - (number of days from teh unix time, account will be disabled)

def publicKeyGen(primeNum, alphaGen, privateKey):
    #public key formula: Yi = ((alphaGen)^(privateKey)) mod primeNum

    publicKey = ((alphaGen)**(privateKey)) % primeNum

    return publicKey

def commonKeyGen(pubKey, privKey, prime):

    key = ((pubKey)**(privKey)) % prime

    return key

def main():

    primeNumber = 45099
    rootGenerator = 23777
    alicePrivateKey = 5983
    alicePublicKey = 36719
    bobPrivateKey = 2880
    bobPublicKey = 36334

    # formula for common key:
    # K = (bob's public key)^(alive's private key) mod primeNumber

    print("Prime Number: " + str(primeNumber))
    print("root (alpha): " + str(rootGenerator))
    print("----------------------")
    print("Alice's Private Key: " + str(alicePrivateKey))
    print("Alice's Public Key: " + str(alicePublicKey))
    print("----------------------")
    print("Bob's Private Key: Unknown") #+ str(bobPrivateKey))
    print("Bob's Public Key: " + str(bobPublicKey))

    print("bob test public key = " + str(publicKeyGen(primeNumber, rootGenerator, bobPrivateKey)))

    key1 = commonKeyGen(bobPublicKey, alicePrivateKey, primeNumber)
    key2 = commonKeyGen(alicePublicKey, bobPrivateKey, primeNumber)
    #key1 = ((bobPublicKey)**(alicePrivateKey)) % primeNumber
    #key2 = ((alicePublicKey)**(bobPrivateKey)) % primeNumber

    print()
    print("Formula: K = Yb^(Xa) mod(p)")
    print("K1 = (bob's public key)^(Alice's private key) mod primeNumber")
    print("K1 = " + str(key1))

    print()
    print("Formula: K = Ya^(Xb) mod(p)")
    print("K2 = (Alice's Public Key)^(Bob's Private Key) mod primeNumber")
    print("K2 = " + str(key2))
    
    if(key1 == key2):
        print("Keys are equal, common key is: " + str(key1))
    else:
        print("Keys are not equal: ")
        print("Key1 = " + str(key1))
        print("Key2 = " + str(key2))
    return


if __name__ == "__main__":
    main()