#import pandas as pd
import numpy as np
from interpolate_cell import interp_ir

def bat_disc_calc(temp,map_data,dic_config,t0,soc0,t1,pw1,Vp_cell):
    cell_capa,max_v,min_v,max_charge_cell_cur,max_current,max_sys_v,min_sys_v,n_seri,n_para=[dic_config[k] for k in ["cell capa(Ah)","max v","min v","max charge cell cur","max current","max sys v","min sys v","n-seri","n-para"]]

    dt=t1-t0
    if pw1>=0:
        mode="discharge"
    else:
        mode="charge"
    
    pw_cell=pw1/n_para/n_seri
    warning=""
    
    ocv,Ri,Rp,C=interp_ir(soc0,map_data,mode)  #現在のsoc(soc0)におけるセルの内部抵抗を補間計算
    if (ocv-Vp_cell)**2-4*pw_cell*Ri<0:   #電流が発散しているとすると
        #print("発散")
        if pw_cell>=0:
            cur_cell=max_current/n_para
            warning="max current limit"
        else:
            cur_cell=-max_current/n_para
            warning="max current limit"
            if cur_cell<-max_charge_cell_cur:   #充電レートが最大値を超えているならば、そこで頭を押さえる
                cur_cell=-max_charge_cell_cur 
                warning="max cell charge limit"
    else:   #通常の電流計算　最初は過電流判定を行う
        #print("calculation start")
        #a = ocv - Vp_cell
        #b = a**2 - 4 * pw_cell * Ri
        #print("sqrt =", b)
        cur_cell=(ocv-Vp_cell-np.sqrt((ocv-Vp_cell)**2-4*pw_cell*Ri))/(2*Ri)
        #print("calculation end")
        if cur_cell>=max_current/n_para:
            cur_cell=max_current/n_para
            warning="max current limit"
        elif cur_cell<=-max_current/n_para:
            cur_cell=-max_current/n_para
            warning="max current limit"
            if cur_cell<-max_charge_cell_cur:   #充電レートが最大値を超えているならば、そこで頭を押さえる
                cur_cell=-max_charge_cell_cur 
                warning="max cell charge limit"
    v_cell=ocv-cur_cell*Ri-Vp_cell
    if v_cell*n_seri>max_sys_v:
        v_cell=max_sys_v/n_seri
        warning="max system voltage limit"
    if v_cell>max_v:
        v_cell=max_v
        warning="max voltage limit"
    #    cur_cell=(ocv-v_cell-Vp_cell)/Ri
    if v_cell*n_seri<min_sys_v:
        v_cell=min_sys_v/n_seri
        warning="min system voltage limit"
    if v_cell<min_v:
        v_cell=min_v
        warning="min voltage limit" 
    cur_cell=(ocv-v_cell-Vp_cell)/Ri

    Vp_cell=Vp_cell+(cur_cell/C-Vp_cell/(Rp*C))*dt   #次回Vp_cellの更新
    Wloss=cur_cell**2*(Ri+Rp)*dt*n_seri*n_para   #損失電力の計算(J)
    soc0=(soc0/100-cur_cell*dt/cell_capa/3600)*100
    current=cur_cell*n_para
    voltage=v_cell*n_seri

    return temp,soc0,current,voltage,warning,Wloss,Vp_cell
