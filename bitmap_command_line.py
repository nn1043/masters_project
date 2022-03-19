import binascii


def new_bitmap():
    """
Creates a new bitmap file.
    """

    # user inputs
    filename = input("Filename: ")
    print("From the bottom...")
    row1 = input("First row: ")
    row2 = input("Second row: ")
    row3 = input("Third row: ")
    row4 = input("Fourth row: ")
    pixel_rows = [row1, row2, row3, row4]

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
# i could let user manually type (FF FF FF) each pixel, not really sure what
# the use is.

    # build hex string
    header = "42 4D 4C 00 00 00 00 00 00 00 1A 00 00 00 0C 00 00 00"
    width = "04 00" # use a list ['00', '01', ... '09'] and convert string to int,
    height = "04 00"    # then use an index to grab proper header
    header_more = "01 00 18 00"
    padding = "00 00"   # fills out to 4 bytes (8 hex string)
    bitmap = header + width + height + header_more + image_data + padding

    # clean bitmap hex
    bitmap = bitmap.strip()
    bitmap = bitmap.replace(' ', '')
    bitmap = bitmap.replace('\n', '')
    bitmap = binascii.a2b_hex(bitmap)

    # write to user-define file
    with open('%s'%filename, 'wb') as image_file:
        image_file.write(bitmap)

    print("Done!\n")


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


new_bitmap()
