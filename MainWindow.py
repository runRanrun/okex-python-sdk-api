# pyinstaller --console --onefile MainWindow.py
#83078b278c80933cde6c583ce4da6b9328f5a14e
#from .method import AutoTrade
import method

from tkinter import *
from tkinter import ttk
root = Tk()
root.title('自动交易系统')
root.geometry('600x400')

# label_stdp_short = Label(root, text="开空基准价格", fg="black", relief="groove")
# label_stdp_short.grid(column=0, row=0)
label_short_count = Label(root, text="开空点位数量", fg="black", relief="groove")
label_short_count.grid(column=0, row=1)
label_short_quantity = Label(root, text="点位购买张数", fg="black", relief="groove")
label_short_quantity.grid(column=0, row=2)

# label_stdp_long = Label(root, text="开多基准价格", fg="black", relief="groove")
# label_stdp_long.grid(column=2, row=0)
label_long_count = Label(root, text="开多点位数量", fg="black", relief="groove")
label_long_count.grid(column=2, row=1)
label_long_quantity = Label(root, text="点位购买张数", fg="black", relief="groove")
label_long_quantity.grid(column=2, row=2)

label_step = Label(root, text="开仓步进比例（空）", fg="black", relief="groove")
label_step.grid(column=0, row=3)
label_step = Label(root, text="平仓步进比例（空）", fg="black", relief="groove")
label_step.grid(column=2, row=3)
label_step = Label(root, text="开仓步进比例（多）", fg="black", relief="groove")
label_step.grid(column=0, row=4)
label_step = Label(root, text="平仓步进比例（多）", fg="black", relief="groove")
label_step.grid(column=2, row=4)
label_step = Label(root, text="币类型", fg="black", relief="groove")
label_step.grid(column=0, row=5)
label_step = Label(root, text="api_key", fg="black", relief="groove")
label_step.grid(column=2, row=5)
label_step = Label(root, text="secret_key", fg="black", relief="groove")
label_step.grid(column=0, row=6)
label_step = Label(root, text="passphrase", fg="black", relief="groove")
label_step.grid(column=2, row=6)



JY_dict = dict()
ZYZS_dict = dict()


entry_short_point = Entry(root)
entry_short_point.grid(column=1, row=1)
entry_short_quantity = Entry(root)
entry_short_quantity.grid(column=1, row=2)

# entry_stdp_long = Entry(root)
# entry_stdp_long.grid(column=3, row=0)
entry_long_point = Entry(root)
entry_long_point.grid(column=3, row=1)
entry_long_quantity = Entry(root)
entry_long_quantity.grid(column=3, row=2)




coinType = StringVar()
combobox_coinType = ttk.Combobox(root, width=12, textvariable=coinType)
combobox_coinType['values'] = ("BTC", "LTC", "ETH", "ETC", "XRP", "EOS", "BCH", "BSV", "TRX")
combobox_coinType.grid(column=1, row=5)
combobox_coinType.current(1)

entry_shortstep = Entry(root)
entry_shortstep.grid(column=1, row=3)
entry_shortstep2 = Entry(root)
entry_shortstep2.grid(column=3, row=3)

entry_longstep = Entry(root)
entry_longstep.grid(column=1, row=4)
entry_longstep2 = Entry(root)
entry_longstep2.grid(column=3, row=4)


entry_apikey = Entry(root)
entry_apikey.grid(column=3, row=5)
entry_apikey.insert(0, 'e475a6ff-3a83-4bce-8cc8-51b1108b5d23')

entry_secretkey = Entry(root)
entry_secretkey.insert(0, '57944536044AD9587DC263C734A2B3A7')
entry_secretkey.grid(column=1, row=6)

entry_passphrase = Entry(root)
entry_passphrase.grid(column=3, row=6)
entry_passphrase.insert(0,'rander360104456')


JY_dict['ShortPoint'] = entry_short_point
JY_dict['LongPoint'] = entry_long_point
JY_dict['ShortQuantity'] = entry_short_quantity
JY_dict['LongQuantity'] = entry_long_quantity
JY_dict['CoinType'] = combobox_coinType
JY_dict['shortStep'] = entry_shortstep
JY_dict['shortStep2'] = entry_shortstep2
JY_dict['longStep'] = entry_longstep
JY_dict['longStep2'] = entry_longstep2

JY_dict['api_key'] = entry_apikey
JY_dict['secret_key'] = entry_secretkey
JY_dict['passphrase'] = entry_passphrase


btn1 = Button(root, text='开始交易', command=lambda :method.start_trade(JY_dict,ZYZS_dict))
btn1.grid(column=0, row=0)
btn2 = Button(root, text='停止交易', command=lambda: method.stopdeal())
btn2.grid(column=3, row=0)

root.mainloop()