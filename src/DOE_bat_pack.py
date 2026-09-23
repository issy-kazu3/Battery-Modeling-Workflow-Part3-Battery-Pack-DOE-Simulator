from Batt_sim_main import main
import pandas as pd
import tkinter as tk        #ダイアログボックスでの入力パラメータ入力のため
from tkinter import ttk
from bat_pack_cond_loader import load_conditions 


min_seri=100
max_seri=200
min_para=1
max_para=4

csv_path=r"C:\Users\kazi3\Documents\my_program\Github\python_battery\battery\DOE_dialog"
file_pack=r"bat_pack_DOE_initial_condition.csv"
file_drive=r"drive_condition.csv"
file_map=r"IR_MAP.csv"


#----------DOE条件の設定dialog---------------------------------------------
def get_conditions(dic_config):     #ここではからなず引数に使う辞書dic_configを入れねばならない

    confirmed=False #confirmedはここで作った関数ローカルの変数 Falseだと、そのままwindowが閉じられたことを呼び出し側に知らせる

    def start_simulation():

        nonlocal confirmed  #ローカル変数でない。上の変数を使うという宣言

        dic_config["cell capa(Ah)"]=dic_config["cell capa(Ah)"]
        dic_config["wt g"]=dic_config["wt g"]
        dic_config["n-seri max"]=int(entry_seri_max.get())
        dic_config["n-para max"]=int(entry_para_max.get())
        dic_config["n-seri min"]=int(entry_seri_min.get())
        dic_config["n-para min"]=int(entry_para_min.get())
        dic_config["start soc"]=float(entry_soc.get())
        dic_config["max current"]=float(entry_current.get())
        dic_config["max charge cell cur"]=float(entry_charge_current.get())
        dic_config["max sys v"]=float(entry_max_sys_v.get())
        dic_config["min sys v"]=float(entry_min_sys_v.get())
        dic_config["max v"]=float(entry_max_cell_v.get())
        dic_config["min v"]=float(entry_min_cell_v.get())

        confirmed=True  #正しく終了した場合には、False->Trueに変更する！
        window.destroy()

    def cancel():    #windowがそのまま閉じられた場合の関数
        window.destroy()    #そのままwindowを消滅させている。confirmedはFalseのまま

   #conditions={}

    window=tk.Tk()
    window.title("Battery pack condition")
    window.geometry("400x350") #windowの幅を指定

    #xボタンを押したときもcancel()を実行
    window.protocol("WM_DELETE_WINDOW",cancel)  #mainloop()の前に指定しておく　windowが消されたらcancel()

    tk.Label(window,text="cell capa(Ah)").grid(row=0,column=0)
    tk.Label(window,text=str(dic_config["cell capa(Ah)"])).grid(row=0,column=1)
    tk.Label(window,text="cell wt g").grid(row=1,column=0)
    tk.Label(window,text=str(dic_config["wt g"])).grid(row=1,column=1)
    tk.Label(window,text="max").grid(row=2,column=1)
    tk.Label(window,text="min").grid(row=2,column=2)
    tk.Label(window,text="n-seri").grid(row=3,column=0)
    entry_seri_max=tk.Entry(window,justify="center")            #tk.Entryはテキストボックス
    entry_seri_max.insert(0,str(int(dic_config["n-seri max"])))
    entry_seri_max.grid(row=3,column=1)
    entry_seri_min=tk.Entry(window,justify="center")            #tk.Entryはテキストボックス
    entry_seri_min.insert(0,str(int(dic_config["n-seri min"])))
    entry_seri_min.grid(row=3,column=2)
    tk.Label(window,text="n-para").grid(row=4,column=0)
    entry_para_max=tk.Entry(window,justify="center")
    entry_para_max.insert(0,str(int(dic_config["n-para max"])))
    entry_para_max.grid(row=4,column=1)
    entry_para_min=tk.Entry(window,justify="center")
    entry_para_min.insert(0,str(int(dic_config["n-para min"])))
    entry_para_min.grid(row=4,column=2)
    tk.Label(window,text="start soc").grid(row=5,column=0)
    entry_soc=tk.Entry(window,justify="center")
    entry_soc.insert(0,str(dic_config["start soc"]))
    entry_soc.grid(row=5,column=1)
    ttk.Separator(window,orient="horizontal").grid(
        row=6,column=0,columnspan=3,sticky="ew",pady=8
    )
    tk.Label(window,text="threshold").grid(row=7,column=0)
    tk.Label(window,text="system max current A").grid(row=8,column=0)
    entry_current=tk.Entry(window,justify="center")
    entry_current.insert(0,str(dic_config["max current"]))
    entry_current.grid(row=8,column=1)
    tk.Label(window,text="cell max charge current A").grid(row=9,column=0)
    entry_charge_current=tk.Entry(window,justify="center")
    entry_charge_current.insert(0,str(dic_config["max charge cell cur"]))
    entry_charge_current.grid(row=9,column=1)
    tk.Label(window,text="system max voltage V").grid(row=10,column=0)
    entry_max_sys_v=tk.Entry(window,justify="center")
    entry_max_sys_v.insert(0,str(dic_config["max sys v"]))
    entry_max_sys_v.grid(row=10,column=1)
    tk.Label(window,text="system min voltage V").grid(row=11,column=0)
    entry_min_sys_v=tk.Entry(window,justify="center")
    entry_min_sys_v.insert(0,str(dic_config["min sys v"]))
    entry_min_sys_v.grid(row=11,column=1)
    tk.Label(window,text="cell max lmt V").grid(row=12,column=0)
    entry_max_cell_v=tk.Entry(window,justify="center")
    entry_max_cell_v.insert(0,str(dic_config["max v"]))
    entry_max_cell_v.grid(row=12,column=1)
    tk.Label(window,text="cell min lmt V").grid(row=13,column=0)
    entry_min_cell_v=tk.Entry(window,justify="center")
    entry_min_cell_v.insert(0,str(dic_config["min v"]))
    entry_min_cell_v.grid(row=13,column=1)

    tk.Button(
        window,
        text="start simulation",
        command=start_simulation
    ).grid(row=14,column=1,columnspan=1,pady=(10,0))

    window.mainloop()

    if not confirmed:   #キャンセルの場合
        return None

    return dic_config
#-------------DOE条件の設定dialogここまで---------------------------------------------






DOE_result=[]

input_map=csv_path+"\\"+file_map

input_drive=csv_path+"\\"+file_drive

input_file=csv_path+"\\"+file_pack
dic_config=load_conditions(input_file)      #dic_configはパック構成の辞書  ちなみに辞書を多数個束ねたものがリストである  リストからある辞書を取り出すにはresult[i-1] ある辞書のある項目はresult[i-1]["soc"]などの表現となる

dic_config=get_conditions(dic_config)
if dic_config==None:
    dic_config=load_conditions(input_file)

print(dic_config)

#-----------セルの調査範囲----------------
max_seri=int(dic_config["n-seri max"])
min_seri=int(dic_config["n-seri min"])
max_para=int(dic_config["n-para max"])
min_para=int(dic_config["n-para min"])
#-----------セルの調査範囲ここまで--------


for n_para in range(max_para,min_para-1,-1):
    for n_seri in range(max_seri,min_seri-1,-2):
#        print("n_seri=",n_seri,"n_para=",n_para)
        if dic_config["min v"]*n_seri>dic_config["max sys v"]:   #直列数が多すぎると、最小電圧が最大システム電圧を超えてしまうので、そこで打ち切る
            continue
        df_results,df_conclusion=main(doe_seri=n_seri,doe_para=n_para,dic_input=dic_config,input_map=input_map,input_drive=input_drive,csv_path=csv_path)  #main()の戻り値は、df_resultsとdf_conclusionの２つのDataFrameである
#       上の行で、doe_para=npara,という引数を設定するのならば、その後ろも同様の引数の私に統一しなければならない dic_input以下も同じような代入形式にしたためにエラーを解消することができた
#        print("columns =", df_conclusion.columns.tolist())
#        print(df_conclusion)
        if df_conclusion.iloc[0]["result"]=="min system voltage limit" or df_conclusion.iloc[0]["result"]=="min voltage limit":     #直列数はこれ以下は意味がないのでbreakさせる
            break
        elif df_conclusion.iloc[0]["result"]=="Passed":
            DOE_result.append({
                "n-seri":n_seri,
                "n-para":n_para,
                "result":"Passed",
                "finished soc":df_conclusion.iloc[0]["finished soc"],
                "pack weight kg":df_conclusion.iloc[0]["pack weight kg"],
                "DOD":df_conclusion.iloc[0]["DOD"],
                "max cell voltage":df_results["voltage"].max()/n_seri,
                "min cell voltage":df_results["voltage"].min()/n_seri,  
                "total loss wh":df_conclusion.iloc[0]["total loss wh"],
            })

df_DOE_result=pd.DataFrame(DOE_result)
df_DOE_result.to_csv(csv_path+"\\bat_sim_DOE_result.csv",index=False)

df_config=pd.DataFrame(dic_config,index=[0])
df_config.T.to_csv(csv_path+"\\bat_pack_DOE_applied_conditions.csv",index=True,header=False)  #Tが転置。index=Trueにしないと、項目の文字列がなくなってしまう

