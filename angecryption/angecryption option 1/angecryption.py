# Royi Alishayev.

from menu_file import menu
from actions_file import *


def handle_file(src, key, iv, out, action):
    """
    we use this method when chose action of:
    "encrypt", "decrypt", "decrypt-to-png", "decrypt-to-pdf"
    """
    with open(src, "rb") as f:
        s = f.read()

    with open(out, "wb") as f:
        if action == "decrypt":
            f.write(decrypt(s, iv, key))

        elif action == "decrypt-to-png":
            f.write(decrypt_to_png(s, iv, key))

        elif action == "decrypt-to-file":
            f.write(decrypt_to_file(s, iv, key))

        else:  # action == "encrypt":
            f.write(encrypt(s, iv, key))


ange_funcs = {
    "hide-png-in-png": hide_png_in_png,
    "hide-file-in-png": hide_file_in_png,
}

cleaning_funcs = {
    "make-png-clean": remove_hidden_file_from_png_file,
    "make-file-clean": remove_wrapping_png_file,
    # "combine-file-in-png": combine_file_and_png
}


def main():
    """
    the main of the angecryption program.
    """
    args = menu()

    if args.action in ["encrypt", "decrypt", "decrypt-to-png", "decrypt-to-file"]:
        handle_file(args.source, args.key, args.iv, args.output, args.action)

    elif args.action in ["make-png-clean", "make-file-clean"]:
        cleaning_funcs[args.action](args.source, args.output)
       
    elif args.action in ["combine-file-in-png"]:
        combine_file_and_png(args.source, args.target, args.output)

    else:  # args.action in ["hide-png-in-png", "hide-file-in-png"]
        ange_funcs[args.action](args.source, args.target, args.output, args.key, args.iv)

    print("done ")


if __name__ == '__main__':
    main()
