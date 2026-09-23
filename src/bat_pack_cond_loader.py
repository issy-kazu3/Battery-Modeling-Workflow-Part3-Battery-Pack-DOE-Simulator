import pandas as pd

#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\battery\bat_pack_condition.csv"

def load_conditions(csv_path):
    df=pd.read_csv(csv_path,header=None,index_col=0)    #header=Noneは先頭行がcolumns(表題)でないことを指示している index_col=0はindex列も不要で、indexを最初の列(=0)にしないさという指示
#    config=df[1].to_dict()                  #df[1]とは、１列目つまり数値のこと。df[0]はindexにしてしまったのですでに存在していなくて、df[1]空のみ残っている    さらに.to_dict()はここでのindexが辞書の項目になることを暗黙に意味している
    config={}       #より慎重に、項目の文字列のスペースなどを取り除く　まずは空の辞書を定義
    for k,v in df[1].to_dict().items():      #df[1].to_dict()で、辞書化を指定していて、items()は1項目ごと取り出す関数
        config[k.strip()]=v                 #.strip()は、kという文字列から文字列の両端のスペースを取り除く vが数値
    return config                           #configという辞書を関数の戻り値とする

#config=load_conditions(csv_path)
#cell_capa=float(config["cell capa(Ah)"])
#max_v=float(config["max v"])
#min_v=float(config["min v"])
#start_soc=float(config["start soc"])
#max_current=float(config["max current"])
#max_sys_v=float(config["max sys v"])
#min_sys_v=float(config["min sys v"])
#n_seri=int(config["n-seri"])
#n_para=int(config["n-para"])
#print(cell_capa)
#print(max_v)
#print(min_v)
#print(start_soc)
#print(max_current)
#print(max_sys_v)
#print(min_sys_v)
#print(n_seri)
#print(n_para)
