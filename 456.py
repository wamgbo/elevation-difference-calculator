import math
import matplotlib.pyplot as plt

# --- 原始數據 ---
BS = [1.331, 0.223, 0.962, 0.466, 11.943, 12.538, 12.763]
FS = [8.374, 7.915, 11.722, 8.711, 2.585, 0.695, 0.215]
L  = [0.12, 0.12, 0.11, 0.10, 0.16, 0.15, 0.12]
origin_high = 53.182

# 全域變數初始化
High = []
vi = []
correction_level_high = []
after_high = []

# --- 1. 計算高程差 ---
def level_high(BS, FS):
    n = len(BS)
    global High
    for i in range(n):
        dh = BS[i] - FS[i]
        High.append(dh)
    # return 必須移到迴圈外面，才能回傳完整的列表
    return High

dH_list = level_high(BS, FS)
print(f"總高程差 (Wh) = {round(sum(dH_list), 3)} m")

# --- 2. 計算改正值 ---
def Correction_value(dH_list):
    WH = round(sum(dH_list), 3)
    n = len(dH_list)
    global vi
    total_len = sum(L)
    
    for i in range(n):
        v = -WH * (L[i] / total_len) # 修正公式寫法
        vi.append(v)
    return vigit

V_list = Correction_value(dH_list)
print(f"總改正值檢查 = {round(sum(V_list), 3)} m")

# --- 3. 計算改正後高程差 ---
def Correction_level_high(dH_list):
    global High
    global vi
    global correction_level_high
    n = len(dH_list)
    
    for i in range(n):
        c_l_h_i = High[i] + vi[i]
        correction_level_high.append(c_l_h_i)
    return correction_level_high

correction_level_high_list = Correction_level_high(dH_list)

# --- 4. 計算高程 ---
def After_High(dH_list):
    global origin_high
    global correction_level_high
    global after_high
    
    # 這裡使用一個暫存變數來累加，避免一直修改 global origin_high 的初始值
    current_h = origin_high 
    n = len(dH_list)
    
    for i in range(n):
        current_h += correction_level_high[i]
        after_high.append(current_h)
    return after_high

after_high_list = After_High(dH_list)

# --- 5. 容許閉合差 ---
K = sum(L) / 2 # 依照題目圖示 K = Sigma L / 2

def Allowable_Misclosure(dH_list):
    global K
    # 修正: 先加總再乘 1000 換算成 mm
    WH_mm = abs(sum(dH_list) * 1000) 
    
    # 公式: 20 * sqrt(K)
    C = abs(20 * math.sqrt(K))
    
    print("-" * 30)
    print(f"閉合差 Wh = {round(WH_mm, 2)} mm")
    print(f"容許值 C  = {round(C, 2)} mm")
    
    if WH_mm < C:
        print("結果: 合格 (在容許誤差範圍內)")
    else:
        print("結果: 不合格 (超出容許誤差範圍)")

Allowable_Misclosure(dH_list)

# ==========================================
#  輸出表格
# ==========================================
print("\n" + "="*85)
header = "{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}"
print(header.format("測站", "BS", "FS", "高程差dH", "改正數v", "改正dH", "高程"))
print("-" * 85)

# 顯示起點
print(f"{'Start':<5} {'-':<10} {'-':<10} {'-':<10} {'-':<10} {'-':<10} {53.182:<10.3f}")

# 顯示計算過程
for i in range(len(BS)):
    print("{:<5} {:<10} {:<10} {:<10.3f} {:<10.4f} {:<10.3f} {:<10.3f}".format(
        i + 1,
        BS[i],
        FS[i],
        dH_list[i],
        V_list[i],
        correction_level_high_list[i],
        after_high_list[i]
    ))
print("="*85)

# ==========================================
#  繪圖部分
# ==========================================

# 1. 計算累積距離 (X軸)
cumulative_dist = [0]
current_dist = 0
for dist in L:
    current_dist += dist
    cumulative_dist.append(current_dist)

# 2. 準備高程數據 (Y軸，含起點)
all_elevations = [53.182] + after_high_list

# 3. 設定畫布
plt.figure(figsize=(10, 6))

# 4. 畫線
plt.plot(cumulative_dist, all_elevations, 
         marker='o', linestyle='-', color='blue', label='Elevation')

# 5. 標註數值
for i, txt in enumerate(all_elevations):
    plt.annotate(f"{txt:.2f}", 
                 (cumulative_dist[i], all_elevations[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Leveling Profile')
plt.xlabel('Cumulative Distance (km)')
plt.ylabel('Elevation (m)')
plt.grid(True)
plt.legend()
plt.show()