with open("lorem", "rb") as file:
    # Read content and prepare for output
    content = file.read()
    out = ''
    # Loop through the content in chunks of size 3
    for i in range(0, len(content), 3):
        # Create a triplet for each iteration
        triplet = content[i:i+3]
        # Add character and continue iteration if first two bytes are 0
        if(triplet[0] == 0 and triplet[1] == 0):
            out += chr(triplet[2])
            continue
        # Prepend the first 4 bits of the length byte to the offset byte
        offset = (triplet[1] & 0b1111) << 8 | triplet[0]
        # Clear 4 bits off of length byte
        length = triplet[1] >> 4
        # Absolute position of the nearest occurrence
        absolute_pos = len(out) - offset
        # Concat the substring according to the absolute position and length as well as the character element to the output
        out += out[absolute_pos:absolute_pos + length] + chr(triplet[2])
    # Print the output to file
    with open("lorem.txt", "w") as f:
        f.write(out)