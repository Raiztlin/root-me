# Soon to be solution to https://www.root-me.org/en/Challenges/Cracking/ELF-x86-No-software-breakpoints


def leftRotate32(value, rotate): 
    return  ((value << rotate) % 0xffffffff) | (value >> (32 - rotate))

def rightRotate32(value, rotate):
    return ((value >> rotate) | (value << (32 - rotate)) % 0xffffffff) 

def initializeStream(section):
    bitStream = 0
    for byte in section:
        bitStream += byte
        leftRotate32(bitStream, 3)
    return bitStream

if __name__ == '__main__':
    from lief import ELF

    binary = ELF.parse('ch20.bin')
    textSection = binary.get_section('.text')
    #size = textSection.size

    stream = initializeStream(textSection.content)
    print(stream)
