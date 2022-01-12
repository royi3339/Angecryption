# Royi Alishayev.

import argparse


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


def menu():
    """
    the menu of the program, that the user gets when entered to the program.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-k", "--key", type=check_key, help="the encryption key", required=True)
    parser.add_argument("-s", "--source", type=check_file,
                        help="the source file(the one that shows up by default in the result file)", required=True)

    parser.add_argument("-a", "--action",
                        choices=["encrypt", "decrypt",
                                 "decrypt-to-png", "decrypt-to-pdf",
                                 "hide-png-in-png", "hide-png-in-pdf", "hide-pdf-in-png",
                                 "make-png-clean", "make-pdf-clean"],
                        help="the action to perform:\n"
                             "encrypt: {}\n"
                             "decrypt: {}\n"
                             "decrypt-to-fileTYPE: {}\n"
                             "hide-fileTYPE1-in-fileTYPE2: {}\n"
                             "make-png-clean: {}\n"
                             "make-pdf-clean: {}\n".format(
                            "encrypt the result file(flag -iv/--iv required)",
                            "decrypt the result file(flag -iv/--iv required)",
                            "decrypt a given angecrypted file in order to get the hidden file(flag -iv/--iv required)",
                            "generate an angecrypted file,"
                            " which fileTYPE2 will contains a hidden fileTYPE1 inside him"
                            "(flag -iv/--iv required, -t/--target required)",
                            "returns a 'clean' PNG file, without an angecrypted file inside it"
                            "(flag -o/--output required)",
                            "returns a 'clean' PDF file, without an angecrypted file inside it"
                            "(flag -o/--output required)"
                        ),
                        required=True)
    parser.add_argument("-iv", "--iv", type=check_iv, help="the iv generated from the encryption phase")
    parser.add_argument("-t", "--target", type=check_file,
                        help="the target file(the one that's hidden in the result file)")
    parser.add_argument("-o", "--output", help="the output/result file (default %(default)s)",
                        default="angecryption.out")

    namespace = parser.parse_args()

    if namespace.action in ["encrypt", "decrypt", "decrypt-to-png", "decrypt-to-pdf"]:
        if namespace.iv is None:
            parser.error('IV not specified')

    elif namespace.action in ["hide-png-in-png", "hide-pdf-in-png", "hide-png-in-pdf"]:
        if namespace.iv is None:
            parser.error('IV not specified')
        if namespace.target is None:
            parser.error('TARGET file not specified')

    else:  # namespace.action in ["make-png-clean", "make-pdf-clean"]:
        print("you have to insert a --key in length 16 in order to activate the program... but the key is useless...")

    return namespace
