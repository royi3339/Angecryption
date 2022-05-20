# Royi Alishayev.

import pathlib
from tkinter import *
import tkinter as tk
from tkinter import ttk
from actions_file import encrypt, decrypt, decrypt_to_png, decrypt_to_file,  hide_png_in_png, hide_file_in_png,\
    remove_hidden_file_from_png_file, remove_wrapping_png_file, combine_file_and_png
from utils import ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE, HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG, MAKE_PNG_CLEAN,\
    MAKE_FILE_CLEAN, COMBINE_FINE_IN_PNG
from gui_angecryption_utils import files_in_the_directory, check_enc_dec_funcs_params, check_angecryption_funcs_params,\
    check_cleaning_funcs_params, check_combine_file_in_png_params


ACTION_FUNCTIONS_DICT = {
    ENCRYPT: encrypt,
    DECRYPT: decrypt,
    DECRYPT_TO_PNG: decrypt_to_png,
    DECRYPT_TO_FILE: decrypt_to_file,
    HIDE_PNG_IN_PNG: hide_png_in_png,
    HIDE_FILE_IN_PNG: hide_file_in_png,
    MAKE_PNG_CLEAN: remove_hidden_file_from_png_file,
    MAKE_FILE_CLEAN: remove_wrapping_png_file,
    COMBINE_FINE_IN_PNG: combine_file_and_png
}

ENC_DEC_FUNCS = [ENCRYPT, DECRYPT, DECRYPT_TO_PNG, DECRYPT_TO_FILE]
ANGECRYPTION_FUNCS = [HIDE_PNG_IN_PNG, HIDE_FILE_IN_PNG]
CLEANING_FUNCS = [MAKE_PNG_CLEAN, MAKE_FILE_CLEAN]

DEFAULT_OUTPUT_FILE_NAME = "angecrypted.out"
CURRENT_PATH_FILES = str(pathlib.Path(__file__).parent.resolve()) + "\\*.*"


def check_params_list_values(list_of_params):
    """
    get a list of params, and check that they arre not an empty string ('').
    if one of them is empty string ('') - will return a "request to fill the params"
    else will return '' - which means that there is no error message...
    """
    for param in list_of_params:
        if not param:
            # if the box is empty (''), will be returned a error message...
            return "Please fill al the required box values !!!"
    return ''


def ok_button_func():
    """
    Function for getting Input from Entry box and activating the right function as well.
    """
    combo_action_result = action_inpt.get()

    try:
        if combo_action_result in ENC_DEC_FUNCS:
            src_param = source_inpt.get()
            out_param = output_inpt.get()
            key_param = key_inpt.get()
            iv_param = iv_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME

            error_msg = check_params_list_values([src_param, key_param, iv_param])
            if error_msg:
                write_to_label(lbl, error_msg, msg_color="red", to_print=True)
                return

            src_param, key_param, iv_param = check_enc_dec_funcs_params(src_param, key_param, iv_param, combo_action_result)
            function_params = [src_param, out_param, key_param, iv_param]

        elif combo_action_result in ANGECRYPTION_FUNCS:
            src_param = source_inpt.get()
            tar_param = target_inpt.get()
            out_param = output_inpt.get()
            key_param = key_inpt.get()
            iv_param = iv_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME

            error_msg = check_params_list_values([src_param, tar_param, key_param, iv_param])
            if error_msg:
                write_to_label(lbl, error_msg, msg_color="red", to_print=True)
                return

            src_param, tar_param, key_param, iv_param = check_angecryption_funcs_params(src_param, tar_param, key_param, iv_param)
            function_params = [src_param, tar_param, out_param, key_param, iv_param]

        elif combo_action_result in CLEANING_FUNCS:
            src_param = source_inpt.get()
            out_param = output_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME
            error_msg = check_params_list_values([src_param])
            if error_msg:
                write_to_label(lbl, error_msg, msg_color="red", to_print=True)
                return

            src_param = check_cleaning_funcs_params(src_param)
            function_params = [src_param, out_param]

        elif combo_action_result == COMBINE_FINE_IN_PNG:
            src_param = source_inpt.get()
            tar_param = target_inpt.get()
            out_param = output_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME
            error_msg = check_params_list_values([src_param, tar_param])
            if error_msg:
                write_to_label(lbl, error_msg, msg_color="red", to_print=True)
                return

            src_param, tar_param = check_combine_file_in_png_params(src_param, tar_param)
            function_params = [src_param, tar_param, out_param]

        else:
            # if nothing is chosen - print "please choose one..."
            error_msg = "Please choose which action you want to perform !\nand insert the proper values\n"
            write_to_label(lbl, error_msg, msg_color="blue", to_print=True)
            return

        if error_msg:
            write_to_label(lbl, error_msg, msg_color="red", to_print=True)
        else:
            ACTION_FUNCTIONS_DICT[combo_action_result](*function_params)
            # inp = inputtxt.get(1.0, "end-1c")
            write_to_label(lbl, "done", msg_color="green", to_print=True)

    except Exception as e:
        write_to_label(lbl, e, msg_color="red", to_print=True)


# Top level window
frame_root = tk.Tk()
frame_root.eval('tk::PlaceWindow %s center' % frame_root.winfo_toplevel())
frame_root.title("Angecryption Software")
frame_root.geometry('300x355')
frame_root.resizable(False, False)

frame = Frame(frame_root)
frame.pack(padx=10, pady=10, fill='x')

# Label Creation
action_lbl = tk.Label(frame, text="Action: ")
action_lbl.pack(fill='x', expand=True)

# Combobox creation
action_inpt = ttk.Combobox(frame, width=55)

# Adding combobox drop down list
action_inpt["values"] = [action for action in ACTION_FUNCTIONS_DICT]
action_inpt.pack(fill='x', expand=True)

# prevent typing a value
action_inpt['state'] = 'readonly'


# Label Creation
source_lbl = tk.Label(frame, text='Source: ')
source_lbl.pack(fill='x', expand=True)

# Combobox Creation
source_inpt = ttk.Combobox(frame, width=55)
source_inpt["values"] = files_in_the_directory(CURRENT_PATH_FILES)
source_inpt.pack(fill='x', expand=True)

# Label Creation
key_lbl = tk.Label(frame, text='Key: ')
key_lbl.pack(fill='x', expand=True)

# EntryBox Creation
key_inpt = ttk.Entry(frame, width=55)
key_inpt.pack(fill='x', expand=True)

# Label Creation
iv_lbl = tk.Label(frame, text='IV: ')
iv_lbl.pack(fill='x', expand=True)

# EntryBox Creation
iv_inpt = ttk.Entry(frame, width=55)
iv_inpt.pack(fill='x', expand=True)

# Label Creation
target_lbl = tk.Label(frame, text='Target: ')
target_lbl.pack(fill='x', expand=True)

# Combobox Creation
target_inpt = ttk.Combobox(frame, width=55)
target_inpt["values"] = files_in_the_directory(CURRENT_PATH_FILES)
target_inpt.pack(fill='x', expand=True)

# Label Creation
output_lbl = tk.Label(frame, text='Output: ')
output_lbl.pack(fill='x', expand=True)

# EntryBox Creation
output_inpt = ttk.Entry(frame, width=55)
output_inpt.pack(fill='x', expand=True)

# Button Creation
printButton = ttk.Button(frame, text="OK", command=ok_button_func)
printButton.pack(fill='x', expand=True, pady=10)

# Label Creation
lbl = tk.Label(frame, text='')
lbl.pack(fill='x', expand=True)


def write_to_label(lbl_obj, new_text='', msg_color="black", to_print=False):
    """
    A simple function that writing a message to a given label
    and if to_print is - True, will print the message as well.
    """
    if to_print:
        print(new_text)
    lbl_obj.config(text=new_text, foreground=msg_color)


def combo_action_changed(action_chosen):
    """
    Bind the selected value changes

    handle the action changed event
    and calling to the proper function that will
    locks and unlocks the right values box.
    """
    combo_result = action_inpt.get()
    # print(f'You selected {combo_result}')

    # clear the text the we current have in the label.
    write_to_label(lbl)

    if combo_result in ENC_DEC_FUNCS:
        combo_enc_dec_funcs()
    elif combo_result in ANGECRYPTION_FUNCS:
        combo_angecryption_funcs()
    elif combo_result in CLEANING_FUNCS:
        combo_cleaning_funcs()
    else:  # combo_result in [COMBINE_FILE_IN_PNG]:
        combo_combine_file_in_png()


def config_box_list_state(list_of_box, new_state="normal"):
    """
    new_state = "readonly" / normal / disabled
    """
    for box in list_of_box:
        box.config(state=new_state)


def combo_enc_dec_funcs():
    """
    changing the proper Entry Box to be "disabled", and "normal"...
    source, key, iv, output => "normal".
    target => "disabled".
    """
    config_box_list_state([source_inpt, key_inpt, iv_inpt, output_inpt], "normal")
    config_box_list_state([target_inpt], "disabled")


def combo_angecryption_funcs():
    """
    changing the proper Entry Box to be "readonly", and "normal"...
    source, target, key, iv, output => "normal".
    """
    config_box_list_state([source_inpt, key_inpt, iv_inpt, target_inpt, output_inpt], "normal")


def combo_cleaning_funcs():
    """
    changing the proper Entry Box to be "disabled", and "normal"...
    source, output => "normal".
    target, key, iv => "disabled".
    """
    config_box_list_state([source_inpt, output_inpt], "normal")
    config_box_list_state([target_inpt, key_inpt, iv_inpt], "disabled")


def combo_combine_file_in_png():
    """
    changing the proper Entry Box to be "disabled", and "normal"...
    source, target, output => "normal".
    key, iv => "disabled".
    """
    config_box_list_state([source_inpt, target_inpt, output_inpt], "normal")
    config_box_list_state([key_inpt, iv_inpt], "disabled")


action_inpt.bind('<<ComboboxSelected>>', combo_action_changed)

frame.mainloop()
