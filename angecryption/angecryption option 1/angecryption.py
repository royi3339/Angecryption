# Royi Alishayev.

from menu_file import menu
from actions_file import encrypt, decrypt, decrypt_to_png, decrypt_to_file,  hide_png_in_png, hide_file_in_png,\
    remove_hidden_file_from_png_file, remove_wrapping_png_file, combine_file_and_png
from utils import ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE, HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG, MAKE_PNG_CLEAN,\
    MAKE_FILE_CLEAN


enc_dec_funcs_dict = {
    ENCRYPT: encrypt,
    DECRYPT: decrypt,
    DECRYPT_TO_PNG: decrypt_to_png,
    DECRYPT_TO_FILE: decrypt_to_file,
}

ange_funcs_dict = {
    HIDE_PNG_IN_PNG: hide_png_in_png,
    HIDE_FILE_IN_PNG: hide_file_in_png,
}

cleaning_funcs_dict = {
    MAKE_PNG_CLEAN: remove_hidden_file_from_png_file,
    MAKE_FILE_CLEAN: remove_wrapping_png_file,
}


def main():
    """
    the main of the angecryption program.
    """
    args = menu()

    if args.action in enc_dec_funcs_dict:
        # ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE
        enc_dec_funcs_dict[args.action](args.source, args.output, args.key, args.iv)

    elif args.action in cleaning_funcs_dict:
        # MAKE_PNG_CLEAN, MAKE_FILE_CLEAN
        cleaning_funcs_dict[args.action](args.source, args.output)

    elif args.action in ange_funcs_dict:
        # HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG
        ange_funcs_dict[args.action](args.source, args.target, args.output, args.key, args.iv)

    else:
        # COMBINE_FILE_IN_PNG
        combine_file_and_png(args.source, args.target, args.output)

    print("done ")


if __name__ == '__main__':
    main()
