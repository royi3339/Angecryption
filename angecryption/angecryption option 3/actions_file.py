# Royi Alishayev.

from Crypto.Cipher import AES
from zlib import crc32
from puremagic import from_file

BLOCK_SIZE_16 = 16


def remove_a_hidden_file_from_a_given_file(file, index_of_start, index_of_end):
    """
    get a file with a hiding file inside it.
    removing the hidden file from the given file.
    """
    final_file = file[index_of_start:index_of_end]
    return final_file


def remove_hidden_file_from_pdf_file(pdf_file_name, output_file_name):
    """
    get a PDF file with a hiding file inside it.
    removing the hidden file from the given PDF file.
    """
    with open(pdf_file_name, "rb") as opened_reading_pdf_file:
        pdf_file = opened_reading_pdf_file.read()

    pdf_index = pdf_file.index(b"%PDF")
    # print("PDF_index = ", pdf_index)

    eof_index = pdf_file.index(b"%%EOF") + 6
    # print("EOF_index = ", eof_index - 6)

    # print("total length = ", len(pdf_file), "\n\n\n")

    # taking only the part with the PDF file, in order to remove the hidden file from the given PDF file.
    final_pdf_file = remove_a_hidden_file_from_a_given_file(pdf_file, pdf_index, eof_index)

    with open(output_file_name, "wb") as opened_writing_pdf_file:
        opened_writing_pdf_file.write(final_pdf_file)


def remove_hidden_file_from_png_file(png_file_name, output_file_name):
    """
    get a PNG file with a hiding file inside it.
    removing the hidden file from the given PNG file.
    """
    with open(png_file_name, "rb") as opened_reading_png_file:
        png_file = opened_reading_png_file.read()

    png_index = png_file.index(b"PNG") - 1
    # print("PNG_index = ", png_index)

    iend_index = png_file.index(b"IEND") + 8
    # print("IEND_index = ", iend_index - 8)

    # print("total length = ", len(png_file), "\n\n\n")

    # taking only the part with the PNG file, in order to remove the hidden file from the given PNG file.
    final_png_file = remove_a_hidden_file_from_a_given_file(png_file, png_index, iend_index)

    with open(output_file_name, "wb") as opened_writing_pdf_file:
        opened_writing_pdf_file.write(final_png_file)


def encrypt(msg, iv, key):
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


def decrypt(msg, iv, key):
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

    # print("length of r before = ", len(r))
    return r


def decrypt_to_png(msg, iv, key):
    """
    decrypt (actually encrypt) a angecrypted file back to a PNG file.
    """
    res_of_decrypt = encrypt(msg, iv, key)

    png_index = res_of_decrypt.index(b"PNG") - 1
    # print("png_index = ", png_index)

    iend_index = res_of_decrypt.index(b"IEND")
    # print("iend_index = ", iend_index)

    # print("total length = ", len(res_of_decrypt), "\n\n\n")

    # swapping the order of the encrypted file part with the PNG file, in order to make the file valid.
    final_res = res_of_decrypt[png_index:iend_index + 8]
    final_res += res_of_decrypt[0:png_index]

    return final_res


def decrypt_to_pdf(msg, iv, key):
    """
    decrypt (actually encrypt) a angecrypted file back to a PDF file
    """
    res_of_decrypt = encrypt(msg, iv, key)

    pdf_index = res_of_decrypt.index(b"%PDF")
    # print("pdf_index = ", pdf_index)

    eof_index = res_of_decrypt.index(b"%%EOF")
    # print("eof_index = ", eof_index)

    # print("total length = ", len(res_of_decrypt), "\n\n\n")

    # swapping the order of the encrypted file part with the PDF file, in order to make the file valid.
    final_res = res_of_decrypt[pdf_index:eof_index + 6]
    final_res += res_of_decrypt[0:pdf_index]

    return final_res


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


def hide_png_in_png(img1, img2, img3, key, iv):
    """
    taking 3 images file - source (png), target (png), output (png).
    encrypt (actually decrypt) and hiding the target inside the source file.
    and create a result (output) file.
    """
    with open(img1, "rb") as f:
        source = f.read()
    with open(img2, "rb") as f:
        target = f.read()

    source += b"\x00" * (BLOCK_SIZE_16 - len(source) % BLOCK_SIZE_16) * (len(source) % BLOCK_SIZE_16 != 0)

    print("IV: ", iv)

    source = encrypt(source, iv, key)
    source += int_to_str_encoded(crc32(source[12:]) % (1 << 32)) + target[0:]
    source += b"\x00" * (BLOCK_SIZE_16 - len(source) % BLOCK_SIZE_16) * (len(source) % BLOCK_SIZE_16 != 0)
    with open(img3, "wb") as f:
        f.write(decrypt(source, iv, key))


def hide_png_in_pdf(src, tar, out, key, iv):
    """
    taking 3 files - (pdf), (png), (pdf).
    encrypt (actually decrypt) and hiding the png file inside the pdf file.
    and create a result (output pdf) file.
    """
    if from_file(src, mime=True).split("/")[1] == "pdf":
        with open(src, "rb") as f:
            pdf = f.read()
        with open(tar, "rb") as f:
            img = f.read()
    else:
        with open(tar, "rb") as f:
            pdf = f.read()
        with open(src, "rb") as f:
            img = f.read()

    pdf += b"\x00" * (BLOCK_SIZE_16 - len(pdf) % BLOCK_SIZE_16) * (len(pdf) % BLOCK_SIZE_16 != 0)

    print("IV: ", iv)

    pdf = encrypt(pdf, iv, key)
    pdf += img
    pdf += b"\x00" * (BLOCK_SIZE_16 - len(pdf) % BLOCK_SIZE_16) * (len(pdf) % BLOCK_SIZE_16 != 0)
    with open(out, "wb") as f:
        f.write(decrypt(pdf, iv, key))


def hide_pdf_in_png(src, tar, out, key, iv):
    """
    taking 3 files - (png), (pdf), (png).
    encrypt (actually decrypt) and hiding the pdf file inside the png file.
    and create a result (output png) file.
    """
    if from_file(src, mime=True).split("/")[1] == "png":
        with open(src, "rb") as f:
            img = f.read()
        with open(tar, "rb") as f:
            pdf = f.read()
    else:
        with open(tar, "rb") as f:
            img = f.read()
        with open(src, "rb") as f:
            pdf = f.read()

    img += b"\x00" * (BLOCK_SIZE_16 - len(img) % BLOCK_SIZE_16) * (len(img) % BLOCK_SIZE_16 != 0)

    print("IV: ", iv)

    img = encrypt(img, iv, key)
    img += pdf
    img += b"\x00" * (BLOCK_SIZE_16 - len(img) % BLOCK_SIZE_16) * (len(img) % BLOCK_SIZE_16 != 0)

    with open(out, "wb") as f:
        f.write(decrypt(img, iv, key))
