# Solution to https://www.root-me.org/en/Challenges/Cracking/ELF-x86-No-software-breakpoints

# Left rotate and right rotate functions are hardcoded for 32 bit values. change the value 32 to whichever int size you want, or better yet, make it a variable.
def leftRotate32(value: int, rotate: int) -> int:
    return  ((value << rotate) % 0xffffffff) | (value >> (32 - rotate))

def rightRotate32(value: int, rotate: int) -> int:
    return ((value >> rotate) | (value << (32 - rotate)) % 0xffffffff) 

def initializeStream(section: list) -> list: 
    """Takes the .text section values as a list and performes the algorithm which produces a sort of keystream."""
    bitStream = 0
    for byte in section:
        bitStream = (bitStream & 0xffffff00) + (bitStream + byte & 0xff) # Add to the lower byte of bitStream without any overflow to the upper bytes.
        bitStream = leftRotate32(bitStream, 3)
    return bitStream

def decryptPassword(encryptedPassword: list, byteStream: int) -> list:
    """With the stream generated from initializeStream the encrypted password string"""
    index = 0x19
    password = []
    while index > 0:
        byteStream = rightRotate32(byteStream, 1)
        encryptedByte = encryptedPassword[index - 1]
        streamByte = byteStream & 0xff              # zero out all bytes except the smallest.
        password.append(encryptedByte ^ streamByte)
        index -= 1
    return reversed(password)

    

if __name__ == '__main__':
    from lief import ELF

    binary = ELF.parse('ch20.bin')

    textSectionAddress = 0x8048080 # The starting address of the .text section.
    address_of_encrypted_password = 0x8049155 # An address to where the encrypted password is stored in the .data section. 
    textSectionContent = binary.get_content_from_virtual_address(textSectionAddress, 0xa3) # Parse the .text section.
    dataSectionContent = binary.get_content_from_virtual_address(address_of_encrypted_password, 0x19) # Parse the encrypted password from .data.

    stream = initializeStream(textSectionContent) # Calculate the keystream from the .text section.
    password = decryptPassword(dataSectionContent, stream) # Use the above mentioned keystream to decrypt the password.

    print(''.join(list(map(chr,password)))) # Print stuff

