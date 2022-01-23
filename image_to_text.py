import base64

with open("image.png", "rb") as image:
    image_64 = base64.b64encode(image.read())
    image_bits = base64.b64decode(image_64)
    image_binary = "".join(["{:08b}".format(x) for x in image_bits])
    with open("text_binary.txt", "w") as text_binary:
        new_line = 0
        for i in image_binary:
            text_binary.write(i)
            new_line += 1
            if new_line >= 8:
                text_binary.write("\n")    # can be used to compare lines of binary
                new_line = 0
    with open("text_base64.txt", "wb") as text_base64:
        text_base64.write(image_64)
