# coding: utf-8
import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import argparse
import sys
sys.path.append("..")
from src.util import *


class Cam:

    #原点是旋转凸轮的圆心
    #L1: 第一个圆心到坐标原点O的线段
    #L2: 第一个圆心的垂线
    #B点: self.A1_radis_l末端点
    #P点: self.A1_radis_r末端点
    #ps: 原点到P点的距离
    #C点: self.A2_radis_l末端点
    #D点：self.A1_radis_l和self.A2_radis_l的交点
    
    def __init__(self):
       
        #第一个圆
        self.A1_x = 8.48
        self.A1_y = 43.50
        self.A1_radis_l = 73.85
        self.A1_radis_r = 35.90
        self.A1_r_l_a = 129.80
        
        #第二个圆
        self.A2_x = 95
        self.A2_y = 48.23    
        self.A2_radis_l = 52.15
        
        #这个值不需要设置，取一个大于0即可
        self.A2_radis_r = 5
        
        self.A2_r_l_a = 173.16      
        #需要加上100度到最高点的距离
        self.maxHigh = 85.80
       
    
    #给出右边挑线的垂直距离，得到极坐标的半径(原点到P点的距离ps)    
    def  getP(self, height):
        #计算B点坐标
        #print(height, self.A2_y,  self.A2_radis_r)
        a = 180 * math.asin((height - self.A2_y) / self.A2_radis_l) / math.pi
        #a = self.A2_r_l_a - ( 90 + a)
        #a = 90  - a      
        a = 360 - (self.A2_r_l_a - a)
        l_a =  math.pi * a / 180    
        
        x = self.A2_x + self.A2_radis_r * math.cos(l_a)
        y = self.A2_y + self.A2_radis_r * math.sin(l_a)
        
        #求出self.A1_radis_l的直线方程y = kx + d
        k = ( y - self.A2_y ) / ( x - self.A2_x)
        d = y  - k * x
        
        #求解方程 (x- A1x) ** 2 + (y - A1y) **2 = A1_radis_l**2 和 y = kx + d
        t = twoSolve(k, d, self.A1_x, self.A1_y, self.A1_radis_l)        
        Dx = t[0][0]
        Dy = t[0][1]
        if t[0][0] < t[1][0]: 
            Dx = t[1][0]
            Dy = t[1][1]
        
        #A1 到原点距离
        A1O = math.sqrt(self.A1_x **2 + self.A1_y **2)
        #D点到原点距离
        DO =  math.sqrt(Dx **2 + Dy **2)
        #求出角 D A1 O
        DA1O = 180 * cosx(DO, A1O, self.A1_radis_l) / math.pi
        #求出角 P A1 O 
        PA1O = DA1O - self.A1_r_l_a        
        ar = PA1O * math.pi / 180  
        
        ret = math.sqrt((A1O **2 + self.A1_radis_r **2 - 2 * A1O * self.A1_radis_r * math.cos(ar))) 
        return ret      
    
    #输入极坐标得到挑线的坐标
    def getC(self, ps):
        #A1 到原点距离
        A1O = math.sqrt(self.A1_x **2 + self.A1_y **2)
        #求出角 P A1 O
        PA1O = 180 * cosx(ps, A1O, self.A1_radis_r) / math.pi
        A1OM = 180 - 180 * math.atan2(self.A1_y, self.A1_x) / math.pi 
        #A1OM = 180 * math.atan(self.A1_y / self.A1_x) / math.pi 
        
        BA1M = PA1O + self.A1_r_l_a - A1OM 
        
        #B点坐标
        ar = math.pi * BA1M / 180 
        Bx = self.A1_x + self.A1_radis_l * math.cos(ar)
        By = self.A1_y + self.A1_radis_l * math.sin(ar)        
        
        BA2M =  180 * math.atan2(Bx - self.A2_x, By - self.A2_y) / math.pi
        #BA2M =  180 * math.atan((Bx - self.A2_x) / (By - self.A2_y)) / math.pi
        if BA2M < 0 : BA2M = 180 + BA2M
        a = self.A2_r_l_a - 90 - BA2M
        ar = math.pi * a / 180 
        Cx = self.A2_x + self.A2_radis_l * math.cos(ar)
        Cy = self.A2_y + self.A2_radis_l * math.sin(ar)
        return Cx, Cy
        
    '''    
    #相对距离转绝对距离
    #相对距离：表示相对最高(低)点的距离 绝对距离: 相对原点的垂直距离

    转动度数 相对距离 -> 转动度数 绝对距离  
    50       -0.34       50       83.65     
    '''
    def Redst2Abdst(self, ans):    
        #排序
        idx = np.argsort(ans[:, 0])
        ans = ans[idx]
        ma = ans[:, 1].argmax()    
        ans = np.concatenate((ans[ma:], ans[:ma]),  axis=0)         
        ans[:,1] = self.maxHigh + ans[:,1]
        return ans

    
    
    #转动度数细分
    #间隔5度的数组，进行更细微的细分
    def datasplit(self, ans):
        
        #转动度数 绝对距离 -> 转动度数 绝对距离  上一度数到本度数移动的距离 上一度数的绝对距离    
        #上一度数到本度数移动的距离 
        loss = np.array([ans[0, 1] - self.maxHigh] + (ans[1:, 1] - ans[:-1, 1]).tolist())
        ans = np.concatenate((ans, loss[:, None]), axis=1)     
        #上一度数的绝对距离
        ans = np.concatenate((ans, (ans[:, 1] - ans[:, 2])[:, None]), axis=1) 
        #细分
        temp = []
        for one in ans:
            for i in range(1, 6):    
                angle = one[0] - 5 + i 
                offset = one[3] + i * one[2] / 5       
                temp.append([angle, offset])        
        return np.array(temp)


#输入最大最小极坐标，求出行程距离
def testDst(setup_path, a, b):
    obj = Cam()
    obj.read_cfg(setup_path)
    _, ay = obj.getC(a)
    _, by = obj.getC(b)
    return ay - by
    
    
def createRadis(obj, input_path, mode=1):
    #obj = Cam()
    #obj.read_cfg(setup_path)
    
    with open(input_path, 'r') as f:
        ans = []
        while True:
            line = f.readline()            
            temp = line.split()
            if not temp: break
            ans.append(line.split())
    ans = np.array(ans).astype(float)  
    ans = obj.Redst2Abdst(ans)     
                
    
    if mode == 1:    
        ans = obj.datasplit(ans) 
    ret = []    
    for i, one in enumerate(ans):        
        rad = obj.getP(one[1])
        one[0] = int(one[0]) % 360        
        ret.append([one[0], one[1], rad])
    
    ret = np.array(ret)
    t = np.argsort(ret[:,0])      
    ret = ret[t]
    return ret    
    

def createCadFile(obj, input_path, output_path, mode=0):
    
    ret = createRadis(obj, input_path, mode)
    if ret.size == 0:
        raise Exception("create 出错")    
        
    with open(output_path, 'w') as f:
        f.write('P_SPLINE\t\t\n')
        f.write('OPEN\t\t\n')
        f.write('%d\t\t\n' %(602))
        for one in ret:                   
           f.write('%.3f,%d,0\n' %(one[2], int(one[0])))                      
        f.write('EOF\t\t\n')   
     
     
if __name__ == '__main__': 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=0, metavar='mode', help='input run mode (default: 1)')    
    args = parser.parse_args()  
    
    
    setup_path = '../config/cam_setup.txt'
    input_path =  '../pppttt.txt'
    output_path = './cam_output.dat' 
    
    
    obj = Cam()
    obj.read_cfg(setup_path)
    h = obj.getP(89.31)
    h1 = obj.getP1(89.31)
    
    print(h, h1)
    
    exit()
    x, y = obj.getC(19.833)
    x1, y1 = obj.getC(29.628)
    print(x, y, x1, y1, y-y1)
    exit()
    createCadFile(setup_path, input_path, output_path)
    
    
        
    
  