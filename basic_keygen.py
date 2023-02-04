# Input root-me.org for the solution.

from sys import stdin
from hashlib import sha256

userInput = stdin.read().strip()
length = len(userInput)


serialList =  [ord(userInput[i]) - i + 20 for i in range(length)]
serial = bytearray(serialList)

#with open(".m.key", "wb") as binary_file:
#    binary_file.write(serial)

print(sha256(serial).hexdigest())

