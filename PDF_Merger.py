import tkinter as tk
from tkinter import messagebox
from TkinterDnD2 import DND_FILES, TkinterDnD
import os
from PyPDF2 import PdfFileMerger
from pathlib import Path

merger = PdfFileMerger()

def drop_inside_list_box(event):
    listb.insert("end", event.data)

def clearall():
    listb.delete(0,'end')
    submit_button["state"] = "active"

def _parse_drop_files(filename):
    size = len(filename)
    res = []  # list of file paths
    name = ""
    idx = 0
    while idx < size:
        if filename[idx] == "{":
            j = idx + 1
            while filename[j] != "}":
                name += filename[j]
                j += 1
            res.append(name)
            name = ""
            idx = j
        elif filename[idx] == " " and name != "":
            res.append(name)
            name = ""
        elif filename[idx] != " ":
            name += filename[idx]
        idx += 1
    if name != "":
        res.append(name)
    return res


files_list = []
def main_func():
    submit_button["state"] = "disable"
    
    if len(listb.curselection()) == 0:
        tk.messagebox.showerror('No File Selected','Please select your files after dropiing them in the application.')
        submit_button["state"] = "active"
        return
    
    for x in listb.curselection():
        if listb.get(x) != '':
            if '.pdf' not in listb.get(x):
                tk.messagebox.showerror('Unsupported File Type','This program only supports pdf files at this time.')
                clearall()
                return
            files_list.append(listb.get(x))


    files_string = ' '.join([str(file) for file in files_list])

    final_list = _parse_drop_files(files_string)

    downloads_path = str(Path.home() / "Downloads")
    downloads_path = downloads_path.replace('\\\\', '\\')
    
    for path in final_list:
        merger.append(path)

    merger.write(downloads_path +"\Merged_PDF.pdf")
    merger.close()
    clearall()


root = TkinterDnD.Tk()
root.title('PDF Merger v1.0')
root.geometry('600x200')

listb = tk.Listbox(root, selectmode=tk.MULTIPLE, background="light grey")
listb.pack(fill=tk.X)
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box)

submit_button = tk.Button(root, text='Merge', command= main_func, width=25)
submit_button.pack()


root.mainloop()