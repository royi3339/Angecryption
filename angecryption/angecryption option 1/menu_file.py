# Royi Alishayev.

import argparse
from utils import check_key, check_iv, check_file, check_png
from utils import ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE, HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG, MAKE_PNG_CLEAN,\
    MAKE_FILE_CLEAN, COMBINE_FINE_IN_PNG

ENC_DEC_ACTIONS = [ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE]
ANGECRYPTION_ACTIONS = [HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG]


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

    else:  # namespace.action in [MAKE_PNG_CLEAN, MAKE_FILE_CLEAN, COMBINE_FINE_IN_PNG]:
        print("you have to insert a --key in length 16 in order to activate the program... but the key is useless...")

    return namespace
