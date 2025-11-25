import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import pandas as pd
import Surveying

window = tk.Tk()
window.title("python project")
window.geometry("1000x600")  # 寬x高

content=[]
BS=[]
FS=[]
L=[]
#button function
"""讀取檔案"""
def open_file():
    global df
    global content
    file_path = filedialog.askopenfilename(title="upload file")
    try:
        if file_path:
            df = pd.read_excel('./BS_FS_L.xlsx')
            parser(df)
    except ValueError as e:
        print("wrong file type!")
"""解析xlsx格式"""
def parser(df):
    content=df.values.tolist()
    for i in content:
        BS.append(i[0])
        FS.append(i[1])
        L.append(i[2])
    print(BS,FS,L)
"""輸出到gui"""
def output():
    global content
    r=Surveying.level_high(BS,FS)
    print(r)
    # output=content[4:]
    # print(content[0])
    # for i in content:
    #     print(i)
    # output_box.delete("1.0",tk.END)
    # output_box.insert(tk.END,content)
def fname(arg):
    pass
#button
#file
button = tk.Button(window, text="upload file", command=open_file)
button.grid(row=0, column=0, sticky="w",padx=30,pady=30)
#calculate
button = tk.Button(window, text="calculate",command=output)
button.grid(row=0, column=1, sticky="se",padx=30,pady=30)
#output
output_box = scrolledtext.ScrolledText(window,width=80,height=25)
output_box.grid(row=1,column=0,columnspan=2,sticky='nswe',padx=50,pady=20)


window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
