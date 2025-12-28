import tkinter as tk
import pandas as pd
from Surveying import Surveying
from tkinter import scrolledtext, filedialog
from tkinter import ttk


# -------------------------
# 主視窗
# -------------------------
window = tk.Tk()
window.title("python project")
window.geometry("1000x600")

# -------------------------
# 全域資料
# -------------------------
content = []
BS = []
FS = []
L = []
surveying=Surveying()
# -------------------------
# 讀取檔案
# -------------------------
df=[]
def open_file():
    global df
    global content
    file_path = filedialog.askopenfilename(
        title="upload file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    print(file_path)

    if not file_path:
        output_box.insert(tk.END, f"讀取檔案失敗：\n{e}")
        return

    try:
        df = pd.read_excel(file_path)
        parser(df)
        # show_content()
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"讀取檔案失敗：\n{e}")

# -------------------------
# 解析 Excel
# -------------------------
def parser(df):
    global surveying
    df = df.dropna(subset=[df.columns[1], df.columns[2]]) 

    content.clear()
    BS.clear()
    FS.clear()
    L.clear()

    BS.extend(pd.to_numeric(df.iloc[:, 1], errors='coerce').tolist())
    FS.extend(pd.to_numeric(df.iloc[:, 2], errors='coerce').tolist())
    L.extend(pd.to_numeric(df.iloc[:, 3], errors='coerce').tolist())

    
    origin_h = float(origin_hight.get())
    surveying.BS = BS
    surveying.FS = FS
    surveying.L = L
    surveying.origin_high = origin_h
    
    surveying.after_high_list = [] 
    surveying.calculate_all()

def show_content():
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, BS)
    output_box.insert(tk.END, '\n')
    output_box.insert(tk.END, FS)
    output_box.insert(tk.END, '\n')
    output_box.insert(tk.END, L)
    output_box.insert(tk.END, '\n')
    output_box.insert(tk.END, origin_hight.get())
    output_box.insert(tk.END, '\n')
    output_box.insert(tk.END, select_allowable_misclosure.get())
    output_box.insert(tk.END, '\n')
    output_box.config(state=tk.DISABLED)

# -------------------------
# 計算並輸出結果
# -------------------------


def output():
    global surveying

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, surveying.check_misclosure() + "\n")
    output_box.insert(tk.END, surveying.display_table() + "\n")
    output_box.config(state=tk.DISABLED)


def run():
    global df
    parser(df)
    output()
# -------------------------
# 按鈕
# -------------------------
tk.Button(window, text="upload file", command=open_file)\
    .grid(row=0, column=0, padx=30, pady=30, sticky="w")

tk.Button(window, text="calculate", command=run)\
    .grid(row=0, column=5, padx=30, pady=30, sticky="e")
# -------------------------
# 輸入框
# -------------------------
bar1input=tk.StringVar()
bar1x=0
origin_hight_input_x=200
origin_hight_label=tk.Label(window, text="Origin Hight:")
origin_hight_label.grid(row=0,column=0 ,padx=origin_hight_input_x,pady=10,sticky="w")
origin_hight=tk.Entry(window,width=5)
origin_hight.grid(row=0,column=0 ,padx=origin_hight_input_x+100,pady=10,sticky="w")
origin_hight.insert(0, "57.3")

inputbarLabel=tk.Label(window, text="閉合差:")
inputbarLabel.grid(row=0,column=3,padx=bar1x,pady=10,sticky="w")
select_allowable_misclosure=ttk.Combobox(window,width=5,values=[2,7,10,20],state="readonly")
select_allowable_misclosure.grid(row=0,column=3 ,padx=bar1x+50,pady=10,sticky="w")
select_allowable_misclosure.set(7)
# -------------------------
# 輸出框
# -------------------------
output_box = scrolledtext.ScrolledText(window, width=80, height=25)
output_box.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")
output_box.config(state=tk.DISABLED)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
