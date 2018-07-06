import pickle
import ast
import json
import sys
import matplotlib
from numpy.core.multiarray import ndarray

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from numpy import nan


class Data:
    def __init__(
            self,
            num_iter,
            num_ES,
            num_Cotask,
            num_task,
            ratio
    ):
        self.num_iter = num_iter
        self.num_ES = num_ES
        self.num_Cotask = num_Cotask
        self.num_task = num_task
        self.ratio = ratio
        self.tasks = np.array([])
        self.up_link = np.array([])
        self.down_link = np.array([])

    def generate(self):
        # proc_time = np.linspace(0.1, 10, 100)
        self.tasks = np.random.exponential(3, self.num_Cotask * self.num_task)
        # print np.average(self.tasks)

        self.up_link = np.random.uniform(0.1, 0.3, self.num_Cotask * self.num_ES)
        self.down_link = np.random.uniform(0.1, 0.3, self.num_Cotask * self.num_ES)

        # if self.num_task >= 100:
        #     for i in xrange(self.num_Cotask):
        #         for j in xrange(self.num_task / 100):
        #             self.tasks = np.concatenate((self.tasks, proc_time))
        # else:
        #     for i in xrange(self.num_Cotask):
        #         self.tasks = np.concatenate((self.tasks, proc_time[0:self.num_task]))

        self.tasks = np.reshape(self.tasks, (self.num_Cotask, self.num_task))
        self.up_link = np.reshape(self.up_link, (self.num_Cotask, self.num_ES))
        self.down_link = np.reshape(self.down_link, (self.num_Cotask, self.num_ES))
        # print self.tasks


def round_robin(data,mobile):
    num_select = data.num_ES + mobile
    # print num_select
    offload = np.array([])
    for j in xrange(data.num_Cotask):
        offload = np.concatenate((offload, [(x % num_select) for x in xrange(data.num_task)]))

    offload = np.reshape(offload, (data.num_Cotask, data.num_task))
    data.offload = offload
    # print data.tasks
    # print offload

def minrt(data, mobile):
    # print num_select
    offload = np.array([])
    for j in xrange(data.num_Cotask):
        for i in xrange(data.num_task):
            tmp = [data.up_link[j][x] + data.down_link[j][x] + data.tasks[j][i] / data.ratio for x in xrange(data.num_ES)]
            if (mobile == 1):
                tmp.insert(0, data.tasks[j][i])

            offload = np.append(offload, np.argmin(tmp))


    offload = np.reshape(offload, (data.num_Cotask, data.num_task))
    data.offload = offload
    # print offload

# def fcfs(data, mobile, ES, MD):
#     # print ES
#     # print MD
#
#     CCT = [0 for i in xrange(data.num_Cotask)]
#     TCT = []
#     UL = [0 for i in xrange(data.num_Cotask)]
#     DL = [0 for i in xrange(data.num_Cotask)]
#     Proc = []
#     WaitES = []
#     Seq = []
#     if mobile == 1:
#         for i in xrange(data.num_Cotask):
#             if len(MD[i]) > 0:
#                 Seq.append(i)
#                 CCT[i] = MD[i][0]
#                 Proc.append(MD[i][0])
#                 TCT.append(MD[i][0])
#
#     for i in xrange(data.num_ES):
#         ES[i].sort(key=lambda x: data.up_link[x[1]][i])
#     for i in xrange(data.num_ES):
#         now = 0
#         for j in xrange(len(ES[i])):
#             cotask = ES[i][j][1]
#             Seq.append(cotask)
#             Proc.append(ES[i][j][0])
#             WaitES.append(max(0, now - data.up_link[cotask][i]))
#             now = max(now + ES[i][j][0], data.up_link[cotask][i] + ES[i][j][0])
#             CCT[cotask] = max(CCT[cotask], now + data.down_link[cotask][i])
#             TCT.append(now + data.down_link[cotask][i])
#             UL[cotask] += data.up_link[cotask][i]
#             DL[cotask] += data.down_link[cotask][i]
#     # print Seq
#     # print CCT
#     # print TCT
#     # print UL
#     # print DL
#     # print Proc
#     # print WaitES
#     WaitMD = [CCT[Seq[x]] - TCT[x] for x in xrange(len(Seq))]
#     # print WaitMD
#
#     return CCT, TCT, UL, DL, Proc, WaitES, WaitMD

def lcls(data, mobile, ES, MD):
    CCT = [0 for i in xrange(data.num_Cotask)]
    TCT = []
    UL = [0 for i in xrange(data.num_Cotask)]
    DL = [0 for i in xrange(data.num_Cotask)]
    Proc = []
    WaitES = []
    Seq = []

    if mobile == 1:
        for i in xrange(data.num_Cotask):
            Seq.append(i)
            CCT[i] = MD[i][0]
            Proc.append(MD[i][0])
            TCT.append(MD[i][0])

    order = range(data.num_Cotask)
    order.sort(key=lambda x: min(data.up_link[x]))

    value = [0 for x in xrange(data.num_Cotask)]
    for i in xrange(data.num_Cotask):
        value[order[i]] = i

    # print order
    # print value

    for i in xrange(data.num_ES):
        ES[i].sort(key=lambda x: value[x[1]])

    for i in xrange(data.num_ES):
        now = 0
        for j in xrange(len(ES[i])):
            cotask = ES[i][j][1]
            Seq.append(cotask)
            Proc.append(ES[i][j][0])
            WaitES.append(max(0, now - data.up_link[cotask][i]))
            now = max(now + ES[i][j][0], data.up_link[cotask][i] + ES[i][j][0])
            CCT[cotask] = max(CCT[cotask], now + data.down_link[cotask][i])
            TCT.append(now + data.down_link[cotask][i])
            UL[cotask] += data.up_link[cotask][i]
            DL[cotask] += data.down_link[cotask][i]
    # print Seq
    # print CCT
    # print TCT
    # print UL
    # print DL
    # print Proc
    # print WaitES
    WaitMD = [CCT[Seq[x]] - TCT[x] for x in xrange(len(Seq))]
    # print WaitMD

    return CCT, TCT, UL, DL, Proc, WaitES, WaitMD

def lcls(data, mobile, ES, MD):
    CCT = [0 for i in xrange(data.num_Cotask)]
    TCT = []
    UL = [0 for i in xrange(data.num_Cotask)]
    DL = [0 for i in xrange(data.num_Cotask)]
    Proc = []
    WaitES = []
    Seq = []

    if mobile == 1:
        for i in xrange(data.num_Cotask):
            Seq.append(i)
            CCT[i] = MD[i][0]
            Proc.append(MD[i][0])
            TCT.append(MD[i][0])

    order = range(data.num_Cotask)
    order.sort(key=lambda x: max(data.up_link[x]))

    value = [0 for x in xrange(data.num_Cotask)]
    for i in xrange(data.num_Cotask):
        value[order[i]] = i

    # print order
    # print value

    for i in xrange(data.num_ES):
        ES[i].sort(key=lambda x: value[x[1]])

    for i in xrange(data.num_ES):
        now = 0
        for j in xrange(len(ES[i])):
            cotask = ES[i][j][1]
            Seq.append(cotask)
            Proc.append(ES[i][j][0])
            WaitES.append(max(0, now - data.up_link[cotask][i]))
            now = max(now + ES[i][j][0], data.up_link[cotask][i] + ES[i][j][0])
            CCT[cotask] = max(CCT[cotask], now + data.down_link[cotask][i])
            TCT.append(now + data.down_link[cotask][i])
            UL[cotask] += data.up_link[cotask][i]
            DL[cotask] += data.down_link[cotask][i]
    # print Seq
    # print CCT
    # print TCT
    # print UL
    # print DL
    # print Proc
    # print WaitES
    WaitMD = [CCT[Seq[x]] - TCT[x] for x in xrange(len(Seq))]
    # print WaitMD

    return CCT, TCT, UL, DL, Proc, WaitES, WaitMD

def schedule(data, mobile, method):
    num_select = data.num_ES + mobile
    ES = [[] for x in xrange(data.num_ES)]
    MD = [[] for x in xrange(data.num_Cotask)]
    for j in xrange(data.num_Cotask):
        for i in xrange(num_select):
            proc_time = sum([data.tasks[j][x] for x in xrange(data.num_task) if data.offload[j][x] == i])
            if proc_time == 0:
                continue
            if mobile == 0:
                ES[i].append((proc_time / data.ratio, j))
            else:
                if i == 0:
                    MD[j].append(proc_time)
                else:
                    ES[i - mobile].append((proc_time / data.ratio, j))

    # CCT, TCT, UL, DL, Proc, WaitES, WaitMD = calc(data, ES, MD)
    CCT, TCT, UL, DL, Proc, WaitES, WaitMD = method(data, mobile, ES, MD)

    return np.average(CCT)

    # print np.average(CCT)
    # print np.var(CCT)
    # print np.average(TCT)
    # print np.var(TCT)
    # print np.average(UL)
    # print np.average(DL)
    # print np.average(Proc)
    # print np.sum(WaitES)
    # print np.sum(WaitMD)
    # print


# def RR_FCFS(data, mobile):
#     round_robin(data, mobile)
#     return schedule(data, mobile, fcfs)

def NO_MEC(data):
    data.offload = np.zeros((data.num_Cotask, data.num_task))
    return schedule(data, 1, fcfs)

# def MINRT_FCFS(data, mobile):
#     minrt(data, mobile)
#     return schedule(data, mobile, fcfs)
#
# def COOL(data, mobile):
#     round_robin(data, mobile)
#     return schedule(data, mobile, lcls)

def RR_LCLS(data, mobile):
    round_robin(data, mobile);
    return schedule(data, mobile, lcls)

def MINRT_LCLS(data, mobile):
    minrt(data, mobile)
    return schedule(data, mobile, lcls)

def main():
    for numMD in xrange(1,11):
        data = Data(100, 3, numMD, 100, 2.0)
        CCT = [[] for x in xrange(3)]
        for iterator in xrange(data.num_iter):
            data.generate()
            CCT[0].append(NO_MEC(data))
            CCT[1].append(RR_LCLS(data,1))
            CCT[2].append(MINRT_LCLS(data,1))

        result = np.average(CCT, axis=1)
        for i in xrange(3):
            print result[i]
        print

if __name__ == '__main__':
    main()
