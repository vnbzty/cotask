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
        proc_time = np.linspace(0.1, 10, 100)
        self.up_link = np.linspace(0.1, 0.3, self.num_Cotask * self.num_ES)
        self.down_link = np.linspace(0.1, 0.3, self.num_Cotask * self.num_ES)

        if self.num_task >= 100:
            for i in xrange(self.num_Cotask):
                for j in xrange(self.num_task / 100):
                    self.tasks = np.concatenate((self.tasks, proc_time))
        else:
            for i in xrange(self.num_Cotask):
                self.tasks = np.concatenate((self.tasks, proc_time[0:self.num_task]))


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


def calc(data, mobile, ES, MD):
    # print ES
    # print MD

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

    for i in xrange(data.num_ES):
        ES[i].sort(key=lambda x: data.up_link[x[1]][i])
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
    print CCT
    print TCT
    # print UL
    # print DL
    # print Proc
    # print WaitES
    WaitMD = [CCT[Seq[x]] - TCT[x] for x in xrange(len(Seq))]
    # print WaitMD

    return CCT, TCT, UL, DL, Proc, WaitES, WaitMD


def schedule(data, mobile):
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
    CCT, TCT, UL, DL, Proc, WaitES, WaitMD = calc(data, mobile, ES, MD)

    print np.average(CCT)
    print np.var(CCT)
    print np.average(TCT)
    print np.var(TCT)
    print np.average(UL)
    print np.average(DL)
    print np.average(Proc)
    print np.sum(WaitES)
    print np.sum(WaitMD)
    print


def RR_FCFS(data, mobile):
    round_robin(data, mobile)
    schedule(data, mobile)

def NO_MEC(data):
    data.offload = np.zeros((data.num_Cotask, data.num_task))
    schedule(data, 1)

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

def MINRT_FCFS(data, mobile):
    minrt(data, mobile)
    schedule(data, mobile)

def main():
    data1 = Data(1, 2, 3, 1000, 2.0)

    NO_MEC(data1)
    RR_FCFS(data1,0)
    RR_FCFS(data1,1)
    MINRT_FCFS(data1,0)
    MINRT_FCFS(data1,1)


if __name__ == '__main__':
    main()
