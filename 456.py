import math
BS = [1.331,0.223,0.962,0.466,11.943,12.538,12.763]
FS = [8.374,7.915,11.722,8.711,2.585,0.695,0.215]
L=[0.12,0.12,0.11,0.10,0.16,0.15,0.12]
origin_high=53.182
High = []
vi=[]
correction_level_high=[]
after_high=[]
def level_high(BS, FS):#高程差
    n = len(BS)
    global High
    for i in range(n):
        dh = BS[i] - FS[i]#BS-前一個FS
        High.append(dh)
        print("ΔH", i+1, "=", round(dh,3))
    return High
dH_list = level_high(BS, FS)
print("\n總高程差 =",round(sum(dH_list),3))
def Correction_value(dH_list):#改正值
    WH = round(sum(dH_list),3)
    n = len(dH_list)
    global vi
    for i in range(n):
        v = -WH*L[i]/sum(L)# 每站改正量（等分）
        vi.append(v)
        print("v", i+1, "=", round(v,3))
    return v
V_list =  Correction_value(dH_list)
print("\n總改正值",-round(sum(dH_list),3))



def Correction_level_high(dH_list):#改正後高程差
    global High
    global vi
    global correction_level_high
    n = len(dH_list)
    for i in range(n):
        c_l_h_i=High[i]+vi[i]
        correction_level_high.append(c_l_h_i)
        print("correction_level_high",i+1,"=", round(c_l_h_i,3))
correction_level_high_list=Correction_level_high(dH_list)


def After_High(dH_list):#高程
    global origin_high
    global correction_level_high
    n = len(dH_list)
    for i in range(n):
        origin_high+=correction_level_high[i]
        after_high.append(origin_high)
        print("After_High",i+1,"=",round(origin_high,3))
after_high_list=After_High(dH_list)


K=sum(L)/2

def Allowable_Misclosure(dH_list):#容許閉合差
    global K
    WH = round(sum(dH_list*1000),3)
    C=abs(20*math.sqrt(K))
    if C<WH:
        print("C=",round(C,3),"<",WH,",為普通誤差範圍內")
    else:
        print("C=",round(C,3),">",WH,",為普通誤差範圍外")
allowable_misclosure_list=Allowable_Misclosure(dH_list)