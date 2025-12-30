import tkinter as tk
import pandas as pd
from Surveying import Surveying
from tkinter import scrolledtext, filedialog
from tkinter import ttk
import math

# -------------------------
# 主視窗 setup
# -------------------------
window = tk.Tk()
window.title("Elevation Difference Calculator")
window.geometry("1000x700")

# -------------------------
# 全域變數
# -------------------------
surveying = Surveying()
df = []
# 用來儲存讀取到的原始數據 (供計算用)
raw_data = {"BS": [], "FS": [], "L": []}

# -------------------------
# 輔助：尋找欄位索引
# -------------------------
def find_col_index(columns, keywords, default_idx):
    """
    在 columns 中搜尋包含 keywords 關鍵字的欄位。
    如果有找到，回傳 index；沒找到，回傳 default_idx。
    """
    for idx, col in enumerate(columns):
        col_str = str(col)
        for kw in keywords:
            if kw in col_str:
                return idx, col_str
    return default_idx, "未偵測到 (使用預設)"

# -------------------------
# 讀取檔案
# -------------------------
def open_file():
    global df
    
    file_path = filedialog.askopenfilename(
        title="Upload File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    print(file_path)

    if not file_path:
        log_message("未選擇檔案。")
        return

    try:
        # 讀取 Excel
        df = pd.read_excel(file_path)
        
        # 執行解析
        success, msg = parser(df)
        
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        if success:
            output_box.insert(tk.END, "✅ 檔案讀取成功！\n" + msg + "\n請按下 [Calculate] 進行計算。\n")
        else:
            output_box.insert(tk.END, "❌ 解析失敗：\n" + msg + "\n")
        output_box.config(state=tk.DISABLED)
        
    except Exception as e:
        log_message(f"讀取檔案發生錯誤：\n{e}")

# -------------------------
# 解析資料 
# -------------------------
def parser(df_input):
    global surveying, raw_data
    
    if isinstance(df_input, list):
        return False, "無資料"

    try:
        cols = df_input.columns
        
        # 1. 智慧偵測欄位 
        idx_bs, name_bs = find_col_index(cols, ["後視", "BS", "Back"], 1)
        idx_fs, name_fs = find_col_index(cols, ["前視", "FS", "Fore"], 2)
        idx_l, name_l   = find_col_index(cols, ["距離", "Dist", "L", "Length"], 3)
        
        debug_msg = (
            f"--- 欄位偵測結果 ---\n"
            f"後視 (BS) : 欄位 {idx_bs} [{name_bs}]\n"
            f"前視 (FS) : 欄位 {idx_fs} [{name_fs}]\n"
            f"距離 (Dist): 欄位 {idx_l} [{name_l}]\n"
            f"--------------------"
        )

        # 2. 讀取數據 
        bs_list = pd.to_numeric(df_input.iloc[:, idx_bs], errors='coerce').fillna(0).tolist()
        fs_list = pd.to_numeric(df_input.iloc[:, idx_fs], errors='coerce').fillna(0).tolist()
        l_list  = pd.to_numeric(df_input.iloc[:, idx_l],  errors='coerce').fillna(0).tolist()

        # 更新全域變數 
        raw_data["BS"] = bs_list
        raw_data["FS"] = fs_list
        raw_data["L"] = l_list

        # 同步更新 Surveying 物件 
        try:
            origin_h = float(origin_high.get())
        except:
            origin_h = 0.0

        surveying.BS = bs_list
        surveying.FS = fs_list
        surveying.L = l_list
        surveying.origin_high = origin_h
        surveying.after_high_list = []
        surveying.calculate_all()
        
        return True, debug_msg

    except Exception as e:
        return False, str(e)

# -------------------------
# 計算與輸出
# -------------------------
def output():
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)

    try:
        # 1. 取得設定
        try:
            m_constant = float(select_allowable_misclosure.get())
        except:
            m_constant = 20.0
            
        is_round_trip = round_trip_var.get()
        grade_map = {3: "一等", 7: "二等", 10: "三等", 20: "四等"}
        grade_name = grade_map.get(int(m_constant), "自訂")

        # 2. 使用 raw_data 進行計算 
        sum_bs = sum(raw_data["BS"])
        sum_fs = sum(raw_data["FS"])
        wh = sum_bs - sum_fs  # 閉合差

        sum_dist = sum(raw_data["L"])
        
        # 3. K 值處理
        if is_round_trip:
            K_km = sum_dist / 2
            k_note = "(往返平均 K/2)"
        else:
            K_km = sum_dist
            k_note = "(單程總和)"

        # 4. 容許誤差
        if K_km > 0:
            allowable_c = abs(m_constant * math.sqrt(K_km))
        else:
            allowable_c = 0.0

        # 5. 判定
        is_passed = abs(wh) <= allowable_c
        if is_passed:
            status = "✅ 合格 (Pass)"
        else:
            diff = abs(wh) - allowable_c
            status = f"❌ 不合格 (超限 {diff:.2f} mm)"

        # 6. 顯示結果
        report = (
            f"--- 檢核報告 (Debug Mode) ---\n"
            f"等級與模式      : {grade_name} (m={int(m_constant)}), {k_note}\n"
            f"---------------------------\n"
            f"後視總和 (ΣBS)  : {sum_bs:.3f} m\n"
            f"前視總和 (ΣFS)  : {sum_fs:.3f} m\n"
            f"閉合差 (Wh)     : {wh:.3f} m (={wh*1000:.1f} mm)\n"
            f"---------------------------\n"
            f"總距離 (Total L): {sum_dist:.3f} km\n"
            f"計算用 K 值     : {K_km:.3f} km\n"
            f"容許閉合差 (C)  : {allowable_c:.2f} mm\n"
            f"---------------------------\n"
            f"最終判定        : {status}\n"
            f"---------------------------\n"
        )
        output_box.insert(tk.END, report)
        
        # 顯示詳細表格
        try:
            table = surveying.display_table()
            output_box.insert(tk.END, "\n【計算明細表】\n" + str(table) + "\n")
        except:
            pass

    except Exception as e:
        output_box.insert(tk.END, f"計算錯誤: {e}\n")
    
    output_box.config(state=tk.DISABLED)

# -------------------------
# 輔助函式
# -------------------------
def log_message(msg):
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, msg + "\n")
    output_box.config(state=tk.DISABLED)

def run():
    if isinstance(df, list) and len(df) == 0:
        log_message("⚠️ 請先上傳檔案 (Upload File)！")
        return
    
    # 重新解析一次確保設定正確
    parser(df)
    output()
    try:
        surveying.plot_profile()
    except:
        pass

# -------------------------
# GUI 介面
# -------------------------
tk.Button(window, text="Upload File", command=open_file)\
    .grid(row=0, column=0, padx=20, pady=20, sticky="w")

tk.Button(window, text="Calculate", command=run, bg="#dddddd", font=('Arial', 10, 'bold'))\
    .grid(row=0, column=6, padx=20, pady=20, sticky="   e")

tk.Label(window, text="Origin High:").grid(row=0, column=1, sticky="e")
origin_high = tk.Entry(window, width=8)
origin_high.grid(row=0, column=2, padx=5, sticky="w")
origin_high.insert(0, "53.182")

tk.Label(window, text="精度等級(m):").grid(row=0, column=3, sticky="e")
select_allowable_misclosure = ttk.Combobox(window, width=5, values=[3, 7, 10, 20], state="readonly")
select_allowable_misclosure.grid(row=0, column=4, padx=5, sticky="w")
select_allowable_misclosure.set(20)

round_trip_var = tk.IntVar()
round_trip_check = tk.Checkbutton(
    window, 
    text="往返/環線測量 (K/2)", 
    variable=round_trip_var,
    onvalue=1, 
    offvalue=0
)
round_trip_check.grid(row=0, column=5, padx=10, sticky="w")
round_trip_check.select()

output_box = scrolledtext.ScrolledText(window, width=90, height=35)
output_box.grid(row=1, column=0, columnspan=7, padx=20, pady=10, sticky="nsew")
output_box.config(state=tk.DISABLED)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()