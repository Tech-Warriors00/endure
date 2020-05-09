# this is my(Ashutosh Paul) algorithm; created by me. It is used to allot batches as per user-preference.
import math


class MyDictionary(dict):
    def __init__(self):
        self = dict()

    # function to add key: value
    def add(self, key, value):
        self[key] = value


def paulsAlgorithm(numSlots, list):
    """
    :param numSlots: number of batches
    :param list: list containing user's batch-preferences
    """
    # step 1 : store in ASC order (min number of 1's to max number of 1's)
    sorted = []
    for i in range(numSlots + 1):      # 0, 1, 2, 3...
        index = 0
        while index < len(list):          # [1, 1 , 0, 0], [0, 0, 1, 0], [1, 0, 0, 1]...
            x = list[index]
            oneCount = 0
            for y in x:         # 1, 1, 0, 0 -> 0, 0, 1, 0...
                if y == 1:
                    oneCount += 1
            # y ends
            if oneCount == i:
                sorted.append(x)        # insert x (current list) at the end of sorted
                list.remove(x)          # remove x (element which was inserted to sorted)
                continue

            index += 1
        # index ends
    # i ends

    print('sorted:')
    for x in sorted:
        print(x)
    print('list:')
    for x in list:
        print(x)
    print('end')

    # step 2: initialize slots
    batch = []
    for x in range(numSlots):
        batch.append([])

    for x in batch:
        print(x)
    print('end')

    # step 3: calculate n
    n = int(math.ceil(len(sorted)/numSlots))
    print('n:', n)

    # step 4: batch allotment
    for j in range(n):
        for x in range(numSlots):       # x = 0, 1, 2... (numSlots - 1)
            isRemembered = False
            remembered = []

            index = -1
            for y in sorted:            # y = [0, 0, 1, 0], [0, 0, 0, 1], [0, 1, 0, 0], [1, 0, 0, 1]...
                index += 1
                if -1 not in y and y[x] == 1:
                    batch[x].append(sorted[index])

                    sorted[index][x] = -1
                    isRemembered = False
                    print('>>>', sorted[index], '\t\tIndex + 1:', index + 1, 'y:', y)
                    break
                if -1 in y and y[x] == 1 and isRemembered is False:
                    isRemembered = True
                    remembered = y
                    print('Remembered:', remembered, 'at index + 1:', index+1)

            # y loop over BUT batch[x] not appended. Then append rememberIndex
            if isRemembered is True:
                batch[x].append(remembered)
                print('-1>', remembered)
                sorted[index][x] = -1
        # x ends
    # j ends

    # step 5: check for special cases
    """
    Eg.: sorted: [,,0,],[,,0,],[,,0,],[,,0,],... NO ONE CHOOSE BATCH 3 (here) OR SOME OTHER BATCH
    """
    isSpecialBatch = False
    specialBatch = []
    index = -1
    for x in batch:
        index += 1
        if len(x) < n:
            isSpecialBatch = True
            specialBatch.append(index)
    # x ends

    if isSpecialBatch is True:
        print('Special Batches:', specialBatch)

        # start filling batches which were found either empty or incomplete
        for x in specialBatch:
            print('Current Special Batch:', x)
            startingPoint = 0

            toAllot = n - len(batch[x])
            print('To Allot:', toAllot, 'in', x, 'batch[', x, ']:', batch[x])
            for y in sorted[: startingPoint: -1]:
                print('>', y)
                batch[x].append(y)
                toAllot -= 1
                if toAllot == 0:
                    startingPoint = startingPoint - len(batch[x])
                    if startingPoint < 0:
                        startingPoint = len(batch[x]) - 1
                    break
            # y ends
        # x ends

    print('Batches allotted:')
    for x in batch:
        print(x)

    # finally, return the batches
    return batch


def sendInput(n, preferences):
    """
    :param n: number of Slots
    :param preferences: dictionary input as 'shopName': [preference] (type: List)
    """
    # step 1: batch allotment
    res = paulsAlgorithm(n, preferences)
    print('res:')
    print(res)

    # step 2: convert all -1's to 1
    indexOne = -1
    for x in res:
        indexOne += 1
        indexTwo = -1
        for y in x:
            indexTwo += 1
            indexThree = -1
            for z in y:
                indexThree += 1
                if z == -1:
                    res[indexOne][indexTwo][indexThree] = 1
            # z ends
        # y ends
    # x ends

    print('Modified res:')
    for x in res:
        print(x)

    # step 3: get names and remove 0's and 1's
    answer = []
    index = -1
    for x in res:
        index += 1
        answer.append([])
        for y in x:
            for z in y:
                if type(z) == str:
                    answer[index].append(z)
                    break

    print('\nanswer:')
    print(answer)

    # step 4: convert to dictionary
    finalResult = MyDictionary()
    index = 1
    for x in answer:
        finalResult.add(index, x)
        index += 1
    # x ends

    print('\n\nFinal allotment:')
    for x in finalResult:
        print(x, 'value:', finalResult.get(x))

    return finalResult


list = [
            [1, 0, 0, 0, 'x1'],
            [1, 0, 0, 0, 'x2'],
            [0, 0, 0, 1, 'x3'],
            [1, 0, 0, 0, 'x4'],
            [1, 0, 0, 1, 'x5'],
            [0, 0, 0, 1, 'x6'],
            [1, 0, 0, 0, 'x7'],
            [1, 0, 0, 1, 'x8'],
            [1, 0, 0, 1, 'x9'],
            [1, 0, 0, 1, 'x10'],
            [1, 0, 0, 1, 'x11'],
            [1, 0, 0, 1, 'x12'],
            [1, 0, 0, 1, 'x13']
    ]
'''
list = [
            [0, 1, 0, 0, 'x1'],
            [1, 0, 0, 0, 'x2'],
            [0, 0, 0, 1, 'x3'],
            [1, 0, 0, 0, 'x4'],
            [1, 0, 0, 1, 'x5'],
            [0, 1, 0, 1, 'x6'],
            [1, 1, 0, 0, 'x7'],
            [1, 0, 0, 1, 'x8'],
            [1, 1, 0, 1, 'x9'],
            [1, 1, 0, 1, 'x10'],
            [1, 1, 0, 1, 'x11'],
            [1, 1, 0, 1, 'x12'],
            [1, 1, 0, 1, 'x13']
    ]
'''

'''
list = [
            [1, 1, 0, 0, 'x6'],
            [0, 0, 1, 1, 'x7'],
            [0, 0, 1, 0, 'x1'],
            [1, 0, 0, 1, 'x4'],
            [1, 0, 0, 1, 'x5'],
            [0, 1, 1, 0, 'x8'],
            [1, 1, 0, 0, 'x9'],
            [0, 1, 1, 1, 'x10'],
            [0, 1, 1, 1, 'x13'],
            [1, 1, 1, 1, 'x14'],
            [1, 1, 1, 1, 'x15'],
            [0, 0, 0, 1, 'x2'],
            [0, 1, 0, 0, 'x3'],
            [1, 1, 1, 0, 'x11'],
            [1, 1, 0, 1, 'x12']
    ]
'''
'''
list = [
    [1, 1, 0, 0, 'varungupta@outlook.com'],
    [0, 1, 1, 0, 'daniell@outlook.com'],
    [0, 0, 1, 0, 'meet.ashutosh.paul@outlook.com'],
]
'''
#sendInput(4, list)
