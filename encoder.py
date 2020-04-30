def encode(data):
    """Encodes data as base64 and returns the base64 string"""
    # if data is not string get string representation 
    if type(data) != str:
        data = str(data)

    # get byte array representation
    byteArray = bytearray(data, 'utf8')

    # add padding bytes
    l = len(byteArray)
    padding = 0

    while l % 3 != 0:
        padding += 1
        byteArray.append(0)
        l += 1

    # create new bytearray for base64 encoded sequence
    b64Array = bytearray()

    # define bit masks
    mask1 = 0x03
    mask2 = 0x0F
    mask3 = 0xC0
    mask4 = 0x3F

    # process bytes in groups of three each
    for n in range(int(l/3)):
        # get slice of next three bytes
        slice = byteArray[n*3:n*3+3]

        # do some bit shifting and bit masking
        # this encodes 3 bytes into four 6-bit chunks
        b64Array.append(slice[0] >> 2) # strip the 2 LSB
        b64Array.append(((mask1 & slice[0]) << 4) | (slice[1] >> 4)) # get the 2 LSB from first byte and mask with the 4 MSB from second byte
        b64Array.append(((mask2 & slice[1]) << 2) | ((mask3 & slice[2]) >> 6)) # get the 4 LSB of the second byte and mask with the 2 MSB from third byte 
        b64Array.append(mask4 & slice[2]) # strip the 2 MSB of third byte

    # create empty string
    b64String = ''

    # calculate b64 char using ascii table
    for c in b64Array[:len(b64Array) - padding]:
        if 0 <= c <= 25:
            # A - Z
            b64String += chr(c + 65)
        elif 26 <= c <= 51:
            # a - z
            b64String += chr(c + 71)
        elif 52 <= c <= 61:
            # 0 - 9
            b64String += chr(c - 4)
        elif c == 62:
            # +
            b64String += '+'
        else:
            # /
            b64String += '/'

    # add padding character
    for _ in range(padding):
        b64String += '='

    # return base64 encoded string
    return b64String