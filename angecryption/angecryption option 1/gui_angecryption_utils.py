# Royi Alishayev.

import glob
from utils import check_key, check_iv, check_png, check_file, ENCRYPT, DECRYPT
from tkinter import messagebox, Tk


def dir_func(file_or_path):
    """
    Function that return the list of the files/folder of a path as string, if not exists - return ''
    return - 1 big string as a result.
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
    """
    Function that return the list of the files/folder of a path as string, if not exists - return ''
    using the dir_func(), and then parsing the result in order to get a list of options, and not 1 big string...
    """
    file_res = dir_func(file_or_path).strip()
    file_res_as_list = file_res.split("\n")
    res = list(map(lambda x: x.split("\\")[-1], file_res_as_list))
    return res


def check_enc_dec_funcs_params(src_param, key_param, iv_param, func_name=''):
    """
    checking if the values that "enc dec funcs" should get - are valid.
    will raise a error if one or more are - invalid.
    """

    # if we just want to encrypt/decrypt a file - we will check if the source_param file is exist...
    # we don't make a "check_png()", because the file could be invalid thus the encrypt/decrypt action...
    if func_name in [ENCRYPT, DECRYPT]:
        src_valid = check_file(src_param)

    # else we probably want to perform DECRYPT_TO_PNG/DECRYPT_TO_FILE - we will check if the source_param file is a PNG.
    else:  # func_name in [DECRYPT_TO_PNG, DECRYPT_TO_FILE]
        src_valid = check_png(src_param)

    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, key_valid, iv_valid


def check_angecryption_funcs_params(src_param, tar_param, key_param, iv_param):
    """
    checking if the values that "angecryption funcs" should get - are valid.
    will raise a error if one or more are - invalid.
    """
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, tar_valid, key_valid, iv_valid


def check_cleaning_funcs_params(src_param):
    """
    checking if the values that "cleaning funcs" should get - are valid.
    will raise a error if one or more are - invalid.
    """
    src_valid = check_png(src_param)
    return src_valid


def check_combine_file_in_png_params(src_param, tar_param):
    """
    checking if the values that "combine_file_in_png()" should get - are valid.
    will raise a error if one or more are - invalid.
    """
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    return src_valid, tar_valid


def show_message_box(msg_title, msg_text, msg_icon, msg_type):
    """ general messageBox method """
    """ general window initialization : """
    general_window = Tk()
    general_window.eval('tk::PlaceWindow %s center' % general_window.winfo_toplevel())
    general_window.withdraw()

    result = messagebox._show(msg_title, msg_text, msg_icon, msg_type)

    general_window.deiconify()
    general_window.destroy()
    """ ---End general window--- """
    return result
