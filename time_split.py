import os
import traceback
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import time_range


TIME_COL = 'time'
DATE_COL = 'date'


def main():
    root = tk.Tk()
    root.withdraw()
    path, is_folder, is_valid = prompt_user(root)
    
    if not is_valid:
        print("Faulty file!")
        return
    save_path = filedialog.askdirectory(title="Save Folder", parent=root)
    extension_name = simpledialog.askstring("Input", "Save name extension?")
    start, end = time_range.open_popup(root)
    if not start or not end:
        messagebox.showwarning("Program Terminate", "Program Terminated")
        return
    if save_path is None:
        return
    if extension_name is None:
        extension_name = "ble_data"
    if is_folder:
        process_folder(start, end, path, extension_name,  save_path)
    else:
        process_file(start, end, path, extension_name,  save_path)
        return


def prompt_user(root):
    is_valid = True
    is_folder = True
    path = ""
    user_response = simpledialog.askstring("Input", "Process folder? (y/n)")
    if user_response is None:
        return path, is_folder, False
    if user_response.lower() != 'y':
        path = filedialog.askopenfilename(
            title = "Select a file",
            filetypes = (("excel files", "*.xlsx"), ("csv files", "*.csv")),
            parent=root
        )
        is_folder = False
    else:
        path = filedialog.askdirectory(title="Folder of ble data", parent=root)
    
    if not path:
        is_valid = False
    return path, is_folder, is_valid



def process_folder(start, end, path, extension_name, save_path):
    is_success = True
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        is_success = is_success and process_file(start, end, file_path, extension_name, save_path)

def process_file(start, end, path, extension_name, save_path):
    check_if_open(path)
    try:
        df = None
        if os.path.isfile(path):
            filetype = os.path.splitext(path)[1].lower()
            if filetype == '.csv':
                df = pd.read_csv(path)
            elif filetype =='.xlsx':
                df = pd.read_excel(path)
            else:
                return
            df = process_df(df, start, end)
            save_to_xlsx(df, path, save_path, extension_name)
            
        
    except Exception as e:
        traceback.print_exc()
    
    return


def process_df(df, start, end):
    df['datetime'] = pd.to_datetime(df[DATE_COL] + ' ' + df[TIME_COL], format='%m/%d/%Y %H:%M:%S')
    filtered_df = df[(df['datetime'] >= start) & (df['datetime'] <= end)]
    filtered_df = filtered_df.drop('datetime', axis=1)
    return filtered_df
    
def save_to_xlsx(df, path,  save_path, extension):
    parsed_file_name = os.path.splitext(os.path.basename(path))[0] + '_' + extension +  '.xlsx'
    full_path = os.path.join(save_path, parsed_file_name)
    if os.path.exists(full_path):
        os.remove(full_path)
    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Time Filtered Data')
    return

def check_if_open(path):
    try:
        with open(path, "rb+"):
            return
    except PermissionError:
        messagebox.showwarning("File Open", "Please close file before continuing program")


if __name__ == "__main__":
    main()