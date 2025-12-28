import math
import matplotlib.pyplot as plt

class Surveying:
    def __init__(self, BS, FS, L, origin_high):
        self.BS = BS
        self.FS = FS
        self.L = L
        self.K = sum(L) / 2
        self.origin_high = origin_high

        # 初始化各列表
        self.High = []
        self.vi = []
        self.correction_level_high = []
        self.after_high = []

        # 計算
        self.dH_list = self._level_high()
        self.V_list = self._Correction_value()
        self.correction_level_high_list = self._Correction_level_high()
        self.after_high_list = self._After_High()

    # --- 計算高程差 ---
    def _level_high(self):
        self.High = [bs - fs for bs, fs in zip(self.BS, self.FS)]
        return self.High

    # --- 計算改正值 ---
    def _Correction_value(self):
        WH = round(sum(self.dH_list), 3)
        total_len = sum(self.L)
        self.vi = [-WH * (l / total_len) for l in self.L]
        return self.vi

    # --- 計算改正後高程差 ---
    def _Correction_level_high(self):
        self.correction_level_high = [dh + v for dh, v in zip(self.dH_list, self.vi)]
        return self.correction_level_high

    # --- 計算高程 ---
    def _After_High(self):
        current_h = self.origin_high
        self.after_high = []
        for c_l_h in self.correction_level_high:
            current_h += c_l_h
            self.after_high.append(current_h)
        return self.after_high

    # --- 容許誤差計算 ---
    def _Allowable_Misclosure(self, thenumber=20):
        WH_mm = abs(sum(self.dH_list) * 1000)
        C = abs(thenumber * math.sqrt(self.K))
        return round(WH_mm, 2), round(C, 2)

    def get_C(self):
        _, C = self._Allowable_Misclosure()
        return C

    def get_WH_mm(self):
        WH_mm, _ = self._Allowable_Misclosure()
        return WH_mm

    def Allowable_Misclosure(self, thenumber=20):
        WH_mm, C = self._Allowable_Misclosure(thenumber)
        print("-" * 30)
        print(f"閉合差 Wh = {WH_mm} mm")
        print(f"容許值 C  = {C} mm")
        if WH_mm < C:
            print("結果: 合格 (在容許誤差範圍內)")
        else:
            print("結果: 不合格 (超出容許誤差範圍)")

    # --- 輸出表格 ---
    def output_tables(self):
        result = ""
        result += "\n" + "="*85 + "\n"
    
        # 表頭
        header = "{:<5} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}"
        result += header.format("測站", "BS", "FS", "高程差dH", "改正數v", "改正dH", "高程") + "\n"
    
        # 閉合差與容許值
        result += f"閉合差: {self.get_WH_mm()} mm\n"
        result += f"容許值: {self.get_C()} mm\n"
        result += "-"*85 + "\n"

        # 起點
        result += f"{'Start':<5} {'-':<10} {'-':<10} {'-':<10} {'-':<10} {'-':<10} {self.origin_high:<10.3f}\n"

        # 計算過程
        for i in range(len(self.BS)):
            result += "{:<5} {:<10} {:<10} {:<10.3f} {:<10.4f} {:<10.3f} {:<10.3f}\n".format(
                i + 1,
                self.BS[i],
                self.FS[i],
                self.dH_list[i],
                self.V_list[i],
                self.correction_level_high_list[i],
                self.after_high_list[i]
            )

        result += "="*85 + "\n"

        return result

    # --- 繪圖 ---
    def draw_output(self):
        cumulative_dist = [0]
        current_dist = 0
        for dist in self.L:
            current_dist += dist
            cumulative_dist.append(current_dist)

        all_elevations = [self.origin_high] + self.after_high_list

        plt.figure(figsize=(10, 6))
        plt.plot(cumulative_dist, all_elevations, marker='o', linestyle='-', color='blue', label='Elevation')
        for i, txt in enumerate(all_elevations):
            plt.annotate(f"{txt:.2f}", (cumulative_dist[i], all_elevations[i]),
                         textcoords="offset points", xytext=(0, 10), ha='center')
        plt.title('Leveling Profile')
        plt.xlabel('Cumulative Distance (km)')
        plt.ylabel('Elevation (m)')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__=="__main__":
    # --- 原始數據 ---
    BS = [1.331, 0.223, 0.962, 0.466, 11.943, 12.538, 12.763]
    FS = [8.374, 7.915, 11.722, 8.711, 2.585, 0.695, 0.215]
    L  = [0.12, 0.12, 0.11, 0.10, 0.16, 0.15, 0.12]
    origin_high = 53.182

    # test = Surveying(BS, FS, L, origin_high)
    # print(test.output_tables())
    # test.draw_output()
