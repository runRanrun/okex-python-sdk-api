# pyinstaller --console --onefile deal.py
#from .method import AutoTrade
import method

from tkinter import *
from tkinter import ttk
root = Tk()
root.title('自动交易系统')
root.geometry('600x800')

label_stdp_short = Label(root, text="开空基准价格", fg="black", relief="groove")
label_stdp_short.grid(column=0, row=0)
label_short_count = Label(root, text="开空点位数量", fg="black", relief="groove")
label_short_count.grid(column=0, row=1)
label_short_quantity = Label(root, text="点位购买张数", fg="black", relief="groove")
label_short_quantity.grid(column=0, row=2)

label_stdp_long = Label(root, text="开多基准价格", fg="black", relief="groove")
label_stdp_long.grid(column=2, row=0)
label_long_count = Label(root, text="开多点位数量", fg="black", relief="groove")
label_long_count.grid(column=2, row=1)
label_long_quantity = Label(root, text="点位购买张数", fg="black", relief="groove")
label_long_quantity.grid(column=2, row=2)

label_step = Label(root, text="步进比例", fg="black", relief="groove")
label_step.grid(column=0, row=3)
label_step = Label(root, text="币类型", fg="black", relief="groove")
label_step.grid(column=2, row=3)

label_short_price = Label(root, text="止盈止损", fg="black", relief="groove")
label_short_price.grid(column=0, row=4)

label_short_price = Label(root, text="开空触发价格", fg="black", relief="groove")
label_short_price.grid(column=0, row=5)
label_short_count = Label(root, text="开空数量", fg="black", relief="groove")
label_short_count.grid(column=0, row=6)
label_short_openPro = Label(root, text="开空比例", fg="black", relief="groove")
label_short_openPro.grid(column=0, row=7)
label_short_closePro = Label(root, text="普通平空比例", fg="black", relief="groove")
label_short_closePro.grid(column=0, row=8)
label_short_quickPro = Label(root, text="快速平空比例", fg="black", relief="groove")
label_short_quickPro.grid(column=0, row=9)
label_adjust = Label(root, text="波动调整比例", fg="black", relief="groove")
label_adjust.grid(column=0, row=10)
label_adjust = Label(root, text="平仓延时(秒)", fg="black", relief="groove")
label_adjust.grid(column=0, row=11)



label_long_price = Label(root, text="开多触发价格", fg="black", relief="groove")
label_long_price.grid(column=2, row=5)
label_long_count = Label(root, text="开多数量", fg="black", relief="groove")
label_long_count.grid(column=2, row=6)
label_long_openPro = Label(root, text="开多比例", fg="black", relief="groove")
label_long_openPro.grid(column=2, row=7)
label_long_closePro = Label(root, text="普通平多比例", fg="black", relief="groove")
label_long_closePro.grid(column=2, row=8)
label_long_quickPro = Label(root, text="快速平多比例", fg="black", relief="groove")
label_long_quickPro.grid(column=2, row=9)
label_adjust = Label(root, text="加仓数量", fg="black", relief="groove")
label_adjust.grid(column=2, row=10)
label_adjust = Label(root, text="快速平触发比例", fg="black", relief="groove")
label_adjust.grid(column=2, row=11)



JY_dict = dict()
ZYZS_dict = dict()

entry_stdp_short = Entry(root)
entry_stdp_short.grid(column=1, row=0)
entry_short_point = Entry(root)
entry_short_point.grid(column=1, row=1)
entry_short_quantity = Entry(root)
entry_short_quantity.grid(column=1, row=2)

entry_stdp_long = Entry(root)
entry_stdp_long.grid(column=3, row=0)
entry_long_point = Entry(root)
entry_long_point.grid(column=3, row=1)
entry_long_quantity = Entry(root)
entry_long_quantity.grid(column=3, row=2)

entry1_short_price = Entry(root)
entry1_short_price.grid(column=1, row=5)
entry1_short_quantity = Entry(root)
entry1_short_quantity.grid(column=1, row=6)
entry1_openshort_proportion = Entry(root)
entry1_openshort_proportion.grid(column=1, row=7)
entry1_closeshort_normalproportion = Entry(root)
entry1_closeshort_normalproportion.grid(column=1, row=8)
entry1_closeshort_quickproportion = Entry(root)
entry1_closeshort_quickproportion.grid(column=1, row=9)
entry1_wave_adjust = Entry(root)
entry1_wave_adjust.grid(column=1, row=10)
entry1_close_lag = Entry(root)
entry1_close_lag.grid(column=1, row=11)




entry1_long_price = Entry(root)
entry1_long_price.grid(column=3, row=5)
entry1_long_quantity = Entry(root)
entry1_long_quantity.grid(column=3, row=6)
entry1_openlong_proportion = Entry(root)
entry1_openlong_proportion.grid(column=3, row=7)
entry1_closelong_normalproportion = Entry(root)
entry1_closelong_normalproportion.grid(column=3, row=8)
entry1_closelong_quickproportion = Entry(root)
entry1_closelong_quickproportion.grid(column=3, row=9)
entry1_addposition = Entry(root)
entry1_addposition.grid(column=3, row=10)
entry1_quickclose_trigger = Entry(root)
entry1_quickclose_trigger.grid(column=3, row=11)


coinType = StringVar()
combobox_coinType = ttk.Combobox(root, width=12, textvariable=coinType)
combobox_coinType['values'] = ("BTC", "LTC", "ETH", "ETC", "XRP", "EOS", "BCH", "BSV", "TRX")
combobox_coinType.grid(column=3, row=3)
combobox_coinType.current(1)

entry_step = Entry(root)
entry_step.grid(column=1, row=3)

JY_dict['ShortPrice'] = entry_stdp_short
JY_dict['LongPrice'] = entry_stdp_long
JY_dict['ShortPoint'] = entry_short_point
JY_dict['LongPoint'] = entry_long_point
JY_dict['ShortQuantity'] = entry_short_quantity
JY_dict['LongQuantity'] = entry_long_quantity
JY_dict['CoinType'] = combobox_coinType
JY_dict['Step'] = entry_step

ZYZS_dict['ShortPrice'] = entry1_short_price
ZYZS_dict['ShortQuantity'] = entry1_short_quantity
ZYZS_dict['OpenShortProp'] = entry1_openshort_proportion
ZYZS_dict['CloseShortNormProp'] = entry1_closeshort_normalproportion
ZYZS_dict['CloseShortQuickProp'] = entry1_closeshort_quickproportion
ZYZS_dict['WaveAdjust'] = entry1_wave_adjust
ZYZS_dict['CloseLag'] = entry1_close_lag

ZYZS_dict['LongPrice'] = entry1_long_price
ZYZS_dict['LongQuantity'] = entry1_long_quantity
ZYZS_dict['OpenLongProp'] = entry1_openlong_proportion
ZYZS_dict['CloseLongNormProp'] = entry1_closelong_normalproportion
ZYZS_dict['CloseLongQuickProp'] = entry1_closelong_quickproportion
ZYZS_dict['AddPosition'] = entry1_addposition
ZYZS_dict['QuickCloseTrigger'] = entry1_quickclose_trigger





#ZYZS_dict['ShortPrice'] =



btn1 = Button(root, text='开始交易', command=lambda: method.start_trade(JY_dict,ZYZS_dict))
btn1.grid(column=0, row=12)
btn1 = Button(root, text='停止交易', command=lambda: function.stopdeal())
btn1.grid(column=3, row=12)

root.mainloop()