import binascii
import random


def random_rgb():
    """
Creates a randomized hex-format RGB value and returns it.
    """
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
              "D", "E", "F"
             ]
    rgb = ""
    for i in range(6):
        rgb = rgb + values[random.randint(0,15)]
    return rgb


def build_binary_string(x, y, image_data, filename):
    """
Adds bitmap-specific header data to the image data and writes the binary file.
    """
    dimensions = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]

    header = "42 4D 4C 00 00 00 00 00 00 00 1A 00 00 00 0C 00 00 00"
    width = dimensions[x] + " 00"
    height = dimensions[y] + " 00"
    header_more = "01 00 18 00"
    padding = "00 00"   # fills out to 4 bytes (8 hex string)
    bitmap = header + width + height + header_more + image_data + padding

    bitmap = bitmap.strip()
    bitmap = bitmap.replace(' ', '')
    bitmap = bitmap.replace('\n', '')
    bitmap = binascii.a2b_hex(bitmap)

    with open('%s.bmp'%filename, 'wb') as image_file:
        image_file.write(bitmap)


def new_random_bitmap(filename):
    """
Creates a random bitmap file.
    """

    random_width = random.randint(1,9)
    random_height = random.randint(1,9)

    pixel_rows = []
    for row in range(random_height):
        row_input = ""
        for pixel in range(random_width):
            new_pixel = random_rgb()
            row_input = row_input + new_pixel
        pixel_rows.append(row_input)

    image_data = ""
    for row in pixel_rows:
        image_data = image_data + row
        if (((random_width * 3) % 4) != 0):
            for i in range(4 - ((random_width * 3) % 4)):
                image_data = image_data + " 00"

    build_binary_string(random_width, random_height, image_data, filename)


def generate_random_bitmap():
    """
Generates random bitmaps up to the amount specified by the user.
    """
    number_bitmaps = input("How many random bitmaps to generate? ")
    number_bitmaps = int(number_bitmaps)

    name_counter = 1
    for i in range(number_bitmaps):
        new_random_bitmap(name_counter)
        name_counter += 1
    print("Generated %s random bitmaps."%number_bitmaps)


def generate_user_bitmap():
    """
Creates a new bitmap file using user-specified inputs.
    """

    # user inputs
    filename = input("Filename: ")
    user_width = input("Width in pixels (min 1, max 9): ")
    user_height = input("Height in pixels (min 1, max 9): ")
    user_width = int(user_width)
    user_height = int(user_height)

    print("(r)ed (g)reen (b)lue (x)black (w)hite")
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

    build_binary_string(user_width, user_height, image_data, filename)
    print("Done!")


def compress_bitmap():
    bitmap = ""
    filename = input("File to compress: ")
    with open('%s.bmp'%filename, 'rb') as image_file:
        #print(image_file.readlines())
        bitmap = image_file.readlines()[0]

    split_binary = str(bitmap).split('\\x') # remove \x in binary string
    image_data = "".join(split_binary)
    image_data = image_data[51:-5] # cut out header and EOF padding, leaving only
                                  # image_data (hard-coded for width 4 padding)


    # Organize data by pixel and row.
    data = []
    row = []
    pixel = ""
    counter_pixel = 0
    counter_row = 0
    for i in image_data:
        pixel = pixel + i
        counter_pixel += 1
        if counter_pixel == 6: # RR GG BB = one pixel
            row.append(pixel)
            pixel = ""
            counter_pixel = 0
            counter_row += 1
        if counter_row == 4: # hard-code for rows with a width of 4 pixels
            data.append(row)
            row = []
            counter_row = 0

    """
    # test data
    data = [['0c00fe', '0f00fc', '0e00f2', '0200f0'],
            ['00ff00', '00ff00', '00ff00', '00ff00'],
            ['ff0000', 'ff0000', 'ff0000', 'ff0000'],
            ['0000ff', '0000ff', '0000ff', '0000ff']
           ]
    """

    can_compress = True
    compressed = []
    for r in data:
        can_compress = True
        for p in r: # for pixel in row
            if ((p[0] != r[0][0]) or (p[2] != r[0][2]) or (p[4] != r[0][4])):
                can_compress = False # if R, G, and B values are all same base 16,
        if can_compress == True: # then make all the same as the first pixel RGB
            new_row = ["4" + r[0]] # hard-coded multiplier
            compressed.append(new_row)
        else:
            compressed.append(r) # append original row if any difference

    compressed = str(compressed)
    with open('compressed.txt', 'w') as compressed_file:
        compressed_file.write(compressed)

    print("Bitmap compressed.") # 'compressed' image data


def decompress_bitmap():
    # Currently only proof-of-concept. Difficulty in reading from txt file.
    data = [['40000ff'], ['400ff00'], ['4ff0000'], ['40000ff']] # test data

    decompressed_bitmap = ""
    multiplier = ""
    for row in data:
        if len(row) == 1:
            x = row[0][0]
            multipler = int(x)
            for i in range(multipler): # expand to row width
                decompressed_bitmap = decompressed_bitmap + row[0][1:]
        else:
            for pixel in row:
                decompressed_bitmap = decompressed_bitmap + pixel
    build_binary_string(4, 4, decompressed_bitmap, "decompress_test") # hard-coded test data

    print("Bitmap decompressed.")


def print_menu():
    print("MENU  - Prints menu options.")
    print("NEW   - Create a new user-defined bitmap.")
    print("RAND  - Create random bitmaps.")
    print("COM   - Compress an existing bitmap.")
    print("DECOM - Decompress a bitmap. (TEST DATA ONLY)")


def user_interface():
    menu_list = {
        "MENU": print_menu, "COM": compress_bitmap, "DECOM": decompress_bitmap,
        "NEW": generate_user_bitmap, "RAND": generate_random_bitmap
        }
    print("Please choose an operation:")
    print("MENU")
    run_program = True
    while run_program is True:
        user_response = input("Input: ")
        user_response = user_response.upper()
        if user_response in menu_list:
            menu_list[user_response]()
        elif user_response in ["EXIT", "QUIT"]:
            print("Goodbye.")
            run_program = False
        else:
            print("Not a valid command.")

user_interface()
