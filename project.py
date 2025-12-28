import tkinter as tk
import pandas as pd
import Surveying
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

# -------------------------
# 讀取檔案
# -------------------------
def open_file():
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
        BS.append(row[1])
        FS.append(row[2])
        L.append(row[3])

# -------------------------
# 顯示 Excel 內容
# -------------------------
# def show_content():
#     output_box.delete("1.0", tk.END)
#     output_box.insert(tk.END, "BS\tFS\tL\n")
#     output_box.insert(tk.END, "-" * 30 + "\n")

#     for row in content:
#         output_box.insert(tk.END, f"{row[0]}\t{row[1]}\t{row[2]}\n")

def show_content():
    if not content:
        return
    # 將 content 轉回 DataFrame（或直接使用原 df）
    df_display = pd.DataFrame(content)

    # 將 DataFrame 轉成字串
    df_str = df_display.to_string(index=False, header=True)

    # 插入到 scrolledtext
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, df_str)
    output_box.config(state=tk.DISABLED)

# -------------------------
# 計算並輸出結果
# -------------------------
# def output():
#     print(select_allowable_misclosure.get())

def output():
    if not BS or not FS:
        output_box.insert(tk.END, "\n尚未讀取資料\n")
        return

    result = Surveying.level_high(BS, FS)
    print(result)

    output_box.insert(tk.END, "\n計算結果：\n")
    output_box.insert(tk.END, str(result) + "\n")

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
inputbarLabel=tk.Label(window, text="閉合差:")
inputbarLabel.grid(row=0,column=3,padx=bar1x,pady=10,sticky="w")
select_allowable_misclosure=ttk.Combobox(window,width=5,values=[2,7,10,20])
select_allowable_misclosure.grid(row=0,column=3 ,padx=bar1x+50,pady=10,sticky="w")
# -------------------------
# 輸出框
# -------------------------
output_box = scrolledtext.ScrolledText(window, width=80, height=25)
output_box.grid(row=1, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")
output_box.config(state=tk.DISABLED)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
