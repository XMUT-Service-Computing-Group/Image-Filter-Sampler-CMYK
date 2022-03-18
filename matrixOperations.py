import cv2
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def generate(path1, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq):
    t1 = cv2.getTickCount()
    image_data = np.array(Image.open(path1))
    if counts > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, 1)
        for i in range(counts):
            singleColor(image_data, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, i + 1)
    if countd > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countd, 2)
        for j in range(countd):
            doubleColor(image_data, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, j + 1)
    if countt > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countt, 3)
        for k in range(countt):
            trebleColor(image_data, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, k + 1)
    if countq > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countq, 4)
        for h in range(countq):
            quadrupleColor(image_data, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allStep, h + 1)
    t2 = cv2.getTickCount()
    return str(round((t2 - t1) * 1000 / cv2.getTickFrequency() / 1000, 2)) + '秒'


def singleColor(image_data, path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, count):
    countC, countM, countY, countK = allCount
    stepC, stepM, stepY, stepK = allStep
    processed_data = image_data
    countTemp = 0
    isC = isM = isY = isK = False
    if count < countC + 1:
        countTemp = count
        processed_data = generate_one_image(image_data, sideC + stepC * countTemp, midC, 0, 0, 0, 0, 0, 0)
        isC = True
    elif count < countC + countM + 1:
        countTemp = count - countC
        processed_data = generate_one_image(image_data, 0, 0, sideM + stepM * countTemp, midM, 0, 0, 0, 0)
        isM = True
    elif count < countC + countM + countY + 1:
        countTemp = count - countC - countM
        processed_data = generate_one_image(image_data, 0, 0, 0, 0, sideY + stepY * countTemp, midY, 0, 0)
        isY = True
    elif count < countC + countM + countY + countK + 1:
        countTemp = count - countC - countM - countY
        processed_data = generate_one_image(image_data, 0, 0, 0, 0, 0, 0, sideK + stepK * countTemp, midK)
        isK = True
    name = '未命名'
    if isC:
        name = '(' + generate_name(sideC, midC, stepC, countTemp) + ',0,0,0)'
    elif isM:
        name = '(0,' + generate_name(sideM, midM, stepM, countTemp) + ',0,0)'
    elif isY:
        name = '(0,0,' + generate_name(sideY, midY, stepY, countTemp) + ',0)'
    elif isK:
        name = '(0,0,0,' + generate_name(sideK, midK, stepK, countTemp) + ')'
    print(name)
    Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(path + '/' + name + ".jpg")


def doubleColor(image_data, path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, count):
    countCM, countCY, countCK, countMY, countMK, countYK = allCount
    stepCMC, stepCMM, stepCYC, stepCYY, stepCKC, stepCKK, stepMYM, stepMYY, stepMKM, stepMKK, stepYKY, stepYKK = allStep
    processed_data = image_data
    countTemp = 0
    isCM = isCY = isCK = isMY = isMK = isYK = False
    if count < countCM + 1:
        countTemp = count
        processed_data = generate_one_image(image_data, sideC + stepCMC * countTemp, midC, sideM + stepCMM * countTemp, midM, 0, 0, 0, 0)
        isCM = True
    elif count < countCM + countCY + 1:
        countTemp = count - countCM
        processed_data = generate_one_image(image_data, sideC + stepCYC * countTemp, midC, 0, 0, sideY + stepCYY * countTemp, midY, 0, 0)
        isCY = True
    elif count < countCM + countCY + countCK + 1:
        countTemp = count - countCM - countCY
        processed_data = generate_one_image(image_data, sideC + stepCKC * countTemp, midC, 0, 0, 0, 0, sideK + stepCKK * countTemp, midK)
        isCK = True
    elif count < countCM + countCY + countCK + countMY + 1:
        countTemp = count - countCM - countCY - countCK
        processed_data = generate_one_image(image_data, 0, 0, sideM + stepMYM * countTemp, midM, sideY + stepMYY * countTemp, midY, 0, 0)
        isMY = True
    elif count < countCM + countCY + countCK + countMY + countMK + 1:
        countTemp = count - countCM - countCY - countCK - countMY
        processed_data = generate_one_image(image_data, 0, 0, sideM + stepMKM * countTemp, midM, 0, 0, sideK + stepMKK * countTemp, midK)
        isMK = True
    elif count < countCM + countCY + countCK + countMY + countMK + countYK + 1:
        countTemp = count - countCM - countCY - countCK - countMY - countYK
        processed_data = generate_one_image(image_data, 0, 0, 0, 0, sideY + stepYKY * countTemp, midY, sideK + stepYKK * countTemp, midK)
        isYK = True
    name = '未命名'
    if isCM:
        name = '(' + generate_name(sideC, midC, stepCMC, countTemp) + ',' + generate_name(sideM, midM, stepCMM, countTemp) + ',0,0)'
    elif isCY:
        name = '(' + generate_name(sideC, midC, stepCYC, countTemp) + ',0,' + generate_name(sideY, midY, stepCYY, countTemp) + ',0)'
    elif isCK:
        name = '(' + generate_name(sideC, midC, stepCKC, countTemp) + ',0,0,' + generate_name(sideK, midK, stepCKK, countTemp) + ')'
    elif isMY:
        name = '(0,' + generate_name(sideM, midM, stepMYM, countTemp) + ',' + generate_name(sideY, midY, stepMYY, countTemp) + ',0)'
    elif isMK:
        name = '(0,' + generate_name(sideM, midM, stepMKM, countTemp) + ',0,' + generate_name(sideK, midK, stepMKK, countTemp) + ')'
    elif isYK:
        name = '(0,0,' + generate_name(sideY, midY, stepYKY, countTemp) + ',' + generate_name(sideK, midK, stepYKK, countTemp) + ')'
    print(name)
    Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(path + '/' + name + ".jpg")


def trebleColor(image_data, path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allCount, allStep, count):
    countCMY, countCMK, countCYK, countMYK = allCount
    stepCMYC, stepCMYM, stepCMYY, stepCMKC, stepCMKM, stepCMKK, stepCYKC, stepCYKY, stepCYKK, stepMYKM, stepMYKY, stepMYKK = allStep
    processed_data = image_data
    isCMY = isCMK = isCYK = isMYK = False
    if count < countCMY + 1:
        countTemp = count
        processed_data = generate_one_image(image_data, sideC + stepCMYC * countTemp, midC, sideM + stepCMYM * countTemp, midM,
                                            sideY + stepCMYY * countTemp, midY, 0, 0)
        isCMY = True
    elif count < countCMY + countCMK + 1:
        countTemp = count - countCMY
        processed_data = generate_one_image(image_data, sideC + stepCMKC * countTemp, midC, sideM + stepCMKM * countTemp, midM,
                                            0, 0, sideK + stepCMKK * countTemp, midK)
        isCMK = True
    elif count < countCMY + countCMK + countCYK + 1:
        countTemp = count - countCMY - countCMK
        processed_data = generate_one_image(image_data, sideC + stepCYKC * countTemp, midC, 0, 0, sideY + stepCYKY * countTemp, midY,
                                            sideK + stepCYKK * countTemp, midK)
        isCYK = True
    elif count < countCMY + countCMK + countCYK + countMYK + 1:
        countTemp = count - countCMY - countCMK - countCYK
        processed_data = generate_one_image(image_data, 0, 0, sideM + stepMYKM * countTemp, midM, sideY + stepMYKY * countTemp, midY,
                                            sideK + stepMYKK * countTemp, midK)
        isMYK = True
    name = '未命名'
    if isCMY:
        name = '(' + generate_name(sideC, midC, stepCMYC, countTemp) + ',' \
               + generate_name(sideM, midM, stepCMYM, countTemp) + ',' + generate_name(sideY, midY, stepCMYY, countTemp) + ',0)'
    elif isCMK:
        name = '(' + generate_name(sideC, midC, stepCMKC, countTemp) + ',' \
               + generate_name(sideY, midY, stepCMKM, countTemp) + ',0,' + generate_name(sideY, midY, stepCMKK, countTemp) + ')'
    elif isCYK:
        name = '(' + generate_name(sideC, midC, stepCYKC, countTemp) + ',0,' \
               + generate_name(sideY, midY, stepCYKY, countTemp) + ',' + generate_name(sideK, midK, stepCYKK, countTemp) + ')'
    elif isMYK:
        name = '(0,' + generate_name(sideM, midM, stepMYKM, countTemp) + ',' \
               + generate_name(sideY, midY, stepMYKY, countTemp) + ',' + generate_name(sideK, midK, stepMYKK, countTemp) + ')'
    print(name)
    Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(path + '/' + name + ".jpg")


def quadrupleColor(image_data, path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, allStep, count):
    stepC, stepM, stepY, stepK = allStep
    processed_data = generate_one_image(image_data, sideC + stepC * count, midC, sideM + stepM * count, midM, sideY + stepY * count, midY,
                                        sideK + stepK * count, midK)
    name = '(' + generate_name(sideC, midC, stepC, count) + ',' \
           + generate_name(sideM, midM, stepM, count) + ',' \
           + generate_name(sideY, midY, stepY, count) + ',' + generate_name(sideK, midK, stepK, count) + ')'
    print(name)
    Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(path + '/' + name + ".jpg")


# 获得每个通道对应的数量和步长
def generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countTemp, mode):
    countC = countM = countY = countK = 0
    stepC = stepM = stepY = stepK = 0
    countCM = countCY = countCK = countMY = countMK = countYK = 0
    stepCMC = stepCMM = stepCYC = stepCYY = stepCKC = stepCKK = stepMYM = stepMYY = stepMKM = stepMKK = stepYKY = stepYKK = 0
    countCMY = countCMK = countCYK = countMYK = 0
    stepCMYC = stepCMYM = stepCMYY = stepCMKC = stepCMKM = stepCMKK = stepCYKC = stepCYKY = stepCYKK = stepMYKM = stepMYKY = stepMYKK = 0
    allCount = []
    allStep = []

    # 获得四个中心值中不为零的个数
    mids = [midC, midM, midY, midK]
    countNonzero = 4 - mids.count(0)

    # 获得当生成数量为奇数时部分通道的生成数量需要额外增加的数量countLeft
    countMod = 0
    if countNonzero < 4:
        countMod = countTemp % countNonzero
    if countNonzero == 4:
        if mode == 1:
            countMod = countTemp % 4
        if mode == 2:
            countMod = countTemp % 6
        elif mode == 3:
            countMod = countTemp % 4
    countTemp = countTemp - countMod
    countLeft = countMod

    # 获得四种模式中四个通道的平均生成数量
    if mode == 1 and countNonzero > 1:  # 单色模式且不为零的中心值大于1个时
        countTemp = countTemp // countNonzero
        if midC > 0:
            countC, stepC, countLeft = generate_count_step_mode_1(sideC, midC, countTemp, countLeft)
        if midM > 0:
            countM, stepM, countLeft = generate_count_step_mode_1(sideM, midM, countTemp, countLeft)
        if midY > 0:
            countY, stepY, countLeft = generate_count_step_mode_1(sideY, midY, countTemp, countLeft)
        if midK > 0:
            countK, stepK, countLeft = generate_count_step_mode_1(sideK, midK, countTemp, countLeft)
        allCount = [countC, countM, countY, countK]
        allStep = [stepC, stepM, stepY, stepK]
    elif mode == 2:  # 双色模式
        if countNonzero == 4:
            countTemp = countTemp // 6  # 有且仅有[1,2][1,3][1,4][2,3],[2,4],[3,4]六种情况
        elif countNonzero == 3:
            countTemp = countTemp // 3
        elif countNonzero == 2:
            countTemp = countTemp + countLeft
        if midC > 0 and midM > 0:
            countCM, stepCMC, stepCMM, countLeft = generate_count_step_mode_2(sideC, midC, sideM, midM, countTemp, countLeft)
        if midC > 0 and midY > 0:
            countCY, stepCYC, stepCYY, countLeft = generate_count_step_mode_2(sideC, midC, sideY, midY, countTemp, countLeft)
        if midC > 0 and midK > 0:
            countCK, stepCKC, stepCKK, countLeft = generate_count_step_mode_2(sideC, midC, sideK, midK, countTemp, countLeft)
        if midM > 0 and midY > 0:
            countMY, stepMYM, stepMYY, countLeft = generate_count_step_mode_2(sideM, midM, sideY, midY, countTemp, countLeft)
        if midM > 0 and midK > 0:
            countMK, stepMKM, stepMKK, countLeft = generate_count_step_mode_2(sideM, midM, sideK, midK, countTemp, countLeft)
        if midY > 0 and midK > 0:
            countYK, stepYKY, stepYKK, countLeft = generate_count_step_mode_2(sideY, midY, sideK, midK, countTemp, countLeft)
        allCount = [countCM, countCY, countCK, countMY, countMK, countYK]
        allStep = [stepCMC, stepCMM, stepCYC, stepCYY, stepCKC, stepCKK, stepMYM, stepMYY, stepMKM, stepMKK, stepYKY, stepYKK]
    elif mode == 3:  # 三色模式
        if countNonzero == 4:
            countTemp = countTemp // 4  # 三色模式有且仅有[1,2,3][1,2,4][1,3,4][2,3,4]四种情况
        elif countNonzero == 3:
            countTemp = countTemp + countLeft
        if midC > 0 and midM > 0 and midY > 0:
            countCMY, stepCMYC, stepCMYM, stepCMYY, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideM, midM, sideY, midY, countTemp, countLeft)
        if midC > 0 and midM > 0 and midK > 0:
            countCMK, stepCMKC, stepCMKM, stepCMKK, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideM, midM, sideK, midK, countTemp, countLeft)
        if midC > 0 and midY > 0 and midK > 0:
            countCYK, stepCYKC, stepCYKY, stepCYKK, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideY, midY, sideK, midK, countTemp, countLeft)
        if midM > 0 and midY > 0 and midK > 0:
            countMYK, stepMYKM, stepMYKY, stepMYKK, countLeft = \
                generate_count_step_mode_3(sideM, midM, sideY, midY, sideK, midK, countTemp, countLeft)
        allCount = [countCMY, countCMK, countCYK, countMYK]
        allStep = [stepCMYC, stepCMYM, stepCMYY, stepCMKC, stepCMKM, stepCMKK, stepCYKC, stepCYKY, stepCYKK, stepMYKM, stepMYKY, stepMYKK]
    elif mode == 4:  # 四色模式且不为零的中心值大于1个时
        stepC, stepm, stepY, stepK = generate_count_step_mode_4(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countTemp)
        allStep = [stepC, stepm, stepY, stepK]
    print(allCount, allStep)
    return allCount, allStep


def generate_count_step_step(side, mid, countTemp, countLeftTemp):
    step = round((mid - side) / (countTemp + countLeftTemp), 1)
    if step * (countTemp + countLeftTemp) > (mid - side):
        step = round(step - 0.1, 1)
    return step


def generate_count_step_count(countLeft):
    if countLeft >= 1:
        countLeftTemp = 1
    else:
        countLeftTemp = countLeft
    if countLeft > 0:
        countLeft = countLeft - 1
    return countLeftTemp, countLeft


def generate_count_step_mode_1(side, mid, countTemp, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step = generate_count_step_step(side, mid, countTemp, countLeftTemp)
    return countTemp + countLeftTemp, step, countLeft


def generate_count_step_mode_2(side1, mid1, side2, mid2, countTemp, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(side1, mid1, countTemp, countLeftTemp)
    step2 = generate_count_step_step(side2, mid2, countTemp, countLeftTemp)
    return countTemp + countLeftTemp, step1, step2, countLeft


def generate_count_step_mode_3(side1, mid1, side2, mid2, side3, mid3, countTemp, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(side1, mid1, countTemp, countLeftTemp)
    step2 = generate_count_step_step(side2, mid2, countTemp, countLeftTemp)
    step3 = generate_count_step_step(side3, mid3, countTemp, countLeftTemp)
    return countTemp + countLeftTemp, step1, step2, step3, countLeft


def generate_count_step_mode_4(side1, mid1, side2, mid2, side3, mid3, side4, mid4, countTemp):
    step1 = generate_count_step_step(side1, mid1, countTemp, 0)
    step2 = generate_count_step_step(side2, mid2, countTemp, 0)
    step3 = generate_count_step_step(side3, mid3, countTemp, 0)
    step4 = generate_count_step_step(side4, mid4, countTemp, 0)
    return step1, step2, step3, step4


def generate_name(side, mid, step, count):
    return str(round(((side + step * count) * 10 - 1) % (mid * 10)) + 1)


def generate_one_image(image_data, sideC, midC, sideM, midM, sideY, midY, sideK, midK):
    klc, blc, krc, brc = generate_function([0, sideC], [50, midC], [100, sideC])
    klm, blm, krm, brm = generate_function([0, sideM], [50, midM], [100, sideM])
    kly, bly, kry, bry = generate_function([0, sideY], [50, midY], [100, sideY])
    klk, blk, krk, brk = generate_function([0, sideK], [50, midK], [100, sideK])
    if midC > 0:
        image_data = data_processing(0, image_data, klc, blc, krc, brc)
    if midM > 0:
        image_data = data_processing(1, image_data, klm, blm, krm, brm)
    if midY > 0:
        image_data = data_processing(2, image_data, kly, bly, kry, bry)
    if midK > 0:
        image_data = data_processing(3, image_data, klk, blk, krk, brk)
    return image_data


def generate_function(sideL, mid, sideR):
    X1, Y1 = sideL
    X2, Y2 = mid
    X3, Y3 = sideR
    kl = (Y2 - Y1) / (X2 - X1)
    kr = (Y2 - Y3) / (X2 - X3)
    bl = br = Y2
    return kl, bl, kr, br


def data_processing(channel, image_data, kl, bl, kr, br):
    return_data = image_data.copy()
    image_data1 = image_data.copy()
    image_data1[:, :, channel][image_data1[:, :, channel] > 127] = 0  # 将C通道中数值大于127的数值设为0
    image_data2 = image_data.copy()
    image_data2[:, :, channel][image_data2[:, :, channel] <= 127] = 0  # 将C通道中数值小于等于127的数值设为0
    image_data3 = image_data - image_data1  # 得到除了C通道中数值大于127的位置以外所有所有包括其它通道的位置全为0的新矩阵
    image_data4 = image_data - image_data2  # 得到除了C通道中数值小于等于127的位置以外所有所有包括其它通道的位置全为0的新矩阵
    yr = (kr * image_data3 + br + 100) / 100  # 得到C通道中数值大于127的位置可用的变化幅度
    yl = (kl * image_data4 + bl + 100) / 100  # 得到C通道中数值小于等于127的位置可用的变化幅度
    image_data3 = np.where(image_data3 * yr > 255, 255, image_data3 * yr)
    image_data4 = np.where(image_data4 * yl > 255, 255, image_data4 * yl)
    image_data5 = image_data3 + image_data4
    return_data[:, :, channel] = image_data5[:, :, channel]
    return return_data


if __name__ == '__main__':
    pass
