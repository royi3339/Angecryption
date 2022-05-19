# Royi Alishayev.

# import win32api, win32con, win32gui
from tkinter import *
# from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from actions_file import *
# from utils import check_key, check_iv
import pathlib
from gui_angecryption_utils import files_in_the_directory, check_enc_dec_funcs_params, check_angecryption_funcs_params, check_cleaning_funcs_params, check_combine_file_in_png_params

ENCRYPT = "encrypt"
DECRYPT = "decrypt"
DECRYPT_TO_PNG = "decrypt-to-png"
DECRYPT_TO_FILE = "decrypt-to-file"
HIDE_PNG_IN_PNG = "hide-png-in-png"
HIDE_FILE_IN_PNG = "hide-file-in-png"
MAKE_PNG_CLEAN = "make-png-clean"
MAKE_FILE_CLEAN = "make-file-clean"
COMBINE_FINE_IN_PNG = "combine-file-in-png"

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

# f = {
#     ENC_DEC_FUNCS:9
# }

DEFAULT_OUTPUT_FILE_NAME = "angecrypted.out"
CURRENT_PATH_FILES = str(pathlib.Path(__file__).parent.resolve()) + "\\*.*"
# print(files_in_the_directory(CURRENT_PATH_FILES))

# Top level window
frame_root = tk.Tk()
frame_root.eval('tk::PlaceWindow %s center' % frame_root.winfo_toplevel())
frame_root.title("TextBox Input")
frame_root.geometry('300x350')
frame_root.resizable(False, False)

frame = Frame(frame_root)
frame.pack(padx=10, pady=10, fill='x')


# Function for getting Input
# from textbox and printing it
# at label widget
def ok_button_func():
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

            # function_params_container = [source_inpt, output_inpt, key_inpt, iv_inpt]
            # is_inpt_ok, src_param, output_param, key_param, iv_param = get_box_list_values(function_params_container)

            src_param, key_param, iv_param = check_enc_dec_funcs_params(src_param, key_param, iv_param)
            function_params = [src_param, out_param, key_param, iv_param]
            # ACTION_FUNCTIONS_DICT[combo_action_result](*function_params_container)

        elif combo_action_result in ANGECRYPTION_FUNCS:
            src_param = source_inpt.get()
            tar_param = target_inpt.get()
            out_param = output_inpt.get()
            key_param = key_inpt.get()
            iv_param = iv_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME

            error_msg = check_params_list_values([src_param, tar_param, key_param, iv_param])

            # function_params_container = [source_inpt, target_inpt, output_inpt, key_inpt, iv_inpt]
            # is_inpt_ok, src_param, tar_param, out_param, key_param, iv_param = get_box_list_values(function_params_container)

            src_param, tar_param, key_param, iv_param = check_angecryption_funcs_params(src_param, tar_param, key_param, iv_param)
            function_params = [src_param, tar_param, out_param, key_param, iv_param]
            # ACTION_FUNCTIONS_DICT[combo_action_result](*function_params_container)

        elif combo_action_result in CLEANING_FUNCS:
            src_param = source_inpt.get()
            out_param = output_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME
            error_msg = check_params_list_values([src_param])

            # function_params_container = [source_inpt, output_inpt]
            # is_inpt_ok, src_param, out_param = get_box_list_values(function_params_container)

            src_param = check_cleaning_funcs_params(src_param)
            function_params = [src_param, out_param]
            # ACTION_FUNCTIONS_DICT[combo_action_result](*function_params_container)

        elif combo_action_result == COMBINE_FINE_IN_PNG:
            src_param = source_inpt.get()
            tar_param = target_inpt.get()
            out_param = output_inpt.get()
            if not out_param:
                out_param = DEFAULT_OUTPUT_FILE_NAME
            error_msg = check_params_list_values([src_param, tar_param])

            # function_params_container = [source_inpt, target_inpt, output_inpt]
            # is_inpt_ok, src_param, tar_param, out_param = get_box_list_values(function_params_container)

            src_param, tar_param = check_combine_file_in_png_params(src_param, tar_param)
            function_params = [src_param, tar_param, out_param]
            # ACTION_FUNCTIONS_DICT[combo_action_result](*function_params_container)

        else:
            # if nothing is chosen - print "please choose one... etc"
            print("TODO...")
            write_to_label(lbl, "Please choose which action you want to perform !\nand insert the proper values", msg_color="blue")
            return

        # is_inpt_ok, function_params = get_box_list_values(function_params_container)
        if error_msg:
            write_to_label(lbl, error_msg, msg_color="red")
        else:
            ACTION_FUNCTIONS_DICT[combo_action_result](*function_params)
            # inp = inputtxt.get(1.0, "end-1c")
            write_to_label(lbl, "done", msg_color="green")

    except Exception as e:
        print(e)
        write_to_label(lbl, e, msg_color="red")


# Label Creation
action_lbl = tk.Label(frame, text="Action: ")
action_lbl.pack(fill='x', expand=True)

# Combobox creation
action_inpt = ttk.Combobox(frame, width=55)

# Adding combobox drop down list
action_inpt["values"] = (
    ENCRYPT,
    DECRYPT,
    DECRYPT_TO_PNG,
    DECRYPT_TO_FILE,
    HIDE_PNG_IN_PNG,
    HIDE_FILE_IN_PNG,
    MAKE_PNG_CLEAN,
    MAKE_FILE_CLEAN,
    COMBINE_FINE_IN_PNG
)

action_inpt.pack(fill='x', expand=True)

# prevent typing a value
action_inpt['state'] = 'readonly'

# action_inpt.current(0)


# Label Creation
source_lbl = tk.Label(frame, text='Source: ')
source_lbl.pack(fill='x', expand=True)

# TextBox Creation
# source_inpt = tk.Entry(frame, width=55)
source_inpt = ttk.Combobox(frame, width=55)
source_inpt["values"] = files_in_the_directory(CURRENT_PATH_FILES)
source_inpt.pack(fill='x', expand=True)

# Label Creation
key_lbl = tk.Label(frame, text='Key: ')
key_lbl.pack(fill='x', expand=True)

# TextBox Creation
key_inpt = tk.Entry(frame, width=55)
key_inpt.pack(fill='x', expand=True)

# Label Creation
iv_lbl = tk.Label(frame, text='IV: ')
iv_lbl.pack(fill='x', expand=True)

# TextBox Creation
iv_inpt = tk.Entry(frame, width=55)
iv_inpt.pack(fill='x', expand=True)

# Label Creation
target_lbl = tk.Label(frame, text='Target: ')
target_lbl.pack(fill='x', expand=True)

# TextBox Creation
# target_inpt = tk.Entry(frame, width=55)
target_inpt = ttk.Combobox(frame, width=55)
target_inpt["values"] = files_in_the_directory(CURRENT_PATH_FILES)
target_inpt.pack(fill='x', expand=True)

# Label Creation
output_lbl = tk.Label(frame, text='Output: ')
output_lbl.pack(fill='x', expand=True)

# TextBox Creation
output_inpt = tk.Entry(frame, width=55, text="angecrypted.out")
output_inpt.pack(fill='x', expand=True)

# Button Creation
printButton = ttk.Button(frame, text="ok", command=ok_button_func)
printButton.pack(fill='x', expand=True, pady=10)

# Label Creation
lbl = tk.Label(frame, text='')
lbl.pack(fill='x', expand=True)


# bind the selected value changes
def combo_action_changed(month_inpt):
    """ handle the month changed event """
    combo_result = action_inpt.get()
    print(f'You selected {combo_result}')

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


def check_params_list_values(list_of_params):
    for param in list_of_params:
        if not param:
            # if the box is empty ('')...
            return "Please fill al the required box values !!!"
    return ''

# def get_box_list_values(list_of_box):
#     result_list_of_values = []
#     for box in list_of_box:
#         box_text = box.get()
#         if not box_text:
#             # if the box is empty ('')...
#             if box == output_inpt:
#                 result_list_of_values.append(DEFAULT_OUTPUT_FILE_NAME)
#             else:
#                 error_msg = "Please fill the - '" + box_per_label_dict[box].cget("text") + "' box !!!"
#                 return False, error_msg
#         else:
#             result_list_of_values.append(box_text)
#     return True, result_list_of_values


def write_to_label(lbl_obj, new_text='', msg_color="black"):
    lbl_obj.config(text=new_text, foreground=msg_color)


def combo_enc_dec_funcs():
    """
    changing the proper Entry Box to be "readonly", and "normal"...
    source, key, iv, output => "normal".
    target => "readonly".
    """
    config_box_list_state([source_inpt, key_inpt, iv_inpt, output_inpt], "normal")
    config_box_list_state([target_inpt], "readonly")


def combo_angecryption_funcs():
    """
    changing the proper Entry Box to be "readonly", and "normal"...
    """
    config_box_list_state([source_inpt, key_inpt, iv_inpt, target_inpt, output_inpt], "normal")


def combo_cleaning_funcs():
    """
    changing the proper Entry Box to be "readonly", and "normal"...
    """
    config_box_list_state([source_inpt, output_inpt], "normal")
    config_box_list_state([target_inpt, key_inpt, iv_inpt], "readonly")


def combo_combine_file_in_png():
    """
    changing the proper Entry Box to be "readonly", and "normal"...
    """
    config_box_list_state([source_inpt, target_inpt, output_inpt], "normal")
    config_box_list_state([key_inpt, iv_inpt], "readonly")


box_per_label_dict = {
    action_inpt: action_lbl,
    source_inpt: source_lbl,
    key_inpt: key_lbl,
    iv_inpt: iv_lbl,
    target_inpt: target_lbl,
    output_inpt: output_lbl,
}

action_inpt.bind('<<ComboboxSelected>>', combo_action_changed)

frame.mainloop()
