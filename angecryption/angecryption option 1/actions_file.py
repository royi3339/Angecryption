# Royi Alishayev.

from Crypto.Cipher import AES
from zlib import crc32
import struct
from puremagic import from_file

BLOCK_SIZE_16 = 16


def combine_file_and_png(png_file, target_file, output_file):
    """
    combine 2 files (1: png, 2: any other file type) to a png file - without decryption/encryption...
    the output file can be easily open by changing his type to the proper type.

    2 files in 1 (in 1 png file...).
    """
    if from_file(png_file, mime=True).split("/")[1] == "png":
        with open(png_file, "rb") as f:
            png = f.read()
        with open(target_file, "rb") as f:
            file = f.read()
    else:
        with open(target_file, "rb") as f:
            png = f.read()
        with open(png_file, "rb") as f:
            file = f.read()

    combined_file = png[:8]

    file = wrap_of_png(file)

    combined_file += file

    combined_file += png[8:]

    with open(output_file, "wb") as opened_file:
        opened_file.write(combined_file)


def int_to_str_encoded(x):
    """
    take a int convert it to a hex with length of 8 (fills with zero)
    encoding and return it.
    """
    x = hex(x)[2:]
    if "L" in x:
        x = x[:-1]
    if len(x) % 8 != 0:
        x = x.zfill(8)

    x = x.encode()
    return x


def xor(a, b):
    """
    performing a xor between 2 string/bytes letter for each char in them.
    continue till the first one to end.
    """
    res = []
    for x, y in zip(a, b):
        if type(x) == str:
            x = ord(x)

        if type(y) == str:
            y = ord(y)

        res.append(chr(x ^ y))

    res = ''.join(res)
    res = res.encode("iso-8859-1")
    return res


def int4b(i, e='>'):
    """
    a assistance method for the "wrap_of_png" method.
    """
    assert e[0] in "<>"
    return struct.pack(e[0] + "I", i)


def wrap_of_png(data, type_=b"cOMM"):
    """
    wrapping a file according its length and data in order to allow the png to wrap it. and easily get 2 file in 1.
    """
    return b"".join([
        int4b(len(data)),
        type_,
        data,
        int4b(crc32(type_ + data) % 0x100000000)
    ])


def remove_wrapping_png_file(png_file_name, output_file_name):
    """
    get a PNG file with a hiding file inside it.
    removing the hidden file from the given PNG file.
    """
    with open(png_file_name, "rb") as opened_reading_png_file:
        png_file = opened_reading_png_file.read()

    ihdr_index = png_file.index(b"\x00\x00\x00\rIHDR") - 4  # minus 4 because of the finish wrapper

    final_png_file = png_file[16:ihdr_index]

    with open(output_file_name, "wb") as opened_writing_pdf_file:
        opened_writing_pdf_file.write(final_png_file)


def remove_hidden_file_from_png_file(png_file_name, output_file_name):
    """
    get a PNG file with a hiding file inside it.
    removing the hidden file from the given PNG file.
    """
    with open(png_file_name, "rb") as opened_reading_png_file:
        png_file = opened_reading_png_file.read()

    ihdr_index = png_file.index(b"\x00\x00\x00\rIHDR") - 4  # minus 4 because of the finish wrapper

    final_png_file = png_file[:8] + png_file[ihdr_index + 4:]

    with open(output_file_name, "wb") as opened_writing_pdf_file:
        opened_writing_pdf_file.write(final_png_file)


def encrypt_aes_cbc(msg, key, iv):
    """
    encrypt the given msg, with the given key and iv.
    encryption - AES CBC
    """
    aes = AES.new(key, AES.MODE_ECB)
    m = [msg[i:i + BLOCK_SIZE_16] for i in range(0, len(msg), BLOCK_SIZE_16)]

    r = b''
    for i in m:
        if len(i) < BLOCK_SIZE_16:
            # print("\n found i != 16\n", "length of i = ", len(i), "\ni = ", i, "\n total length=", len(msg))

            number_of_padding_at_the_end = b"\x00" * (BLOCK_SIZE_16 - len(i))

            # print("length of number_of_padding_at_the_end = ", len(number_of_padding_at_the_end))

            i = number_of_padding_at_the_end + i[0:]

        # print(iv)
        r += aes.encrypt(xor(i, iv))
        iv = r[-BLOCK_SIZE_16:]
    return r


def decrypt_aes_cbc(msg, key, iv):
    """
    decrypt the given msg, with the given key and iv.
    decryption - AES CBC
    """
    aes = AES.new(key, AES.MODE_ECB)
    m = [msg[i:i + BLOCK_SIZE_16] for i in range(0, len(msg), BLOCK_SIZE_16)]

    r = b''
    for i in m:
        if len(i) < BLOCK_SIZE_16:
            # print("\n found i != 16\n", "length of i=", len(i), "\ni= ", i, "\n total length=", len(msg))

            number_of_padding_at_the_end = b"\x00" * (BLOCK_SIZE_16 - len(i))

            # print("length of number_of_padding_at_the_end = ", len(number_of_padding_at_the_end))

            i = number_of_padding_at_the_end + i[0:]

        # print(iv)
        r += xor(iv, aes.decrypt(i))
        iv = i
    return r


def encrypt(src, out, key, iv):
    """
    encrypting a given file (src) and writing it to the given output (out).
    """
    with open(src, "rb") as opened_file_reading:
        msg = opened_file_reading.read()

    enc_msg = encrypt_aes_cbc(msg, key, iv)

    with open(out, "wb") as opened_file_writing:
        opened_file_writing.write(enc_msg)


def decrypt(src, out, key, iv):
    """
    decrypting a given file (src) and writing it to the given output (out).
    """
    with open(src, "rb") as opened_file_reading:
        msg = opened_file_reading.read()

    dec_msg = decrypt_aes_cbc(msg, key, iv)

    with open(out, "wb") as opened_file_writing:
        opened_file_writing.write(dec_msg)


def decrypt_to_png(src, out, key, iv):
    """
    decrypt a angecrypted PNG file back to a PNG file.
    """
    with open(src, "rb") as opened_file_reading:
        msg = opened_file_reading.read()

    ihdr_index = msg.index(b"\x00\x00\x00\rIHDR") - 4  # minus 4 because of the finish wrapper

    png2 = msg[16:ihdr_index]

    png2 = decrypt_aes_cbc(png2, key, iv)

    png1 = msg[:8] + msg[ihdr_index + 4:]

    png1 = wrap_of_png(png1)

    png2_ihdr_index = png2.index(b"\x00\x00\x00\rIHDR") - 4  # minus 4 because of the finish wrapper

    final_file = png2[:8] + png1 + png2[png2_ihdr_index + 4:]

    with open(out, "wb") as opened_file_writing:
        opened_file_writing.write(final_file)
    # return final_file


def decrypt_to_file(src, out, key, iv):
    """
    decrypt a angecrypted PNG file back to a any file.
    its actually decrypting from png to everything possible file type...
    """
    with open(src, "rb") as opened_file_reading:
        msg = opened_file_reading.read()

    ihdr_index = msg.index(b"\x00\x00\x00\rIHDR") - 4  # minus 4 because of the finish wrapper

    file = msg[16:ihdr_index]

    file = decrypt_aes_cbc(file, key, iv)

    file = wrap_of_png(file)

    final_file = msg[:8] + file + msg[ihdr_index + 4:]

    with open(out, "wb") as opened_file_writing:
        opened_file_writing.write(final_file)
    # return final_file


def hide_png_in_png(img1, img2, img3, key, iv):
    """
    taking 3 images file - source (png), target (png), output (png).
    encrypt and hiding the target inside the source file.
    and create a result (output) file.
    """
    with open(img1, "rb") as png_opened_file:
        src = png_opened_file.read()

    with open(img2, "rb") as pdf_opened_file:
        tar = pdf_opened_file.read()

    combined_file = src[:8]

    tar = encrypt_aes_cbc(tar, key, iv)

    tar = wrap_of_png(tar)

    combined_file += tar

    combined_file += src[8:]

    with open(img3, "wb") as opened_file:
        opened_file.write(combined_file)


def hide_file_in_png(src, tar, out, key, iv):
    """
    taking 3 files - (png), (any file we want), (png).
    encrypt and hiding any file inside the png file.
    and create a result (output png) file.

    # its actually hiding everything possible to png ...
    """
    if from_file(src, mime=True).split("/")[1] == "png":
        with open(src, "rb") as f:
            png = f.read()
        with open(tar, "rb") as f:
            file = f.read()
    else:
        with open(tar, "rb") as f:
            png = f.read()
        with open(src, "rb") as f:
            file = f.read()

    combined_file = png[:8]

    file = encrypt_aes_cbc(file, key, iv)

    file = wrap_of_png(file)

    combined_file += file

    combined_file += png[8:]

    with open(out, "wb") as opened_file:
        opened_file.write(combined_file)
