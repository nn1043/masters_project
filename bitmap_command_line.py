import binascii


def new_bitmap():
    """
Creates a new bitmap file.
    """

    # user inputs
    filename = input("Filename: ")
    user_width = input("Width in pixels (min 1, max 9): ")
    user_height = input("Height in pixels (min 1, max 9): ")
    user_width = int(user_width)
    user_height = int(user_height)

    print("From the bottom...")
    pixel_rows = []
    for row in range(user_height):
        row_input = input("Pixels: ")
        pixel_rows.append(row_input)

    # convert user input to hex
    image_data = ""
    for row in pixel_rows:
        for pixel in row:
            if pixel == "r":
                image_data = image_data + "00 00 FF"    # red
            elif pixel == "g":
                image_data = image_data + "00 FF 00"    # green
            elif pixel == "b":
                image_data = image_data + "FF 00 00"    # blue
            elif pixel == "x":
                image_data = image_data + "00 00 00"    # black
            elif pixel == "w":
                image_data = image_data + "FF FF FF"    # white
            else:
                image_data = image_data + "00 00 00"    # error handler
        if (((user_width * 3) % 4) != 0):
            for i in range(4 - ((user_width * 3) % 4)):
                image_data = image_data + " 00"
# i could let user manually type (FF FF FF) each pixel, not really sure what
# the use is.

    # build hex string
    dimensions = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
        # offset index 0, no other error checking

                    # file size here. need change?
    header = "42 4D 4C 00 00 00 00 00 00 00 1A 00 00 00 0C 00 00 00"
    width = dimensions[user_width] + " 00"
    height = dimensions[user_height] + " 00"
    header_more = "01 00 18 00"
    padding = "00 00"   # fills out to 4 bytes (8 hex string)
    bitmap = header + width + height + header_more + image_data + padding

    # clean bitmap hex
    bitmap = bitmap.strip()
    bitmap = bitmap.replace(' ', '')
    bitmap = bitmap.replace('\n', '')
    bitmap = binascii.a2b_hex(bitmap)

    # write to user-define file
    with open('%s.bmp'%filename, 'wb') as image_file:
        image_file.write(bitmap)

    print("Done!\n")


new_bitmap()

"""
Breaking down the data:

(1 byte = 2 hex string)
header = "42 4D 4C 00 00 00 00 00 00 00 1A 00 00 00 0C 00 00 00"
42 4D - Specifies bitmap file type.
4C 00 00 00 00 00 00 00 - File size in bytes.
1A 00 - Reserved for use by image processing application.
00 00 - Reserved for use by image processing application.
0C 00 00 00 - Number of bytes from start of file (42) through first byte of
    pixel data.

width = "04 00" - Little endian system (04 00 rather than 00 04), width in
    pixels. Up to 4 bytes.
height = "04 00" - Little endian system, height in pixels. Up to 4 bytes.

header_more = "01 00 18 00"
01 - Number of color planes of target device (should be 1).
00 - Compression (none, so 0).
18 - Size of color pallet.
00 - Number of important colors (usually 0).

(image data) - RGB '00 00 00' format per pixel. The bitmap scans the image from
    the bottom row inputted up.
red - 00 00 FF
green - 00 FF 00
blue - FF 00 00
black - 00 00 00
white - FF FF FF

padding = "00 00" - fills out to 4 bytes (8 hex string)

"""
