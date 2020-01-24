import os
from PyPDF2 import PdfFileMerger
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

pdfs = list(filedialog.askopenfilenames())
target = filedialog.asksaveasfilename()
if target:
    if not target.endswith('.pdf'):
        target = target + '.pdf'

    ##for paths, dirs, files in os.walk(directory):
    ##    for file in files:
    ##        if file.endswith('.pdf'):
    ##            filename = '{}/{}'.format(directory,file)
    ##            pdfs.append(filename)

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(target)
    merger.close()
