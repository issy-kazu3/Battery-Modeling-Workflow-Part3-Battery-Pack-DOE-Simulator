#20260728
#セルのRi,Rp,Cを算出する 実際にはτ=CRpを算出

import os
import numpy as np
from scipy.optimize import curve_fit
import tkinter as tk                #file dialog
from tkinter import filedialog      #file dialog
import pandas as pd

def rc_model(t,Rp,C,I):     #VpをフィッティングさせるRC回路のモデル関数
    return I*Rp*(1-np.exp(-t/(Rp*C)))


def analyze_pulse(pulse):
    soc=pulse["soc"].iloc[0]
    t=pulse["ｽﾃｯﾌﾟ時間"].to_numpy()
    ocv=pulse["ocv[v]"].iloc[0]
    V=pulse["電圧[V]"].to_numpy()
    I=np.mean(pulse["電流[A]"])
    Tb= np.mean(pulse["電池温度[℃]"])
    Ta= np.mean(pulse["恒温槽温度[℃]"])
    Ri=(ocv-V[0])/I     # Vはnumpy配列なのでV.iloc[0]という記述はNG
    I_cmd=round(I/5)*5

    # ---RC成分フィッティング--------
    # Riによる電圧降下を除去
    V_rc=ocv-I*Ri-V #V_rcは時系列データ

    #フィット用wrapper Iは平均値を使うので、入力パラメータから除く
    def fit_func(t,Rp,C):
        return rc_model(t,Rp,C,I)

    # 初期値
    p0=[0.002,500]  #フィッティングにおけるRp(Ω),C(F)の初期値

    # popt:フィッティング値、pcov：ばらつき判定(パラメタ共分散行列 2x2行列でRpの信頼性,Cの信頼性,RpとCの相関が入る)、
    # パラメータは、関数、x,y,初期値p0,boundsはRpとCの検討範囲
    try:
        popt,pcov=curve_fit(fit_func,t,V_rc,p0=p0,bounds=([1e-6,1],[1,100000]))

        Rp=popt[0]
        C=popt[1]
    except:
        Rp=np.nan   #np.nanはデーターでないという意味
        C=np.nan
    

    residual = V_rc - fit_func(t,Rp,C)
    rmse=np.sqrt(np.mean(residual**2))

    return {
        "soc":soc,
        "I_cmd":I_cmd,
        "Imean":I,
        "Ri":Ri,
        "Rp":Rp,
        "C":C,
        "tau":Rp*C,
        "ocv":ocv,
        "Tb":Tb,
        "Ta":Ta,
        "rmse":rmse
    }
    





#cwd=os.getcwd()
csv_path=r"D:\Userarea\J0125789\Documents\Python_code\battery"
#input_file=csv_path+r"\60deg_1cell.csv"
root=tk.Tk()                        #file dialog
root.withdraw() # Tkウィンドウを表示しない file dialog
input_file=filedialog.askopenfilename(
#    initialdir=cwd, #現在のディレクトリ(VSCODE)
    initialdir=csv_path,
    title="解析用のファイルを選択してください",
    filetypes=[("CSV file","*.csv")]            #result.csv->60deg_1cell.csvを人力で作成 soc,ocv[v]を2列人力で追加　このファイルを読む
)

df=pd.read_csv(input_file,encoding="shift_jis")

result_list=[]  #最初に作る辞書

for soc in sorted(df["soc"].unique()):  #最初に現れたsoc値を抽出する（重複は選ばない) sortedは昇順
    df_soc=df[df["soc"]==soc]           #あるsoc値をすべて抽出
    start=0
    for i in range(1,len(df_soc)):
        if df_soc["ｽﾃｯﾌﾟ時間"].iloc[i]<df_soc["ｽﾃｯﾌﾟ時間"].iloc[i-1]:     #時間が小さくなったら、、、
            pulse=df_soc.iloc[start:i]                                  #その直前までをpulseとして抜き出す soc,step時間,電流,電圧、、、
            result_list.append(analyze_pulse(pulse))                    #そのsoc,電流でのパラメータ計算結果をresult_listに追加する

            start=i
    pulse=df_soc.iloc[start:]                                           #最後のデータ端部処理。steo時間がここで切れる最後の部分
    result_list.append(analyze_pulse(pulse))            #result_listはリスト。戻り値である辞書の積み重ねデータになっているのが実態

df_result=pd.DataFrame(result_list)         #結果のリストをdataframeに入れる

df_result.to_csv(
    csv_path+r"\pulse_parameter_result.csv",
    index=False,
    encoding="shift_jis"
)

