# Royi Alishayev.

import argparse
from utils import check_key, check_iv, check_file, check_png
from utils import ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE, HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG, MAKE_PNG_CLEAN,\
    MAKE_FILE_CLEAN, COMBINE_FINE_IN_PNG
from utils import ENC_DEC_ACTIONS, ANGECRYPTION_ACTIONS


# def check_iv_or_key_type_and_length(param, name_of_param):
#     """
#     checking the given key / iv, if its a type of bytes, if not - encoding it to bytes...
#     and check if its length is 16.
#     """
#     if type(param) != bytes:
#         param = param.encode("iso-8859-1")
#
#     if len(param) != 16:
#         raise argparse.ArgumentTypeError(f"the {name_of_param} must be 16 bytes in length, and not {len(param)} bytes!")
#     return param


# def check_key(k):
#     """
#     checking the given key, if its a type of bytes, if not - encoding it to bytes...
#     and check if its length is 16.
#     """
#     k = check_iv_or_key_type_and_length(k, "key")
#     return k


# def check_iv(iv):
#     """
#     checking the given iv, if its a type of bytes, if not - encoding it to bytes...
#     and check if its length is 16.
#     """
#     iv = check_iv_or_key_type_and_length(iv, "iv")
#     return iv


# def check_file(f):
#     """
#     checking the given file, if not exist - will raise a error.
#     """
#     try:
#         open(f, "r")
#     except Exception as e:
#         raise argparse.ArgumentTypeError("can't open {}: {}".format(f, e[1]))
#
#     # TODO: this if check the magic number of the given file, - will make a error on a given encrypted/decrypted file...
#     # file_types = ["png", "pdf"]
#     # if from_file(f, mime=True).split("/")[1] not in file_types:
#     #     raise argparse.ArgumentTypeError("the file must be either a {}".format(" or a ".join(file_types)))
#
#     return f


# def check_png(f):
#     """
#     checking the given PNG file magic number, and if its exist.
#      if not exist - will raise a error.
#     """
#     file_types = ["png"]
#
#     try:
#         open(f, "r")
#     except Exception as e:
#         raise argparse.ArgumentTypeError("can't open {}: {}".format(f, e[1]))
#
#     if from_file(f, mime=True).split("/")[1] not in file_types:
#         raise argparse.ArgumentTypeError("the file must be either a {}".format(" or a ".join(file_types)))
#     return f


def menu():
    """
    the menu of the program, that the user gets when entered to the program.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-k", "--key", type=check_key, help="the encryption key", required=True)
    parser.add_argument("-s", "--source", type=check_png,
                        help="the source file(the PNG file that shows up by default in the result PNG file)",
                        required=True)

    parser.add_argument("-a", "--action",
                        choices=[f"{ENCRYPT}", f"{DECRYPT}", f"{DECRYPT_TO_PNG}", f"{DECRYPT_TO_FILE}",
                                 f"{HIDE_PNG_IN_PNG}", f"{HIDE_FILE_IN_PNG}",
                                 f"{COMBINE_FINE_IN_PNG}",
                                 f"{MAKE_PNG_CLEAN}", f"{MAKE_FILE_CLEAN}"],
                        help="the action to perform:\n"
                             f"{ENCRYPT}: %s\n"
                             f"{DECRYPT}: %s\n"
                             f"{DECRYPT_TO_FILE}: %s\n"
                             f"{HIDE_FILE_IN_PNG}: %s\n"
                             f"{COMBINE_FINE_IN_PNG}: %s\n"
                             f"{MAKE_PNG_CLEAN}: %s\n"
                             f"{MAKE_FILE_CLEAN}: %s\n"
                             % ("encrypt the result file(flag --iv required)",
                                "decrypt the result file(flag --iv required)",
                                "decrypt a given angecrypted file in order to get the hidden file(flag -iv/--iv required)",
                                "generate an angecrypted PNG file,"
                                " which fileTYPE2 (must be a png file) will contains a hidden fileTYPE1 inside him"
                                "(flag --iv required, -t/--target required)",
                                "combine 2 files (1: .png, 2: any other file type) to a"
                                " png file - without decryption/encryption... recommend:"
                                "do this action on a png file with zip/rar file in order to get a complete result..."
                                "(flag -o/--output required)",
                                "returns a 'clean' PNG file, without an angecrypted file inside it"
                                "(flag -o/--output required)",
                                "returns a 'clean' file, without the wrapping PNG file on it"
                                "(flag -o/--output required)"
                                ),

                        # "".format(
                        #     "encrypt the result file(flag --iv required)",
                        #     "decrypt the result file(flag --iv required)",
                        #     "decrypt a given angecrypted file in order to get the hidden file(flag -iv/--iv required)",
                        #     "generate an angecrypted PNG file,"
                        #     " which fileTYPE2 (must be a png file) will contains a hidden fileTYPE1 inside him"
                        #     "(flag --iv required, -t/--target required)",
                        #     "combine 2 files (1: .png, 2: any other file type) to a"
                        #     " png file - without decryption/encryption... recommend:"
                        #     "do this action on a png file with zip/rar file in order to get a complete result..."
                        #     "(flag -o/--output required)",
                        #     "returns a 'clean' PNG file, without an angecrypted file inside it"
                        #     "(flag -o/--output required)",
                        #     "returns a 'clean' file, without the wrapping PNG file on it"
                        #     "(flag -o/--output required)"
                        # ),

                        required=True)
    parser.add_argument("-iv", "--iv", type=check_iv, help="the iv generated from the encryption phase")
    parser.add_argument("-t", "--target", type=check_file,
                        help="the target file(the one that's hidden in the result file)")
    parser.add_argument("-o", "--output", help="the output/result file (default %(default)s)",
                        default="angecryption.out")

    namespace = parser.parse_args()

    if namespace.action in ENC_DEC_ACTIONS:
        if namespace.iv is None:
            parser.error('IV not specified')

    elif namespace.action in ANGECRYPTION_ACTIONS:
        if namespace.target is None:
            parser.error('TARGET file not specified')
        if namespace.iv is None:
            parser.error('IV not specified')

    else:  # namespace.action in ["make-png-clean", "make-file-clean", "combine-file-in-png"]:
        print("you have to insert a --key in length 16 in order to activate the program... but the key is useless...")

    return namespace
