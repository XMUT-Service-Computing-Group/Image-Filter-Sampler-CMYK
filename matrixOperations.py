import cv2
import numpy as np

# 生成参数函数
from PIL import Image


def generate_attributes(path1, path2, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq):
    t1 = cv2.getTickCount()
    image_data = np.array(Image.open(path1))
    attrArrays = []
    if counts > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, 1)
        for i in range(4):
            for j in range(allCount[i]):
                attrArrays.append(
                    generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, i, j + 1, round(allStep[i])))
    if countd > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countd, 2)
        channels = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        for i in range(6):
            for j in range(allCount[i]):
                attrArrayss = []
                for k in range(2):
                    attrArrayss.append(
                        generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels[i][k] - 1, j + 1,
                                                  round(allStep[i * 2 + k])))
                attrArrays.append(np.sum([np.array(attrArrayss[0]), np.array(attrArrayss[1])], axis=0))
    if countt > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countt, 3)
        channels = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
        for i in range(4):
            for j in range(allCount[i]):
                attrArrayss = []
                for k in range(3):
                    attrArrayss.append(
                        generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels[i][k] - 1, j + 1,
                                                  round(allStep[i * 3 + k])))
                attrArrays.append(np.sum([np.array(attrArrayss[0]), np.array(attrArrayss[1]), np.array(attrArrayss[2])], axis=0))
    if countq > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countq, 4)
        for i in range(countq):
            attrArrayss = []
            for j in range(4):
                attrArrayss.append(
                    generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, j, i + 1, allStep, 4))
            attrArrays.append(
                np.sum([np.array(attrArrayss[0]), np.array(attrArrayss[1]), np.array(attrArrayss[2]), np.array(attrArrayss[3])], axis=0))
    generate_all_images(image_data, attrArrays, path2)
    t2 = cv2.getTickCount()
    return str(round((t2 - t1) * 1000 / cv2.getTickFrequency() / 1000, 2)) + '秒'


def generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, channel, count, step, mode=0):
    attrArray = []
    side = [sideC, sideM, sideY, sideK]
    mid = [midC, midM, midY, midK]
    for i in range(4):
        if i == channel:
            if mode == 4:
                attrArray.append(round((side[channel] + count * step[channel]) / 100, 2))
                attrArray.append(round(mid[channel] / 100, 2))
            else:
                attrArray.append(round((side[channel] + count * step) / 100, 2))
                attrArray.append(round(mid[channel] / 100, 2))
        else:
            attrArray.append(0)
            attrArray.append(0)
    return attrArray


def generate_all_images(image_data, Array, outputpath):
    for arr in Array:
        processed_data = generate_one_image(image_data, arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7])
        name = str(int(arr[0] * 100)) + ',' + str(int(arr[2] * 100)) + ',' + str(int(arr[4] * 100)) + ',' + str(int(arr[6] * 100))
        Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(outputpath + '/' + name + ".jpg")


# 生成单张图片的函数
# 输入参数：sideX, midX 都是百分比，如sideC是10%，则 sideC = 0.1。sideX和midX默认值为0，当四个通道都是0的时候，图像不变。
def generate_one_image(image_data, sideC=0, midC=0, sideM=0, midM=0, sideY=0, midY=0, sideK=0, midK=0):
    return_data = image_data.copy()
    if (sideC != 0.0) & (midC != 0.0):
        klc, blc, krc, brc = generate_function([0, sideC], [127, midC], [255, sideC])
        return_data[:, :, 0] = np.where(return_data[:, :, 0] < 127, (klc * return_data[:, :, 0] + blc + 1) * return_data[:, :, 0],
                                        np.where((krc * return_data[:, :, 0] + brc + 1) * return_data[:, :, 0] > 255, 255,
                                                 (krc * return_data[:, :, 0] + brc + 1) * return_data[:, :, 0]))
    if (sideM != 0.0) & (midM != 0.0):
        klm, blm, krm, brm = generate_function([0, sideM], [127, midM], [255, sideM])
        return_data[:, :, 1] = np.where(return_data[:, :, 1] < 127, (klm * return_data[:, :, 1] + blm + 1) * return_data[:, :, 1],
                                        np.where((krm * return_data[:, :, 1] + brm + 1) * return_data[:, :, 1] > 255, 255,
                                                 (krm * return_data[:, :, 1] + brm + 1) * return_data[:, :, 1]))
    if (sideY != 0.0) & (midY != 0.0):
        kly, bly, kry, bry = generate_function([0, sideY], [127, midY], [255, sideY])
        return_data[:, :, 2] = np.where(return_data[:, :, 2] < 127, (kly * return_data[:, :, 2] + bly + 1) * return_data[:, :, 2],
                                        np.where((kry * return_data[:, :, 2] + bry + 1) * return_data[:, :, 2] > 255, 255,
                                                 (kry * return_data[:, :, 2] + bry + 1) * return_data[:, :, 2]))
    if (sideK != 0.0) & (midK != 0.0):
        klk, blk, krk, brk = generate_function([0, sideK], [127, midK], [255, sideK])
        return_data[:, :, 3] = np.where(return_data[:, :, 3] < 127, (klk * return_data[:, :, 3] + blk + 1) * return_data[:, :, 3],
                                        np.where((krk * return_data[:, :, 3] + brk + 1) * return_data[:, :, 3] > 255, 255,
                                                 (krk * return_data[:, :, 3] + brk + 1) * return_data[:, :, 3]))
    return return_data


def generate_function(sideL, mid, sideR):
    X1, Y1 = sideL
    X2, Y2 = mid
    X3, Y3 = sideR
    kl = (Y2 - Y1) / (X2 - X1)
    kr = (Y2 - Y3) / (X2 - X3)
    bl = Y2 - kl * X2
    br = Y2 - kr * X2
    return kl, bl, kr, br


# 获得每个通道对应的数量和步长
def generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, count, mode):
    isC = isM = isY = isK = False
    countC = countM = countY = countK = 0
    stepC = stepM = stepY = stepK = 0
    countCM = countCY = countCK = countMY = countMK = countYK = 0
    stepCMC = stepCMM = stepCYC = stepCYY = stepCKC = stepCKK = stepMYM = stepMYY = stepMKM = stepMKK = stepYKY = stepYKK = 0
    countCMY = countCMK = countCYK = countMYK = 0
    stepCMYC = stepCMYM = stepCMYY = stepCMKC = stepCMKM = stepCMKK = stepCYKC = stepCYKY = stepCYKK = stepMYKM = stepMYKY = stepMYKK = 0
    allCount = []
    allStep = []

    if sideC != 0 or midC != 0:
        isC = True
    if sideM != 0 or midM != 0:
        isM = True
    if sideY != 0 or midY != 0:
        isY = True
    if sideK != 0 or midK != 0:
        isK = True

    # 获得四个中心值中不为零的个数
    mids = [midC, midM, midY, midK]
    countNonzero = 4 - mids.count(0)

    # 获得当生成数量为奇数时部分通道的生成数量需要额外增加的数量countLeft
    countMod = 0
    if countNonzero < 4:
        countMod = count % countNonzero
    if countNonzero == 4:
        if mode == 1:
            countMod = count % 4
        if mode == 2:
            countMod = count % 6
        elif mode == 3:
            countMod = count % 4
    count = count - countMod
    countLeft = countMod

    # 获得四种模式中四个通道的平均生成数量
    if mode == 1:  # 单色模式且不为零的中心值大于1个时
        if countNonzero > 1:
            count = count // countNonzero
        if isC:
            countC, stepC, countLeft = generate_count_step_mode_1(sideC, midC, count, countLeft)
        if isM:
            countM, stepM, countLeft = generate_count_step_mode_1(sideM, midM, count, countLeft)
        if isY:
            countY, stepY, countLeft = generate_count_step_mode_1(sideY, midY, count, countLeft)
        if isK:
            countK, stepK, countLeft = generate_count_step_mode_1(sideK, midK, count, countLeft)
        allCount = [countC, countM, countY, countK]
        allStep = [stepC, stepM, stepY, stepK]
    elif mode == 2:  # 双色模式
        if countNonzero == 4:
            count = count // 6  # 有且仅有[1,2][1,3][1,4][2,3],[2,4],[3,4]六种情况
        elif countNonzero == 3:
            count = count // 3
        elif countNonzero == 2:
            count = count + countLeft
        if isC and isM:
            countCM, stepCMC, stepCMM, countLeft = generate_count_step_mode_2(sideC, midC, sideM, midM, count, countLeft)
        if isC and isY:
            countCY, stepCYC, stepCYY, countLeft = generate_count_step_mode_2(sideC, midC, sideY, midY, count, countLeft)
        if isC and isK:
            countCK, stepCKC, stepCKK, countLeft = generate_count_step_mode_2(sideC, midC, sideK, midK, count, countLeft)
        if isM and isY:
            countMY, stepMYM, stepMYY, countLeft = generate_count_step_mode_2(sideM, midM, sideY, midY, count, countLeft)
        if isM and isK:
            countMK, stepMKM, stepMKK, countLeft = generate_count_step_mode_2(sideM, midM, sideK, midK, count, countLeft)
        if isY and isK:
            countYK, stepYKY, stepYKK, countLeft = generate_count_step_mode_2(sideY, midY, sideK, midK, count, countLeft)
        allCount = [countCM, countCY, countCK, countMY, countMK, countYK]
        allStep = [stepCMC, stepCMM, stepCYC, stepCYY, stepCKC, stepCKK, stepMYM, stepMYY, stepMKM, stepMKK, stepYKY, stepYKK]
    elif mode == 3:  # 三色模式
        if countNonzero == 4:
            count = count // 4  # 三色模式有且仅有[1,2,3][1,2,4][1,3,4][2,3,4]四种情况
        elif countNonzero == 3:
            count = count + countLeft
        if isC and isM and isY:
            countCMY, stepCMYC, stepCMYM, stepCMYY, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideM, midM, sideY, midY, count, countLeft)
        if isC and isM and isK:
            countCMK, stepCMKC, stepCMKM, stepCMKK, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideM, midM, sideK, midK, count, countLeft)
        if isC and isY and isK:
            countCYK, stepCYKC, stepCYKY, stepCYKK, countLeft = \
                generate_count_step_mode_3(sideC, midC, sideY, midY, sideK, midK, count, countLeft)
        if isM and isY and isK:
            countMYK, stepMYKM, stepMYKY, stepMYKK, countLeft = \
                generate_count_step_mode_3(sideM, midM, sideY, midY, sideK, midK, count, countLeft)
        allCount = [countCMY, countCMK, countCYK, countMYK]
        allStep = [stepCMYC, stepCMYM, stepCMYY, stepCMKC, stepCMKM, stepCMKK, stepCYKC, stepCYKY, stepCYKK, stepMYKM, stepMYKY, stepMYKK]
    elif mode == 4:  # 四色模式且不为零的中心值大于1个时
        stepC, stepm, stepY, stepK = generate_count_step_mode_4(sideC, midC, sideM, midM, sideY, midY, sideK, midK, count)
        allStep = [stepC, stepm, stepY, stepK]
    return allCount, allStep


def generate_count_step_step(side, mid, count, countLeft):
    step = round((mid - side) / (count + countLeft), 1)
    if step * (count + countLeft) > (mid - side):
        step = round(step - 1, 1)
    return step


def generate_count_step_count(countLeft):
    if countLeft >= 1:
        countLeftTemp = 1
    else:
        countLeftTemp = countLeft
    if countLeft > 0:
        countLeft = countLeft - 1
    return countLeftTemp, countLeft


def generate_count_step_mode_1(side, mid, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step = generate_count_step_step(side, mid, count, countLeftTemp)
    return count + countLeftTemp, step, countLeft


def generate_count_step_mode_2(side1, mid1, side2, mid2, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(side1, mid1, count, countLeftTemp)
    step2 = generate_count_step_step(side2, mid2, count, countLeftTemp)
    return count + countLeftTemp, step1, step2, countLeft


def generate_count_step_mode_3(side1, mid1, side2, mid2, side3, mid3, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(side1, mid1, count, countLeftTemp)
    step2 = generate_count_step_step(side2, mid2, count, countLeftTemp)
    step3 = generate_count_step_step(side3, mid3, count, countLeftTemp)
    return count + countLeftTemp, step1, step2, step3, countLeft


def generate_count_step_mode_4(side1, mid1, side2, mid2, side3, mid3, side4, mid4, count):
    step1 = generate_count_step_step(side1, mid1, count, 0)
    step2 = generate_count_step_step(side2, mid2, count, 0)
    step3 = generate_count_step_step(side3, mid3, count, 0)
    step4 = generate_count_step_step(side4, mid4, count, 0)
    return step1, step2, step3, step4


if __name__ == '__main__':
    pass
