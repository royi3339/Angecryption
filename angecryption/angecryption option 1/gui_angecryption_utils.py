# Royi Alishayev.

import glob
from utils import check_key, check_iv, check_png, check_file


def dir_func(file_or_path):
    """
    Function that return the list of the files/folder of a path as string, if not exists - return ''
    return 1 big string as a result.
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
    res = list(map(lambda x:x.split("\\")[-1], file_res_as_list))
    return res


def check_enc_dec_funcs_params(src_param, key_param, iv_param):
    """
    checking if the values that "enc dec funcs" should get - are valid.
    """
    src_valid = check_png(src_param)
    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, key_valid, iv_valid


def check_angecryption_funcs_params(src_param, tar_param, key_param, iv_param):
    """
    checking if the values that "angecryption funcs" should get - are valid.
    """
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    key_valid = check_key(key_param)
    iv_valid = check_iv(iv_param)
    return src_valid, tar_valid, key_valid, iv_valid


def check_cleaning_funcs_params(src_param):
    """
    checking if the values that "cleaning funcs" should get - are valid.
    """
    src_valid = check_png(src_param)
    return src_valid


def check_combine_file_in_png_params(src_param, tar_param):
    """
    checking if the values that "combine_file_in_png()" should get - are valid.
    """
    src_valid = check_png(src_param)
    tar_valid = check_file(tar_param)
    return src_valid, tar_valid
