import threading
import tkinter as tk
import tkinter.filedialog as tkf
from pathlib import Path
from tkinter import messagebox, END

import matrixOperations


def GUI():
    window = tk.Tk()
    window.title('CMYK打样软件')
    nScreenWid, nScreenHei = window.maxsize()
    window.geometry('%dx%d+%d+%d' % (400, 260, (nScreenWid - 500) / 2, (nScreenHei - 300) / 2))
    window.resizable(0, 0)

    label1 = tk.Label(window, text='选择图片：')
    label1.place(x=10, y=25)

    button1 = tk.Button(window, text='选择', command=lambda: open_file(path))
    button1.place(x=70, y=20)

    path = tk.Entry(window, width=39)
    path.place(x=110, y=25)
    path.insert(0, '')
    label2 = tk.Label(window, text='变化百分比[0,100]')
    label2.place(x=10, y=65)

    label21 = tk.Label(window, text='边界')
    label21.place(x=125, y=65)

    label22 = tk.Label(window, text='中心')
    label22.place(x=175, y=65)

    label23 = tk.Label(window, text='C：')
    label23.place(x=85, y=95)

    sideC = tk.Entry(window, width=5)
    sideC.place(x=120, y=95)
    sideC.insert(0, 0)

    midC = tk.Entry(window, width=5)
    midC.place(x=172, y=95)
    midC.insert(0, 50)

    label24 = tk.Label(window, text='M：')
    label24.place(x=80, y=125)

    sideM = tk.Entry(window, width=5)
    sideM.place(x=120, y=125)
    sideM.insert(0, 0)

    midM = tk.Entry(window, width=5)
    midM.place(x=172, y=125)
    midM.insert(0, 50)

    label25 = tk.Label(window, text='Y：')
    label25.place(x=80, y=155)

    sideY = tk.Entry(window, width=5)
    sideY.place(x=120, y=155)
    sideY.insert(0, 0)

    midY = tk.Entry(window, width=5)
    midY.place(x=172, y=155)
    midY.insert(0, 50)

    label26 = tk.Label(window, text='K：')
    label26.place(x=80, y=185)

    sideK = tk.Entry(window, width=5)
    sideK.place(x=120, y=185)
    sideK.insert(0, 0)

    midK = tk.Entry(window, width=5)
    midK.place(x=172, y=185)
    midK.insert(0, 50)

    label3 = tk.Label(window, text='生成数量[10,100]')
    label3.place(x=280, y=65)

    label31 = tk.Label(window, text='单色：')
    label31.place(x=280, y=95)

    counts = tk.Entry(window, width=5)
    counts.place(x=320, y=95)
    counts.insert(0, 10)

    label32 = tk.Label(window, text='双色：')
    label32.place(x=280, y=125)

    countd = tk.Entry(window, width=5)
    countd.place(x=320, y=125)
    countd.insert(0, 10)

    label33 = tk.Label(window, text='三色：')
    label33.place(x=280, y=155)

    countt = tk.Entry(window, width=5)
    countt.place(x=320, y=155)
    countt.insert(0, 10)

    label34 = tk.Label(window, text='四色：')
    label34.place(x=280, y=185)

    countq = tk.Entry(window, width=5)
    countq.place(x=320, y=185)
    countq.insert(0, 10)

    button2 = tk.Button(window, text='生成', width=50,
                        command=lambda: operations(path.get(), int(sideC.get()), int(midC.get()), int(sideM.get()), int(midM.get()),
                                                   int(sideY.get()), int(midY.get()), int(sideK.get()), int(midK.get()),
                                                   int(counts.get()), int(countd.get()), int(countt.get()), int(countq.get()), button2))
    button2.place(x=20, y=220)

    window.mainloop()


def open_file(path):
    path.delete(0, END)
    path.insert(0, tkf.askopenfilename(filetypes=[('图片', '.png .jpg .jpeg .tif')]))


def operations(path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq, button):
    if not Path(path).is_file():
        tk.messagebox.showerror('错误', '图片不存在！')
        return
    if not str(sideC).isdigit() or not str(midC).isdigit() or not str(sideM).isdigit() or not str(midM).isdigit() or not str(
            sideY).isdigit() or not str(midY).isdigit() or not str(sideK).isdigit() or not str(midK).isdigit() or not str(
        counts).isdigit() or not str(countd).isdigit() or not str(countt).isdigit() or not str(countq).isdigit():
        tk.messagebox.showerror('错误', "变化百分比和生成数量需要是数字！")
        return
    if sideC == "" or midC == "" or sideM == "" or midM == "" or sideY == "" or midY == "" or sideK == "" or midK == "":
        tk.messagebox.showerror('错误', "变化百分比为空！")
        return
    if sideC < 0 or sideC > 100 or sideM < 0 or sideM > 100 or sideY < 0 or sideY > 100 or sideK < 0 or sideK > 100 or midC < 0 or midC > 100 \
            or midM < 0 or midM > 100 or midY < 0 or midY > 100 or midK < 0 or midK > 100:
        tk.messagebox.showerror('错误', "变化百分比的范围是[0,100]！")
        return
    if sideC > midC or sideM > midM or sideY > midY or sideK > midK:
        tk.messagebox.showerror('错误', "边界变化百分比需要小于中心变化百分比")
        return
    if counts == "" or countd == "" or countt == "" or countq == "":
        tk.messagebox.showerror('错误', "生成数量为空！")
        return
    if counts < 0 or counts > 100 or countd < 0 or countd > 100 or countt < 0 or countt > 100 or countq < 0 or countq > 100:
        tk.messagebox.showerror('错误', "生成数量的范围是[10,100]！")
        return
    mids = [midC, midM, midY, midK]
    countNonzero = 4 - mids.count(0)
    if countq != 0 and countNonzero < 4:
        tk.messagebox.showerror('错误', '四色的生成数量和中心值变化百分比不为0的数量不匹配！')
        return
    elif countt != 0 and countNonzero < 3:
        tk.messagebox.showerror('错误', '三色的生成数量和中心值变化百分比不为0的数量不匹配！')
        return
    elif countd != 0 and countNonzero < 2:
        tk.messagebox.showerror('错误', '双色的生成数量和中心值变化百分比不为0的数量不匹配！')
        return
    elif counts != 0 and countNonzero < 1:
        tk.messagebox.showerror('错误', '单色的生成数量和中心值变化百分比不为0的数量不匹配！')
        return
    OperationsThread(path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq, button).start()
    InfoThread(button).start()


class OperationsThread(threading.Thread):

    def __init__(self, path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq, button):
        threading.Thread.__init__(self)
        self.path = path
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
        message = matrixOperations.generate_attributes(self.path, self.sideC, self.midC, self.sideM, self.midM, self.sideY,
                                                       self.midY, self.sideK, self.midK, self.counts, self.countd, self.countt, self.countq)

        if message == '图片需要是CMYK格式！':
            tk.messagebox.showerror('错误', message)
        else:
            tk.messagebox.showinfo('信息', '生成成功！')
        self.button['text'] = "生成"


class InfoThread(threading.Thread):
    def __init__(self, button):
        threading.Thread.__init__(self)
        self.button = button

    def run(self):
        self.button['text'] = "生成中……"


if __name__ == '__main__':
    GUI()
