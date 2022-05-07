import os
import random
from pathlib import Path
from time import sleep

import cv2
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def generate_attributes(path, sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, countd, countt, countq):
    t1 = cv2.getTickCount()
    if Image.open(path).mode != 'CMYK':
        return '图片需要是CMYK格式！'
    image_data = np.array(Image.open(path))
    result = []
    attrArray = []
    attrArrays = []
    # 当单色模式的生成数量大于0
    if counts > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, counts, 1)
        for i in range(4):
            for j in range(allCount[i]):
                attrArrays.append(generate_attributes_array(0, midC, 0, midM, 0, midY, 0, midK, i, j, round(allStep[i])))
                attrArrays.append(generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, i, j, round(allStep[i])))
        for i in range(4):
            for j in range(allCount[i]):
                attrArrays.append(generate_attributes_array(0, -midC, 0, -midM, 0, -midY, 0, -midK, i, j, round(allStep[i])))
                attrArrays.append(
                    generate_attributes_array(-sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, i, j, round(allStep[i])))
        attrArray.append(attrArrays)
        results = random.sample(range(0, counts * 4), counts)
        result.append(result_check(results, counts * 4))
    attrArrayd = []
    if countd > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countd, 2)
        channels = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        for i in range(6):
            for j in range(allCount[i]):
                attrArrays0 = []
                attrArrayss = []
                for k in range(2):
                    attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, k, 2)
                for h in range(2):
                    attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, h, 2)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 0, 2)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 1, 2)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 0, 2)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 1, 2)
                for index in [0, 2, 4, 6]:
                    attrArrayd.append(np.sum([np.array(attrArrays0[index]), np.array(attrArrays0[index + 1])], axis=0))
                    attrArrayd.append(np.sum([np.array(attrArrayss[index]), np.array(attrArrayss[index + 1])], axis=0))
        attrArray.append(attrArrayd)
        resultd = random.sample(range(0, countd * 8), countd)
        result.append(result_check(resultd, countd * 8))
    attrArrayt = []
    if countt > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countt, 3)
        channels = [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
        for i in range(4):
            for j in range(allCount[i]):
                attrArrays0 = []
                attrArrayss = []
                # +++
                for k in range(3):
                    attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, k, 3)
                # ---
                for h in range(3):
                    attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, h, 3)
                # ++-
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 0, 3)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 1, 3)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 2, 3)
                # +--
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 0, 3)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 1, 3)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 2, 3)
                # -++
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 0, 3)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 1, 3)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 2, 3)
                # -+-
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 0, 3)
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, 1, 3)
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, channels, allStep, i, j, 2, 3)
                for index in [0, 3, 6, 9, 12, 15]:
                    attrArrayt.append(
                        np.sum([np.array(attrArrays0[index]), np.array(attrArrays0[index + 1]), np.array(attrArrays0[index + 2])], axis=0))
                    attrArrayt.append(
                        np.sum([np.array(attrArrayss[index]), np.array(attrArrayss[index + 1]), np.array(attrArrayss[index + 2])], axis=0))
        attrArray.append(attrArrayt)
        resultt = random.sample(range(0, countt * 12), countt)
        result.append(result_check(resultt, countt * 12))
    attrArrayq = []
    if countq > 0:
        allCount, allStep = generate_count_step(sideC, midC, sideM, midM, sideY, midY, sideK, midK, countq, 4)
        for i in range(countq):
            attrArrays0 = []
            attrArrayss = []
            # ++++
            for j in range(4):
                attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, j, 0, 4)
            # ----
            for k in range(4):
                attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, k, 0, 4)
            # +++-
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 3, 0, 4)
            # ++--
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 3, 0, 4)
            # +---
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 3, 0, 4)
            # -+++
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 3, 0, 4)
            # -++-
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 3, 0, 4)
            # -+--
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 0, 0, 4)
            attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, 0, allStep, i, 1, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 2, 0, 4)
            attr_append(attrArrays0, attrArrayss, -sideC, -midC, -sideM, -midM, -sideY, -midY, -sideK, -midK, 0, allStep, i, 3, 0, 4)
            for index in [0, 4, 8, 12, 16, 20, 24, 28]:
                attrArrayq.append(
                    np.sum([np.array(attrArrays0[index]), np.array(attrArrays0[index + 1]), np.array(attrArrays0[index + 2]),
                            np.array(attrArrays0[index + 3])], axis=0))
                attrArrayq.append(
                    np.sum([np.array(attrArrayss[index]), np.array(attrArrayss[index + 1]), np.array(attrArrayss[index + 2]),
                            np.array(attrArrayss[index + 3])], axis=0))
        attrArray.append(attrArrayq)
        resultq = random.sample(range(0, countq * 16), countq)
        result.append(result_check(resultq, countq * 16))
    generate_all_images(image_data, attrArray, result, path)
    t2 = cv2.getTickCount()
    return str(round((t2 - t1) * 1000 / cv2.getTickFrequency() / 1000, 2)) + '秒'


def attr_append(attrArrays0, attrArrayss, sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels, allStep, i, j, k, n):
    if n != 4:
        attrArrays0.append(generate_attributes_array(0, midC, 0, midM, 0, midY, 0, midK, channels[i][k] - 1, j, round(allStep[i * n + k])))
        attrArrayss.append(
            generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, channels[i][k] - 1, j, round(allStep[i * n + k])))
    else:
        attrArrays0.append(generate_attributes_array(0, midC, 0, midM, 0, midY, 0, midK, j, i, allStep, 4))
        attrArrayss.append(generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, j, i, allStep, 4))
    return attrArrays0, attrArrayss


def result_check(result, count):
    result.sort()
    for i in range(len(result) - 1):
        # 当当前数字是偶数并且当前数字的下一个数字是这个数字+1
        if result[i] % 2 == 0 and result[i + 1] == result[i] + 1:
            temp = random.randint(0, count)
            # 如果这个数字不在result列表中并且这个数字+1或-1也不在时
            while True:
                if temp not in result and temp + 1 not in result and temp - 1 not in result:
                    result[i] = temp
                    break
                else:
                    temp = random.randint(0, count)
    return result


def generate_attributes_array(sideC, midC, sideM, midM, sideY, midY, sideK, midK, channel, count, step, mode=0):
    attrArray = []
    side = [sideC, sideM, sideY, sideK]
    mid = [midC, midM, midY, midK]
    k = 1
    # 遍历CMYK四个通道
    for i in range(4):
        # 当遍历到需要改变的通道
        if i == channel:
            # 当是四色模式时
            if mode == 4:
                attrArray.append(round(side[channel] / 100, 2))
                if mid[channel] < 0:
                    k = -1
                attrArray.append(round((mid[channel] - k * count * step[channel]) / 100, 2))
            else:
                attrArray.append(round(side[channel] / 100, 2))
                if mid[channel] < 0:
                    k = -1
                attrArray.append(round((mid[channel] - k * count * step) / 100, 2))
        else:
            attrArray.append(0)
            attrArray.append(0)
    return attrArray


def generate_all_images(image_data, Array, result, path):
    # 获得文件名并生成文件名的文件夹
    outputpath = os.path.splitext(path)[0]
    if not Path(outputpath).is_dir():
        os.makedirs(outputpath)

    # 将参数列表Array根据下标列表result中的数据生成新的生成参数列表Arrays
    Arrays = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            Arrays.append(Array[i][result[i][j]])

    # 将生成参数列表打印到txt文件中
    with open(outputpath + '/打样参数.txt', "w") as f:
        count = 0
        for arr in Arrays:
            count = count + 1
            f.write(str(count) + '#' + str(int(arr[0] * 100)) + ',' + str(int(arr[1] * 100)) + ',' + str(int(arr[2] * 100)) + ',' + str(
                int(arr[3] * 100)) + ',' + str(int(arr[4] * 100)) + ',' + str(int(arr[5] * 100)) + ',' + str(int(arr[6] * 100)) + ',' + str(
                int(arr[7] * 100)))
            f.write('\n')
    count = 0
    for arr in Arrays:
        count = count + 1
        processed_data = generate_one_image(image_data, arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7])
        name = str(count) + '#'
        Image.fromarray(processed_data.astype(np.uint8), mode="CMYK").save(outputpath + '/' + name + ".tif")
        sleep(0.5)


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
            countC, stepC, countLeft = generate_count_step_mode_1(midC, count, countLeft)
        if isM:
            countM, stepM, countLeft = generate_count_step_mode_1(midM, count, countLeft)
        if isY:
            countY, stepY, countLeft = generate_count_step_mode_1(midY, count, countLeft)
        if isK:
            countK, stepK, countLeft = generate_count_step_mode_1(midK, count, countLeft)
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
            countCM, stepCMC, stepCMM, countLeft = generate_count_step_mode_2(midC, midM, count, countLeft)
        if isC and isY:
            countCY, stepCYC, stepCYY, countLeft = generate_count_step_mode_2(midC, midY, count, countLeft)
        if isC and isK:
            countCK, stepCKC, stepCKK, countLeft = generate_count_step_mode_2(midC, midK, count, countLeft)
        if isM and isY:
            countMY, stepMYM, stepMYY, countLeft = generate_count_step_mode_2(midM, midY, count, countLeft)
        if isM and isK:
            countMK, stepMKM, stepMKK, countLeft = generate_count_step_mode_2(midM, midK, count, countLeft)
        if isY and isK:
            countYK, stepYKY, stepYKK, countLeft = generate_count_step_mode_2(midY, midK, count, countLeft)
        allCount = [countCM, countCY, countCK, countMY, countMK, countYK]
        allStep = [stepCMC, stepCMM, stepCYC, stepCYY, stepCKC, stepCKK, stepMYM, stepMYY, stepMKM, stepMKK, stepYKY, stepYKK]
    elif mode == 3:  # 三色模式
        if countNonzero == 4:
            count = count // 4  # 三色模式有且仅有[1,2,3][1,2,4][1,3,4][2,3,4]四种情况
        elif countNonzero == 3:
            count = count + countLeft
        if isC and isM and isY:
            countCMY, stepCMYC, stepCMYM, stepCMYY, countLeft = \
                generate_count_step_mode_3(midC, midM, midY, count, countLeft)
        if isC and isM and isK:
            countCMK, stepCMKC, stepCMKM, stepCMKK, countLeft = \
                generate_count_step_mode_3(midC, midM, midK, count, countLeft)
        if isC and isY and isK:
            countCYK, stepCYKC, stepCYKY, stepCYKK, countLeft = \
                generate_count_step_mode_3(midC, midY, midK, count, countLeft)
        if isM and isY and isK:
            countMYK, stepMYKM, stepMYKY, stepMYKK, countLeft = \
                generate_count_step_mode_3(midM, midY, midK, count, countLeft)
        allCount = [countCMY, countCMK, countCYK, countMYK]
        allStep = [stepCMYC, stepCMYM, stepCMYY, stepCMKC, stepCMKM, stepCMKK, stepCYKC, stepCYKY, stepCYKK, stepMYKM, stepMYKY, stepMYKK]
    elif mode == 4:  # 四色模式且不为零的中心值大于1个时
        stepC, stepm, stepY, stepK = generate_count_step_mode_4(midC, midM, midY, midK, count)
        allStep = [stepC, stepm, stepY, stepK]
    return allCount, allStep


def generate_count_step_step(mid, count, countLeft):
    step = round(mid / (count + countLeft), 1)
    if step * (count + countLeft) > mid:
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


def generate_count_step_mode_1(mid, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step = generate_count_step_step(mid, count, countLeftTemp)
    return count + countLeftTemp, step, countLeft


def generate_count_step_mode_2(mid1, mid2, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(mid1, count, countLeftTemp)
    step2 = generate_count_step_step(mid2, count, countLeftTemp)
    return count + countLeftTemp, step1, step2, countLeft


def generate_count_step_mode_3(mid1, mid2, mid3, count, countLeft):
    countLeftTemp, countLeft = generate_count_step_count(countLeft)
    step1 = generate_count_step_step(mid1, count, countLeftTemp)
    step2 = generate_count_step_step(mid2, count, countLeftTemp)
    step3 = generate_count_step_step(mid3, count, countLeftTemp)
    return count + countLeftTemp, step1, step2, step3, countLeft


def generate_count_step_mode_4(mid1, mid2, mid3, mid4, count):
    step1 = generate_count_step_step(mid1, count, 0)
    step2 = generate_count_step_step(mid2, count, 0)
    step3 = generate_count_step_step(mid3, count, 0)
    step4 = generate_count_step_step(mid4, count, 0)
    return step1, step2, step3, step4


# 生成单张图片的函数
# 输入参数：sideX, midX 都是百分比，如sideC是10%，则 sideC = 0.1。sideX和midX默认值为0，当四个通道都是0的时候，图像不变。
def generate_one_image(image_data, sideC, midC, sideM, midM, sideY, midY, sideK, midK):
    return_data = image_data.copy()
    if (sideC != 0.0) or (midC != 0.0):
        klc, blc, krc, brc = generate_function([0, sideC], [127, midC], [255, sideC])
        return_data[:, :, 0] = np.where(return_data[:, :, 0] < 127, (klc * return_data[:, :, 0] + blc + 1) * return_data[:, :, 0],
                                        np.where((krc * return_data[:, :, 0] + brc + 1) * return_data[:, :, 0] > 255, 255,
                                                 (krc * return_data[:, :, 0] + brc + 1) * return_data[:, :, 0]))
    if (sideM != 0.0) or (midM != 0.0):
        klm, blm, krm, brm = generate_function([0, sideM], [127, midM], [255, sideM])
        return_data[:, :, 1] = np.where(return_data[:, :, 1] < 127, (klm * return_data[:, :, 1] + blm + 1) * return_data[:, :, 1],
                                        np.where((krm * return_data[:, :, 1] + brm + 1) * return_data[:, :, 1] > 255, 255,
                                                 (krm * return_data[:, :, 1] + brm + 1) * return_data[:, :, 1]))
    if (sideY != 0.0) or (midY != 0.0):
        kly, bly, kry, bry = generate_function([0, sideY], [127, midY], [255, sideY])
        return_data[:, :, 2] = np.where(return_data[:, :, 2] < 127, (kly * return_data[:, :, 2] + bly + 1) * return_data[:, :, 2],
                                        np.where((kry * return_data[:, :, 2] + bry + 1) * return_data[:, :, 2] > 255, 255,
                                                 (kry * return_data[:, :, 2] + bry + 1) * return_data[:, :, 2]))
    if (sideK != 0.0) or (midK != 0.0):
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


if __name__ == '__main__':
    pass
