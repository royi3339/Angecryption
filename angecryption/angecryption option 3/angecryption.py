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

        elif action == "decrypt-to-pdf":
            f.write(decrypt_to_pdf(s, iv, key))

        else:  # action == "encrypt":
            f.write(encrypt(s, iv, key))


ange_funcs = {
    "hide-png-in-png": hide_png_in_png,
    "hide-pdf-in-png": hide_pdf_in_png,
    "hide-png-in-pdf": hide_png_in_pdf
}

cleaning_funcs = {
    "make-png-clean": remove_hidden_file_from_png_file,
    "make-pdf-clean": remove_hidden_file_from_pdf_file
}


def main():
    """
    the main of the angecryption program.
    """
    args = menu()

    if args.action in ["encrypt", "decrypt", "decrypt-to-png", "decrypt-to-pdf"]:
        handle_file(args.source, args.key, args.iv, args.output, args.action)

    elif args.action in ["make-png-clean", "make-pdf-clean"]:
        cleaning_funcs[args.action](args.source, args.output)

    else:  # args.action in ["hide-png-in-png", "hide-pdf-in-png", "hide-png-in-pdf"]
        ange_funcs[args.action](args.source, args.target, args.output, args.key, args.iv)

    print("done ")


if __name__ == '__main__':
    main()
