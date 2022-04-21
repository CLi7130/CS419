import hashlib
import os
from os.path import exists
import sys
import time
import string
from itertools import product

# Program will:
# 1. create a SHA-256 has of specified file
# 2. Convert it to printable hex string( matching string produced by the openssl command)
#       - call openssl and use diff to make sure?
# 3. pick a string that's a potential proof of work value.
# 4. Create a hash of the string representation of the hash in (2) concatenated with the potential proof of work string in (3)
#       - M = Message
#       - W = potential proof of work
#       - hash(M || W) = hashed value
# 5. If the hashed value generated in (4) doesn't start with at least nbits zero bits (number supplied by first argument of command line)
#       then go back to step 3 and try with a different suffix
#   Output:
# - print to standard output in header format
# - one name-value item per line wtih each line containing header name, a colon, one or more spaces, and the value.
# - header item shall not span multiple lines, output shall not contain blank lines

# Headers to be produced:
# File:
#       - name of the file
# Initial-hash:
#       - The SHA-256 hash of the file (as a printable hex value)
# Proof-of-work:
#       - The printable string that is your proof of work
# Hash:
#       - the SHA-256 hash of the orginal string concatenated with the proof of work
# Leading-zero-bits:
#       - the actual number of leading 0 bits in the hash you computed. This value should be greater than or equal
#           to the number requested
# Iterations:
#       - the number of different proof-of-work values you have to try before you found one that works
# Compute Time:
#       - How long this process took, in seconds (including decimal seconds if appropriate)

# keep proof-of-work as 7 bit printable ASCII text (no extended characters, so they can be present in headers)
# don't use quotes as part of string either

DEBUG = 0

# globals that we can use later for printing
FILE_HASH_VAL = 0
ITERATIONS = 0
PROOF_OF_WORK = bytearray()
FINAL_HASH = bytearray()
ACTUAL_LEADING_ZERO_BITS = 0
REQUESTED_LEADING_ZERO_BITS = 0
COMPUTE_TIME = 0
VALID_CHAR_ARRAY = []

# if we reach one billion iterations, we've been running too long
ITERATION_UPPER_BOUND = 1000000000

# encodes a given byte array from a file with SHA-256, and returns a hash object of the byte array
def getHashValHexDigest(inputFile):

    # SHA-256 Hash Value
    hashVal = hashlib.sha256(inputFile)
    # String representation of hash value in hex
    hashValHexDigest = hashVal.hexdigest()
    hashValDigest = hashVal.digest()
    if DEBUG:
        print()
        print("hashValDigest:", hashValDigest)
        print("hashValHexDigest:", hashValHexDigest)
        print()
    
    return hashValHexDigest

# tests given proof of work against required leading zero bits
# if constraints are satisfied, set globals and return true
def testProofOfWork(suffix):
    global ACTUAL_LEADING_ZERO_BITS, ITERATIONS, PROOF_OF_WORK, FINAL_HASH

    # each time we test a different proof of work, add an iteration to the global
    ITERATIONS = ITERATIONS + 1
    if ITERATIONS == ITERATION_UPPER_BOUND:
        # probably shouldn't get to this many iterations, kill program
        print("[Error] Runtime is too long")
        exit()

    leadingZeros = 0
    nonZeroVal = 0
    combinedHash = getHashValHexDigest( (FILE_HASH_VAL + suffix).encode('utf-8') )
    if DEBUG:
        print()
        print("Initial Hash:", FILE_HASH_VAL)
        print("Proof of Work:", suffix)
        print("Combined Hash:", combinedHash)

    # iterate over every hex value in hash
    for hexChar in combinedHash:
        #convert to byte value - base 16, truncate first 2 chars of hex byte value
        binValue = bin(int(hexChar, 16))[2:].zfill(4)

        if DEBUG:
            print()
            print("Hex Value:", hexChar)
            print("Binary of Hex Value:", binValue)
        
        # parse binary value until we reach a non zero value
        # keep count of leading zeros
        for num in binValue:
            if num.isdigit() and int(num) == 0:
                leadingZeros = leadingZeros + 1
            else:
                nonZeroVal = 1
                break
        if nonZeroVal == 1:
            break

    if DEBUG:
        print()
        print("leadingZeros:", leadingZeros)

    # satisfied leading zeros constraint, this is a valid proof of work
    if leadingZeros >= REQUESTED_LEADING_ZERO_BITS:
        ACTUAL_LEADING_ZERO_BITS = leadingZeros
        PROOF_OF_WORK = suffix
        FINAL_HASH = combinedHash
        return True

    # invalid proof of work, go to next value
    return False

# https://docs.python.org/3/library/itertools.html
# https://docs.python.org/3/library/itertools.html#itertools.product
def generateProofOfWork():

    # we're limited to a 7 bit ASCII text, so iterate from 1 char to 7 chars
    for num in range(1, 8):     

        # this creates a list of the cartesian product of all valid chars for a given length
        cartesianProduct = list(product(VALID_CHAR_ARRAY, repeat=num))
        for tuple in cartesianProduct:

            # generate usable string from tuples
            suffix = ''.join(tuple)
            # actual answers are verified/stored in testProofOfWork Function
            retVal = testProofOfWork(suffix)

            # found valid proof of work, go back to main
            if retVal is True:
                return

# creates array of all possible printable characters in ASCII
# except quotations and whitespace
def createValidCharArr():
    global VALID_CHAR_ARRAY
    validChars = []
    invalidChars = []
    for char in string.whitespace:
        invalidChars.append(char)
    
    # 34 = " char, 39 = ' char
    invalidChars.append(chr(34))
    invalidChars.append(chr(39))

    for char in string.printable:
        if char not in invalidChars:
            validChars.append(char)

    VALID_CHAR_ARRAY = validChars

def main():

    # error handling
    if len(sys.argv) != 3 or sys.argv[1] == "" or sys.argv[2] == "":
        print("[Error] Invalid Number of Arguments")
        exit()

    numBits = sys.argv[1]
    inputFile = sys.argv[2]
    
    if (not numBits.isdigit()) or int(numBits) < 0:
        print("[Error] Please put a positive integer value for nbits")
        exit()
    
    if (not os.path.exists(inputFile)) or (os.path.getsize(inputFile) == 0):
        print("[Error] Invalid/Empty File")
        exit()

    global FILE_HASH_VAL, COMPUTE_TIME, REQUESTED_LEADING_ZERO_BITS

    REQUESTED_LEADING_ZERO_BITS = int(numBits)
    createValidCharArr()

    #start timer after error handling
    timeStart = time.perf_counter()

    # do all error handling before this point
    #  - empty files
    #   - file does not exist
    #   - non-numeric arg for numBits
    #   - negative value for numBits
    #   - file size of 0
    #   - 

    if DEBUG:
        print("numBits:", numBits)
        print("File Path:", inputFile)

    readInput = open(inputFile, "rb").read()

    if DEBUG:
        print("Read From File:", readInput)
    
    FILE_HASH_VAL = getHashValHexDigest(readInput)
    generateProofOfWork()

    #this needs to go at end of program, before things get printed
    timeEnd = time.perf_counter()
    COMPUTE_TIME = timeEnd - timeStart

    # print headers at end of program
    print("File:", inputFile)
    print("Initial-hash:", FILE_HASH_VAL)
    print("Proof-of-work:", PROOF_OF_WORK)
    print("Hash:", FINAL_HASH)
    print("Leading-zero-bits:", ACTUAL_LEADING_ZERO_BITS)
    print("Iterations:", ITERATIONS)
    print("Compute-time:", COMPUTE_TIME)

if __name__ == "__main__":
    main()