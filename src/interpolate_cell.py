import numpy as np

def map_const(ocv,IR_MAP):
    df_chg=IR_MAP[IR_MAP["mode"]=="charge"].sort_values("soc")      #modeがchargeだけを抜き出して、それのsocを昇順になるように、項目を整理している
    df_dis=IR_MAP[IR_MAP["mode"]=="discharge"].sort_values("soc")

    ocv_soc=ocv["soc"].to_numpy()   #計算の高速化のために、ndarrayに変換
    ocv_value=ocv["ocv"].to_numpy()

    map_data={                  #これは辞書、入れ子の辞書で、numpy配列のndarrayが並んでいる
        "ocv_soc":ocv_soc,
        "ocv_value":ocv_value,
        "charge":{
            "soc":df_chg["soc"].to_numpy(),     #df_chgから、さらにsocだけを抜き出して、ndarrayにして、、、辞書の数値として保持している。 ndarrayが数値の単位になっていることに注意
            "Ri":df_chg["Ri"].to_numpy(),
            "Rp":df_chg["Rp"].to_numpy(),
            "C":df_chg["C"].to_numpy()
        },
        "discharge":{
            "soc":df_dis["soc"].to_numpy(),
            "Ri":df_dis["Ri"].to_numpy(),
            "Rp":df_dis["Rp"].to_numpy(),
            "C":df_dis["C"].to_numpy()
        }
    }


    return map_data


def interp_ir(soc,map_data,mode):       #y,yri,yrp,yc,x(これはsoc)、などに辞書から分割  あるsocにおける、Ri,Rp,C,ocvの4変数を近似して、まとめて返す関数
    y=map_data[mode]    #modeによって、mapから取り出す
    yri=y["Ri"]
    yrp=y["Rp"]
    yc=y["C"]
    x=y["soc"]
    Ri=interp(soc,x,yri)    #socの値による近似
    Rp=interp(soc,x,yrp)
    C=interp(soc,x,yc)

    x=map_data["ocv_soc"]
    yocv= map_data["ocv_value"]
    ocv=interp(soc,x,yocv)

    return ocv,Ri,Rp,C

def linear_interp(x,x1,x2,y1,y2):   #外挿近似を行う一般関数
    return y1+(x-x1)*(y2-y1)/(x2-x1)

def interp(soc,x,y):                #mapの近似関数
    if soc<x[0]:
        val=linear_interp(soc,x[0],x[1],y[0],y[1])
        return val
    elif soc>x[-1]:
        val=linear_interp(soc,x[-1],x[-2],y[-1],y[-2])
        return val
    else:
        val = np.interp(
            soc,
            x,
            y
        )
        return val


#def interp_soc(soc,map_data):
#    x=map_data["ocv_soc"]
#    y=map_data["ocv_value"]
#    if soc<x[0]:
#        ocv=linier_interp(soc,x[0],x[1],y[0],y[1])
#        return ocv
#    elif soc>x[-1]:
#        ocv=linier_interp(soc,x[-1],x[-2],y[-1],y[-2])
#        return ocv
#    else:
#        ocv = np.interp(
#            soc,
#            x,
#            y
#        )
#        return ocv

#def interp_soc(soc,map_data):
#    if soc<map_data["ocv_soc"][0]:
#        ocv=map_data["ocv_value"][0]-(map_data["ocv_value"][0]-map_data["ocv_value"][1])/(map_data["ocv_soc"][0]-map_data["ocv_soc"][1])*(soc-map_data["ocv_soc"][0])
#        return ocv
#    if soc>map_data["ocv_soc"][-1]:
#        ocv=map_data["ocv_value"][-1]+(map_data["ocv_value"][-1]-map_data["ocv_value"][-2])/(map_data["ocv_soc"][-1]-map_data["ocv_soc"][-2])*(soc-map_data["ocv_soc"][-1])
#        return ocv
#    ocv = np.interp(
#        soc,
#        map_data["ocv_soc"],
#        map_data["ocv_value"]
#    )
#    return ocv


