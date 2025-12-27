import tkinter as tk
from tkinter import scrolledtext, filedialog
import pandas as pd
import Surveying

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

# -------------------------
# 讀取檔案
# -------------------------
def open_file():
    global content
    file_path = filedialog.askopenfilename(
        title="upload file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        parser(df)
        show_content()
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"讀取檔案失敗：\n{e}")

# -------------------------
# 解析 Excel
# -------------------------
def parser(df):
    # 清空舊資料（很重要）
    content.clear()
    BS.clear()
    FS.clear()
    L.clear()

    content.extend(df.values.tolist())

    for row in content:
        BS.append(row[0])
        FS.append(row[1])
        L.append(row[2])

# -------------------------
# 顯示 Excel 內容
# -------------------------
def show_content():
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "BS\tFS\tL\n")
    output_box.insert(tk.END, "-" * 30 + "\n")

    for row in content:
        output_box.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\n")

# -------------------------
# 計算並輸出結果
# -------------------------
def output():
    output_box.config(state=tk.NORMAL)
    #get value if is not in globals give a fuck
    text1=inputbar1.get() if 'inputbar1' in globals() else ""
    text2=inputbar2.get() if 'inputbar2' in globals() else ""
    text3=inputbar3.get() if 'inputbar3' in globals() else ""
    #only run when var is not ""
    if text1:
        output_box.insert(tk.END,text1+'\n')
        inputbar1.delete(0,tk.END)
    if text2:
        output_box.insert(tk.END,text2+'\n')
        inputbar2.delete(0,tk.END)
    if text3:
        output_box.insert(tk.END,text3+'\n')
        inputbar3.delete(0,tk.END)
    output_box.config(state=tk.DISABLED)

# def output():
#     if not BS or not FS:
#         output_box.insert(tk.END, "\n尚未讀取資料\n")
#         return

#     result = Surveying.level_high(BS, FS)

#     output_box.insert(tk.END, "\n計算結果：\n")
#     output_box.insert(tk.END, str(result) + "\n")

# -------------------------
# 按鈕
# -------------------------
tk.Button(window, text="upload file", command=open_file)\
    .grid(row=0, column=0, padx=30, pady=30, sticky="w")

tk.Button(window, text="calculate", command=output)\
    .grid(row=0, column=5, padx=30, pady=30, sticky="e")
# -------------------------
# 輸入框
# -------------------------
# bar1x=200
bar1input=tk.StringVar()
bar1x=0
inputbarLabel=tk.Label(window, text="塞拎娘:")
inputbarLabel.grid(row=0,column=1,padx=bar1x,pady=10,sticky="w")
inputbar1=tk.Entry(window,width=5,textvariable=bar1input)
inputbar1.grid(row=0,column=1 ,padx=bar1x+50,pady=10,sticky="w")

# bar2x=0
# inputbarLabel=tk.Label(window, text="塞拎娘:")
# inputbarLabel.grid(row=0,column=2,padx=bar2x,pady=10,sticky="w")
# inputbar2=tk.Entry(window,width=5)
# inputbar2.grid(row=0,column=2 ,padx=bar2x+50,pady=10,sticky="w")

# bar3x=0
# inputbarLabel=tk.Label(window, text="塞拎娘:")
# inputbarLabel.grid(row=0,column=3,padx=bar3x,pady=10,sticky="w")
# inputbar3=tk.Entry(window,width=5)
# inputbar3.grid(row=0,column=3 ,padx=bar3x+50,pady=10,sticky="w")
# -------------------------
# 輸出框
# -------------------------
output_box = scrolledtext.ScrolledText(window, width=80, height=25)
output_box.grid(row=1, column=0, columnspan=6, padx=50, pady=20, sticky="nsew")
output_box.config(state=tk.DISABLED)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
