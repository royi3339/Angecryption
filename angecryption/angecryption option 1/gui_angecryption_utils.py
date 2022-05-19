# Royi Alishayev.

from tkinter import *
import tkinter as tk
from tkinter import ttk
from actions_file import *
import glob
import pathlib
from utils import check_key, check_iv, check_png, check_file

# # print("encrypt: {}".format("heree11"))
# rr = "99dds09"
# ff = "dsfd3"
# yy = "84d"
# print(f"encrypt: {rr} %s %s " % (ff, yy))
#
# print("heree im  am\n"
#       "going to %s "
#       "and then %s" % (ff, yy))


def dir_func(file_or_path):
    """
    Function that return the list of the files/folder of a path as string, if not exists - return ''
    """
    if type(file_or_path) == list:
        file_or_path = str(file_or_path[0])
    files_list = glob.glob(file_or_path)
    result_of_dir = ''
    if not not files_list:
        for file in files_list:
            result_of_dir += file + "\n"

    return result_of_dir


def files_in_the_directory(file_or_path):
    file_res = dir_func(file_or_path).strip()
    file_res_as_list = file_res.split("\n")
    res = list(map(lambda x:x.split("\\")[-1], file_res_as_list))
    # print(res)
    return res

# check_cleaning_funcs_params, check_combining_files_params


def check_enc_dec_funcs_params(src_param, key_param, iv_param):
    src_valid = check_png(src_param)
    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, key_valid, iv_valid


def check_angecryption_funcs_params(src_param, tar_param, key_param, iv_param):
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, tar_valid, key_valid, iv_valid


def check_cleaning_funcs_params(src_param):
    src_valid = check_png(src_param)
    return src_valid


def check_combine_file_in_png_params(src_param, tar_param):
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    return src_valid, tar_valid


def main():
    current_path = str(pathlib.Path(__file__).parent.resolve()) + "\\*.*"
    # print(current_path)
    # print(dir_func(current_path))
    files_in_dir = files_in_the_directory(current_path)
    print(files_in_dir)




def main2():
    # def some_func():mlkvf

    # Top level window
    frame_root = tk.Tk()
    frame_root.eval('tk::PlaceWindow %s center' % frame_root.winfo_toplevel())
    frame_root.title("TextBox Input")
    frame_root.geometry('300x350')
    frame_root.resizable(False, False)

    frame = Frame(frame_root)
    frame.pack(padx=10, pady=10, fill='x')

    # Label Creation
    key_lbl = tk.Label(frame, text='Key: ')
    key_lbl.pack(fill='x', expand=True)

    # TextBox Creation
    key_inpt = tk.Entry(frame, width=55)
    key_inpt.pack(fill='x', expand=True)

    # # Button Creation
    # printButton = ttk.Button(frame, text="ok", command=some_func)
    # printButton.pack(fill='x', expand=True, pady=10)


    frame.mainloop()

if __name__ == '__main__':
    main()
