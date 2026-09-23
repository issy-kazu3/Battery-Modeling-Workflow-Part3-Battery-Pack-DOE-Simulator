import tkinter as tk                #file dialog
from tkinter import filedialog      #file dialog
import pandas as pd

def load_ir_map(csv_path):
#    root=tk.Tk()                        #file dialog
#    root.withdraw() # Tkウィンドウを表示しない file dialog
#    input_file=filedialog.askopenfilename(
#        initialdir=csv_path,
#        title="解析用のファイルを選択してください",
#        filetypes=[("IR map","*.csv")]
#    )
#    df=pd.read_csv(input_file)      #これはheader=０オプションで読んでいる。よって、先頭行が見出しとなる

    df=pd.read_csv(csv_path)      #これはheader=０オプションで読んでいる。よって、先頭行が見出しとなる

    temp=df["Ta"].iloc[0]
    ocv=df[["soc","ocv"]]#.to_numpy()        #ここは２重[]であること。なんでだろう？？？  このsocはnumpy配列　高速で扱える数値
    df=df.drop(columns=["Ta","tau","ocv"])
    return temp,ocv,df

#temp,soc,df=load_ir_map()
#print(temp)
#print(soc)
#print(df)

