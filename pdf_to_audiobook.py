import os
import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def select_file():
    global open_flag
    global filepath
    global name

    filepath = askopenfilename(filetypes=[('text file', '*.pdf')])
    name = os.path.basename(filepath)

    if not filepath:
        return

    root.title(f'{name} | Convert PDF to audiobook')
    file_name.config(text=f'File: {name}')
    open_flag = True
    return filepath, name


def save():
    global open_flag
    global filepath
    global name

    language = language_select.get()

    name = os.path.basename(filepath)

    if not filepath:
        return

    with open(filepath, 'rb') as f:

        reader = PyPDF2.PdfFileReader(f, strict=False)

        audio = pyttsx3.init()
        audio.setProperty('rate', 150)

        en_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
        pl_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAULINA_11.0'
        if language == 'English':
            audio.setProperty('voice', en_voice_id)
        elif language == 'Polish':
            audio.setProperty('voice', pl_voice_id)

        for page in range(reader.numPages):
            next_page = reader.getPage(page)
            content = next_page.extractText()

            if name.endswith('.pdf'):
                audio.save_to_file(content, f'{name[:-4:]}.mp3')
                audio.runAndWait()
            else:
                audio.save_to_file(content, f'{name}.mp3')
                audio.runAndWait()

def convert_to_audio():
    save()


def read():
    terms_window = tk.Tk()
    terms_window.geometry('600x620')
    terms_window.resizable(False, False)
    terms_window.config(background='#faf0e6')
    terms_window.title('Terms & Conditions')
    terms_window_text = tk.Label(terms_window, background='#faf0e6')
    terms_window_text.pack()
    terms_window_close_button = tk.Button(terms_window, text='Close', command=terms_window.destroy)
    terms_window_close_button.pack()


def error_window():
    error = tk.Tk()
    error.geometry('300x50')
    error.config(background='#faf0e6')
    error.resizable(False, False)
    error.title('Error')
    error_label = tk.Label(error, text='Error', background='#faf0e6')
    error_label.pack()
    error_close_button = tk.Button(error, text='Close', command=error.destroy)
    error_close_button.pack()


open_flag = False
filepath = ''
name = None

root = tk.Tk()
root.title('Convert PDF to audiobook')
root.geometry('600x300')
root.resizable(False, False)
root.config(background='#faf0e6')

frame = tk.Frame(root, background='#faf0e6')
frame.pack()

file_name = tk.Label(frame, width=50, font=('Arial', 16), text='File:', background='#faf0e6')
file_name.grid(row=0, column=0, pady=5)

open_button = tk.Button(frame, width=20, text='Select File', command=select_file)
open_button.grid(row=1, column=0, pady=10)

language_select = ttk.Combobox(frame, width=20, state='readonly')
language_select['values'] = ['English', 'Polish']
language_select.current(0)
language_select.grid(row=2, column=0, pady=10)

convert_button = tk.Button(frame, font=('Arial', 26), text='Convert', command=convert_to_audio)
convert_button.grid(row=3, column=0, pady=10)

read_button = tk.Button(frame, width=20, text='Read more', command=read)
read_button.grid(row=4, column=0, pady=40)

root.mainloop()
