# Solution to https://www.root-me.org/en/Challenges/Cracking/ELF-x86-CrackPass?lang=en

key = 'THEPASSWORDISEASYTOCRACK'
key_bytes = list(map(ord,key))
k = list(map(ord,key))
key_bytes[0] = key_bytes[0] ^ 0xab

for i in range(1,len(key_bytes)):
    key_bytes[i] = key_bytes[i] - i
    key_bytes[i] = ( key_bytes[i] ^ key_bytes[i - 1] ) & 0xff
    key_bytes[i] = ( key_bytes[i] + key_bytes[i - 1] ) & 0xff
    key_bytes[i] = ( key_bytes[i] ^ key_bytes[i - 1] ) & 0xff
    key_bytes[i] = ( key_bytes[i] ^ key_bytes[8] ) & 0xff
    if key_bytes[i] == 0:
        key_bytes[i] = 1

key_hex = map(hex,key_bytes)
key_string = ''
for byte in key_hex:
    x = byte[2:]
    if len(x) == 2:
        key_string += x
    else:
        key_string += '0' + x 

print(key_string)
