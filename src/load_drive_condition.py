import pandas as pd

#csv_path=r"D:\Userarea\J0125789\Documents\Python_code\battery\drive_condition.csv"

def load_drive_condition(csv_path):
    df=pd.read_csv(csv_path)
    drive_cond=df[["Time(sec)","Battery Power(W)"]].to_numpy()        #ここは２重[]であること。なんでだろう？？？

    return drive_cond

#drive_cond=load_drive_condition(csv_path)
#print(drive_cond)