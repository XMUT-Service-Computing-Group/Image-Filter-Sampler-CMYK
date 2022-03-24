import os
import threading
import tkinter as tk
import tkinter.filedialog as tkf
from pathlib import Path
from tkinter import messagebox, END, ttk

import matrixOperations


def GUI():
    window = tk.Tk()
    window.title('CMYK打样软件')
    nScreenWid, nScreenHei = window.maxsize()
    window.geometry('%dx%d+%d+%d' % (500, 300, (nScreenWid - 500) / 2, (nScreenHei - 300) / 2))
    window.resizable(0, 0)

    label1 = tk.Label(window, text='选择图片：')
    label1.place(x=10, y=25)

    button1 = tk.Button(window, text='选择', command=lambda: openfile(path1))
    button1.place(x=70, y=20)

    path1 = tk.Entry(window, width=53)
    path1.place(x=110, y=25)
    path1.insert(0,
                 'C:/Users/xkz/PycharmProjects/图片/软膜+高清UV卷材3.2米+内光模式+缝边（内框尺寸）#129.00_145.00#1#国兵广告#国兵广告#18014398510459029#18014398513464524.jpg')

    label2 = tk.Label(window, text='生成路径：')
    label2.place(x=10, y=65)

    button2 = tk.Button(window, text='选择', command=lambda: savefiles(path2))
    button2.place(x=70, y=60)

    path2 = tk.Entry(window, width=53)
    path2.place(x=110, y=65)
    path2.insert(0, 'C:/Users/xkz/PycharmProjects/图片/新建文件夹')

    label3 = tk.Label(window, text='阈值模板：')
    label3.place(x=10, y=105)

    value1 = tk.StringVar()
    value1.set('默认')
    values1 = ['默认']
    threshold = ttk.Combobox(window, height=5, width=15, state='readonly', textvariable=value1, values=values1)
    threshold.place(x=70, y=105)

    label4 = tk.Label(window, text='生成模式：')
    label4.place(x=240, y=105)

    value2 = tk.StringVar()
    value2.set('线性分布')
    values2 = ['线性分布']
    distribution = ttk.Combobox(window, height=5, width=15, state='readonly', textvariable=value2, values=values2)
    distribution.place(x=300, y=105)

    label5 = tk.Label(window, text='变化幅度[0,50]：')
    label5.place(x=10, y=145)

    label51 = tk.Label(window, text='边界')
    label51.place(x=125, y=145)

    label52 = tk.Label(window, text='中心')
    label52.place(x=175, y=145)

    label53 = tk.Label(window, text='C：')
    label53.place(x=85, y=175)

    sideC = tk.Entry(window, width=5)
    sideC.place(x=120, y=175)
    sideC.insert(0, 0)

    midC = tk.Entry(window, width=5)
    midC.place(x=172, y=175)
    midC.insert(0, 50)

    label54 = tk.Label(window, text='M：')
    label54.place(x=80, y=205)

    sideM = tk.Entry(window, width=5)
    sideM.place(x=120, y=205)
    sideM.insert(0, 0)

    midM = tk.Entry(window, width=5)
    midM.place(x=172, y=205)
    midM.insert(0, 30)

    label55 = tk.Label(window, text='Y：')
    label55.place(x=80, y=235)

    sideY = tk.Entry(window, width=5)
    sideY.place(x=120, y=235)
    sideY.insert(0, 0)

    midY = tk.Entry(window, width=5)
    midY.place(x=172, y=235)
    midY.insert(0, 40)

    label56 = tk.Label(window, text='K：')
    label56.place(x=80, y=265)

    sideK = tk.Entry(window, width=5)
    sideK.place(x=120, y=265)
    sideK.insert(0, 0)

    midK = tk.Entry(window, width=5)
    midK.place(x=172, y=265)
    midK.insert(0, 20)

    label6 = tk.Label(window, text='生成数量[10,100]：')
    label6.place(x=240, y=145)

    label61 = tk.Label(window, text='单色：')
    label61.place(x=350, y=145)

    counts = tk.Entry(window, width=5)
    counts.place(x=390, y=145)
    counts.insert(0, 0)

    label62 = tk.Label(window, text='双色：')
    label62.place(x=350, y=175)

    countd = tk.Entry(window, width=5)
    countd.place(x=390, y=175)
    countd.insert(0, 0)

    label63 = tk.Label(window, text='三色：')
    label63.place(x=350, y=205)

    countt = tk.Entry(window, width=5)
    countt.place(x=390, y=205)
    countt.insert(0, 0)

    label64 = tk.Label(window, text='四色：')
    label64.place(x=350, y=235)

    countq = tk.Entry(window, width=5)
    countq.place(x=390, y=235)
    countq.insert(0, 10)

    button4 = tk.Button(window, text='生成',
                        command=lambda: operations(path1.get(), path2.get(), threshold.get(), distribution.get(), int(sideC.get()),
                                                   int(midC.get()), int(sideM.get()), int(midM.get()), int(sideY.get()),
                                                   int(midY.get()),
                                                   int(sideK.get()), int(midK.get()), int(counts.get()), int(countd.get()),
                                                   int(countt.get()), int(countq.get()), button4))
    button4.place(x=450, y=260)

    window.mainloop()


def openfile(path):
    path.delete(0, END)
    path.insert(0, tkf.askopenfilename(filetypes=[('图片', '.png .jpg .jpeg .tif')]))


def savefiles(path):
    path.delete(0, END)
    path.insert(0, tkf.askdirectory())


def operations(path1, path2, threshold, distribution, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt,
               countq, button):
    if not Path(path2).is_dir():
        os.makedirs(path2)
    if not Path(path1).is_file():
        tk.messagebox.showerror('错误', '图片不存在！')
        return
    if path2 == "":
        tk.messagebox.showerror('错误', '生成路径为空！')
        return
    if not str(sideC).isdigit() or not str(midC).isdigit() or not str(sideM).isdigit() or not str(midM).isdigit() or not str(
            sideY).isdigit() or not str(midY).isdigit() or not str(sideK).isdigit() or not str(midK).isdigit() or not str(
        counts).isdigit() or not str(countd).isdigit() or not str(countt).isdigit() or not str(countq).isdigit():
        tk.messagebox.showerror('错误', "变化幅度和生成数量需要是数字！")
        return
    if sideC == "" or midC == "" or sideM == "" or midM == "" or sideY == "" or midY == "" or sideK == "" or midK == "":
        tk.messagebox.showerror('错误', "变化幅度为空！")
        return
    if sideC < 0 or sideC > 50 or sideM < 0 or sideM > 50 or sideY < 0 or sideY > 50 or sideK < 0 or sideK > 50 or midC < 0 or midC > 50 \
            or midM < 0 or midM > 50 or midY < 0 or midY > 50 or midK < 0 or midK > 50:
        tk.messagebox.showerror('错误', "变化幅度的范围是[0,50]！")
        return
    if sideC > midC or sideM > midM or sideY > midY or sideK > midK:
        tk.messagebox.showerror('错误', "边界变化幅度需要小于中心变化幅度")
        return
    if counts == "" or countd == "" or countt == "" or countq == "":
        tk.messagebox.showerror('错误', "生成数量为空！")
        return
    if counts + countd + countt + countq < 10 or counts + countd + countt + countq > 100:
        tk.messagebox.showerror('错误', "生成数量的范围是[10,100]！")
        return
    mids = [midC, midM, midY, midK]
    countNonzero = 4 - mids.count(0)
    if countq != 0 and countNonzero < 4:
        tk.messagebox.showerror('错误', '四色的生成数量和中心值变化幅度不为0的数量不匹配！')
        return
    elif countt != 0 and countNonzero < 3:
        tk.messagebox.showerror('错误', '三色的生成数量和中心值变化幅度不为0的数量不匹配！')
        return
    elif countd != 0 and countNonzero < 2:
        tk.messagebox.showerror('错误', '双色的生成数量和中心值变化幅度不为0的数量不匹配！')
        return
    elif counts != 0 and countNonzero < 1:
        tk.messagebox.showerror('错误', '单色的生成数量和中心值变化幅度不为0的数量不匹配！')
        return
    OperationsThread(path1, path2, threshold, distribution, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt,
                     countq, button).start()
    InfoThread(button).start()


class OperationsThread(threading.Thread):

    def __init__(self, path1, path2, threshold, distribution, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd,
                 countt,
                 countq, button):
        threading.Thread.__init__(self)
        self.path1 = path1
        self.path2 = path2
        self.threshold = threshold
        self.distribution = distribution
        self.sideC = round(int(sideC), 1)
        self.midC = round(int(midC), 1)
        self.sideM = round(int(sideM), 1)
        self.midM = round(int(midM), 1)
        self.sideY = round(int(sideY), 1)
        self.midY = round(int(midY), 1)
        self.sideK = round(int(sideK), 1)
        self.midK = round(int(midK), 1)
        self.counts = int(counts)
        self.countd = int(countd)
        self.countt = int(countt)
        self.countq = int(countq)
        self.button = button

    def run(self):
        message = matrixOperations.generate_attributes(self.path1, self.path2, self.sideC, self.midC, self.sideM, self.midM, self.sideY,
                                                       self.midY, self.sideK, self.midK, self.counts, self.countd, self.countt, self.countq)
        self.button['text'] = "生成"
        self.button.place(x=450, y=260)
        tk.messagebox.showinfo('信息', message)


class InfoThread(threading.Thread):
    def __init__(self, button):
        threading.Thread.__init__(self)
        self.button = button

    def run(self):
        self.button.place(x=420, y=260)
        self.button['text'] = "生成中……"


if __name__ == '__main__':
    GUI()
