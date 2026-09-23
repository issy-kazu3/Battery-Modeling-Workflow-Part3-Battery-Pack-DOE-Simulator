from tkinter import NONE

import pandas as pd
import numpy as np
from bat_pack_cond_loader import load_conditions 
from load_drive_condition import load_drive_condition
from ir_map_load import load_ir_map
from interpolate_cell import map_const
from bat_sequential_calc import bat_disc_calc


#csv_path=r"C:\Users\kazi3\Documents\my_program\Github\python_battery\battery"
#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\battery"
#file_drive=r"drive_condition.csv"
#file_pack=r"bat_pack_condition.csv"
#file_map=r"IR_MAP.csv"
def main(doe_seri,doe_para,dic_input,input_map,input_drive,csv_path): #この書き方はNG Noneをデフォルト値した場合、その後ろに引数は入れられない
    temp,ocv,df_map=load_ir_map(input_map)     #temp温度 socはbunpy配列 df_mapはセルの定数のsoc&charge/discharge map

    drive_cond=load_drive_condition(input_drive) #drive_condはnumpy配列

#    input_file=csv_path+"\\"+file_pack
#    dic_config=load_conditions(input_file)      #dic_configはパック構成の辞書  ちなみに辞書を多数個束ねたものがリストである  リストからある辞書を取り出すにはresult[i-1] ある辞書のある項目はresult[i-1]["soc"]などの表現となる
    dic_config={}   #{}が辞書 []はリスト
    if doe_seri is not None:
        dic_config["n-seri"]=doe_seri
    if doe_para is not None:
        dic_config["n-para"]=doe_para

    dic_config["cell capa(Ah)"]=dic_input["cell capa(Ah)"]
    dic_config["start soc"]=dic_input["start soc"]
    dic_config["max v"]=dic_input["max v"]
    dic_config["min v"]=dic_input["min v"]
    dic_config["max current"]=dic_input["max current"]
    dic_config["max charge cell cur"]=dic_input["max charge cell cur"]
    dic_config["max sys v"]=dic_input["max sys v"]
    dic_config["min sys v"]=dic_input["min sys v"]
    dic_config["wt g"]=dic_input["wt g"]

    soc=dic_config["start soc"]
    Vp=0    #batの寄生容量の電圧も共通変数をしてもつ
    results=[]  #dataの入れものとしての空のリスト
    conclusion=[]

    map_data=map_const(ocv,df_map)          #これから使うセルのマップ特性をmap_dataという辞書に入れる

    for i in range(len(drive_cond)-1):   #drive_condの長さは、時間と電力の組み合わせの数である。  ここでは、i番目の時間とi+1番目の時間の間で、計算を行う
        t0=drive_cond[i][0]
        t1=drive_cond[i+1][0]
        pw1=drive_cond[i+1][1]

        temp,soc,current,voltage,warning,Wloss,Vp=bat_disc_calc(temp,map_data,dic_config,t0,soc,t1,pw1,Vp)
        results.append({
            "time":t1,
            "power":pw1,
            "soc":soc,
            "current":current,
            "voltage":voltage,
            "output":current*voltage,
            "loss":Wloss,
            "temp":temp,
            "warning":warning,
        })
        if warning!="":
            print("fault at time=",t1,"sec, warning=",warning)
        if (warning=="max voltage limit")or (warning=="min voltage limit"):
            print(
                "n-seri =", dic_config["n-seri"],
                "n-para =", dic_config["n-para"],
                "voltage =", voltage,
                "current =", current,
                "warning =", warning
            )
            continue
            #break  #電圧が上限下限を超えたら、そこで計算を打ち切る
    df_results=pd.DataFrame(results)
    df_results.to_csv(csv_path+"\\bat_sim_result.csv",index=False)

    fault = df_results[df_results["warning"] != ""]
    if fault.empty:
        first_fault = "Passed"
    else:
        first_fault = fault.iloc[0]["warning"]

    conclusion.append({
        "cell capa":dic_config["cell capa(Ah)"],
        "max v":dic_config["max v"],
        "min v":dic_config["min v"],
        "start soc":dic_config["start soc"],
        "finished soc":soc,
        "max current":dic_config["max current"],
        "max charge cell current":dic_config["max charge cell cur"],
        "max sys v":dic_config["max sys v"],
        "min sys v":dic_config["min sys v"],
        "n-seri":dic_config["n-seri"],
        "n-para":dic_config["n-para"],
        "pack weight kg":dic_config["wt g"]*dic_config["n-seri"]*dic_config["n-para"]/1000,
        "DOD":df_results["soc"].max() - df_results["soc"].min(),
        "total loss wh":df_results["loss"].sum()/3600,
        "result": first_fault,
    })

    df_conclusion=pd.DataFrame(conclusion)
    df_conclusion.to_csv(csv_path+"\\bat_sim_conclusion.csv",index=False)   

    return df_results,df_conclusion

#if __name__ == "__main__":     #このファイルを直接実行し、mainを動かすのであればこの記述が必要。今回はmain()は外部から呼び出されるので不要
#    main()