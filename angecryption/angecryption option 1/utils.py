# Royi Alishayev.

import argparse
from puremagic import from_file

ENCRYPT = "encrypt"
DECRYPT = "decrypt"
DECRYPT_TO_PNG = "decrypt-to-png"
DECRYPT_TO_FILE = "decrypt-to-file"
HIDE_PNG_IN_PNG = "hide-png-in-png"
HIDE_FILE_IN_PNG = "hide-file-in-png"
MAKE_PNG_CLEAN = "make-png-clean"
MAKE_FILE_CLEAN = "make-file-clean"
COMBINE_FINE_IN_PNG = "combine-file-in-png"

ENC_DEC_ACTIONS = [ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE]
ANGECRYPTION_ACTIONS = [HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG]
CLEANING_ACTIONS = [MAKE_PNG_CLEAN, MAKE_FILE_CLEAN]


def check_iv_or_key_type_and_length(param, name_of_param):
    """
    checking the given key / iv, if its a type of bytes, if not - encoding it to bytes...
    and check if its length is 16.
    """
    if type(param) != bytes:
        param = param.encode("iso-8859-1")

    if len(param) != 16:
        raise argparse.ArgumentTypeError(f"the {name_of_param} must be 16 bytes in length, and not {len(param)} bytes!")
    return param


def check_key(k):
    """
    checking the given key, if its a type of bytes, if not - encoding it to bytes...
    and check if its length is 16.
    """
    k = check_iv_or_key_type_and_length(k, "key")
    return k


def check_iv(iv):
    """
    checking the given iv, if its a type of bytes, if not - encoding it to bytes...
    and check if its length is 16.
    """
    iv = check_iv_or_key_type_and_length(iv, "iv")
    return iv


def check_file(f):
    """
    checking the given file, if not exist - will raise a error.
    """
    try:
        open(f, "r")
    except Exception as e:
        raise argparse.ArgumentTypeError("can't open {}: {}".format(f, e[1]))

    # TODO: this if check the magic number of the given file, - will make a error on a given encrypted/decrypted file...
    # file_types = ["png", "pdf"]
    # if from_file(f, mime=True).split("/")[1] not in file_types:
    #     raise argparse.ArgumentTypeError("the file must be either a {}".format(" or a ".join(file_types)))

    return f


def check_png(f):
    """
    checking the given PNG file magic number, and if its exist.
     if not exist - will raise a error.
    """
    file_types = ["png"]

    try:
        open(f, "r")
    except Exception as e:
        raise argparse.ArgumentTypeError("can't open {}: {}".format(f, e[1]))

    if from_file(f, mime=True).split("/")[1] not in file_types:
        raise argparse.ArgumentTypeError("the 'Source File' must be a {}".format(" or a ".join(file_types)))
    return f



