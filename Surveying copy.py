import math
import matplotlib.pyplot as plt

class Surveying:
    def __init__(self, BS, FS, L, origin_high):
        self.BS = BS
        self.FS = FS
        self.L = L
        self.origin_high = origin_high
        
        self.dH_list = []                
        self.V_list = []                 
        self.corr_dH_list = []           
        self.after_high_list = []        
        self.total_len = sum(L)
        self.K = self.total_len / 2      

    def calculate_all(self):
        self._calc_level_high()
        self._calc_correction_value()
        self._calc_corr_level_high()
        self._calc_final_elevation()

    def _calc_level_high(self):
        self.dH_list = [b - f for b, f in zip(self.BS, self.FS)]
        return self.dH_list

    def _calc_correction_value(self):
        WH = round(sum(self.dH_list), 3)
        self.V_list = [(-WH * (dist / self.total_len)) for dist in self.L]
        return self.V_list

    def _calc_corr_level_high(self):
        self.corr_dH_list = [dh + v for dh, v in zip(self.dH_list, self.V_list)]
        return self.corr_dH_list

    def _calc_final_elevation(self):
        current_h = self.origin_high
        for c_dh in self.corr_dH_list:
            current_h += c_dh
            self.after_high_list.append(current_h)
        return self.after_high_list

    def check_misclosure(self, constant=20):
        WH_mm = abs(sum(self.dH_list) * 1000)
        C = abs(constant * math.sqrt(self.K))
        
        print("-" * 30)
        print(f"閉合差 Wh = {round(WH_mm, 2)} mm")
        print(f"容許值 C  = {round(C, 2)} mm (K={self.K:.3f})")
        
        status = "合格" if WH_mm <= C else "不合格"
        print(f"結果: {status}")
        return WH_mm, C, status

    def display_table(self):
        print("\n" + "="*90)
        header = "{:<5} {:<10} {:<10} {:<12} {:<12} {:<12} {:<10}"
        print(header.format("測站", "BS(m)", "FS(m)", "dH(m)", "v(m)", "Corr_dH(m)", "Elev(m)"))
        print("-" * 90)
        
        print(f"{'Start':<5} {'-':<10} {'-':<10} {'-':<12} {'-':<12} {'-':<12} {self.origin_high:<10.3f}")
        
        for i in range(len(self.BS)):
            print("{:<5} {:<10.3f} {:<10.3f} {:<12.3f} {:<12.4f} {:<12.3f} {:<10.3f}".format(
                i + 1, self.BS[i], self.FS[i], self.dH_list[i], 
                self.V_list[i], self.corr_dH_list[i], self.after_high_list[i]
            ))
        print("="*90)

    def plot_profile(self):
        cumulative_dist = [0]
        curr = 0
        for d in self.L:
            curr += d
            cumulative_dist.append(curr)
            
        all_elevs = [self.origin_high] + self.after_high_list

        plt.figure(figsize=(10, 5))
        plt.plot(cumulative_dist, all_elevs, marker='o', linestyle='-', color='b', label='Elevation Profile')
        
        for x, y in zip(cumulative_dist, all_elevs):
            plt.annotate(f"{y:.3f}", (x, y), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('Surveying Leveling Profile')
        plt.xlabel('Cumulative Distance (km)')
        plt.ylabel('Elevation (m)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    bs_data = [1.331, 0.223, 0.962, 0.466, 11.943, 12.538, 12.763]
    fs_data = [8.374, 7.915, 11.722, 8.711, 2.585, 0.695, 0.215]
    l_data  = [0.12, 0.12, 0.11, 0.10, 0.16, 0.15, 0.12]
    start_h = 53.182

    survey = Surveying(bs_data, fs_data, l_data, start_h)
    survey.calculate_all()
    survey.check_misclosure(constant=20)
    survey.display_table()
    survey.plot_profile()