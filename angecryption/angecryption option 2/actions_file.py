# Royi Alishayev - Optimized & Fixed Version

from Crypto.Cipher import AES
from zlib import crc32
from puremagic import from_file

BLOCK_SIZE_16 = 16
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def pad_zero(data):
    """משלים את המידע לכפולה של 16 בייטים על ידי הוספת אפסים בסוף"""
    remainder = len(data) % BLOCK_SIZE_16
    if remainder != 0:
        return data + b"\x00" * (BLOCK_SIZE_16 - remainder)
    return data


def remove_a_hidden_file_from_a_given_file(file, index_of_start, index_of_end):
    """חילוץ חלק ספציפי מתוך הקובץ"""
    return file[index_of_start:index_of_end]


def remove_hidden_file_from_pdf_file(pdf_file_name, output_file_name):
    """מסיר קובץ מוסתר מתוך קובץ PDF"""
    with open(pdf_file_name, "rb") as opened_reading_pdf_file:
        pdf_file = opened_reading_pdf_file.read()

    pdf_index = pdf_file.index(b"%PDF")
    # שימוש ב-rindex כדי למצוא את ה-EOF האחרון בקובץ (מונע חיתוך בקבצים גדולים)
    eof_index = pdf_file.rindex(b"%%EOF") + 5
    # שמירה על ירידת שורה אחרי %%EOF אם קיימת
    if eof_index < len(pdf_file) and pdf_file[eof_index:eof_index + 1] in (b"\r", b"\n"):
        eof_index += 1

    final_pdf_file = remove_a_hidden_file_from_a_given_file(pdf_file, pdf_index, eof_index)

    with open(output_file_name, "wb") as opened_writing_pdf_file:
        opened_writing_pdf_file.write(final_pdf_file)


def remove_hidden_file_from_png_file(png_file_name, output_file_name):
    """מסיר קובץ מוסתר מתוך קובץ PNG"""
    with open(png_file_name, "rb") as opened_reading_png_file:
        png_file = opened_reading_png_file.read()

    # חיפוש החתימה המלאה של PNG למניעת זיהוי שגוי באמצע קובץ גדול
    png_index = png_file.index(PNG_MAGIC)
    iend_index = png_file.rindex(b"IEND") + 8

    final_png_file = remove_a_hidden_file_from_a_given_file(png_file, png_index, iend_index)

    with open(output_file_name, "wb") as opened_writing_png_file:
        opened_writing_png_file.write(final_png_file)


def encrypt(msg, iv, key):
    """הצפנת AES-CBC מהירה באמצעות המימוש המובנה ב-C"""
    msg = pad_zero(msg)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(msg)


def decrypt(msg, iv, key):
    """פענוח AES-CBC מהיר באמצעות המימוש המובנה ב-C"""
    msg = pad_zero(msg)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(msg)


def decrypt_to_png(msg, iv, key):
    """פענוח קובץ מוסתר חזרה לקובץ PNG תקין"""
    res_of_decrypt = decrypt(msg, iv, key)

    png_index = res_of_decrypt.index(PNG_MAGIC)
    iend_index = res_of_decrypt.rindex(b"IEND")

    final_res = res_of_decrypt[png_index:iend_index + 8]
    final_res += res_of_decrypt[0:png_index]

    return final_res


def decrypt_to_pdf(msg, iv, key):
    """פענוח קובץ מוסתר חזרה לקובץ PDF תקין"""
    res_of_decrypt = decrypt(msg, iv, key)

    pdf_index = res_of_decrypt.index(b"%PDF")
    eof_index = res_of_decrypt.rindex(b"%%EOF")

    final_res = res_of_decrypt[pdf_index:eof_index + 6]
    final_res += res_of_decrypt[0:pdf_index]

    return final_res


def int_to_str_encoded(x):
    """המרת מספר להקסדצימלי באורך 8 תווים מקודד ל-bytes"""
    x = hex(x)[2:].rstrip("L")
    if len(x) % 8 != 0:
        x = x.zfill(8)
    return x.encode()


def hide_png_in_png(img1, img2, img3, key, iv):
    """הסתרת קובץ PNG בתוך PNG אחר"""
    with open(img1, "rb") as f:
        source = f.read()
    with open(img2, "rb") as f:
        target = f.read()

    source = pad_zero(source)
    print("IV: ", iv)

    source = decrypt(source, iv, key)
    source += int_to_str_encoded(crc32(source[12:]) % (1 << 32)) + target
    source = pad_zero(source)

    with open(img3, "wb") as f:
        f.write(encrypt(source, iv, key))


def hide_png_in_pdf(src, tar, out, key, iv):
    """הסתרת קובץ PNG בתוך קובץ PDF"""
    if "pdf" in from_file(src, mime=True).lower():
        pdf_path, img_path = src, tar
    else:
        pdf_path, img_path = tar, src

    with open(pdf_path, "rb") as f:
        pdf = f.read()
    with open(img_path, "rb") as f:
        img = f.read()

    pdf = pad_zero(pdf)
    print("IV: ", iv)

    pdf = decrypt(pdf, iv, key)
    pdf += img
    pdf = pad_zero(pdf)

    with open(out, "wb") as f:
        f.write(encrypt(pdf, iv, key))


def hide_pdf_in_png(src, tar, out, key, iv):
    """הסתרת קובץ PDF בתוך קובץ PNG"""
    if "png" in from_file(src, mime=True).lower():
        img_path, pdf_path = src, tar
    else:
        img_path, pdf_path = tar, src

    with open(img_path, "rb") as f:
        img = f.read()
    with open(pdf_path, "rb") as f:
        pdf = f.read()

    img = pad_zero(img)
    print("IV: ", iv)

    img = decrypt(img, iv, key)
    img += pdf
    img = pad_zero(img)

    with open(out, "wb") as f:
        f.write(encrypt(img, iv, key))
