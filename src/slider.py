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


class Slider:
    
    def __init__(self):
    
        #第一个圆的坐标和半径
        self.A1_x = 0 
        self.A1_y = 0 
        self.A1_radis = 9.2
        
        #第二个圆的坐标和半径 
        self.A2_x = 51 
        self.A2_y = -17     
        self.A2_radis = 23.75
    
        #连接点到第二个圆心的距离
        self.A2_radis_r = 56.143
        #连接点到第二个圆的半径的距离
        self.A2_radis_l = 33.5
        
        #第一个圆和第二个园连杆距离
        self.A1A2_lg = 51.65
        
        #滑块的坐标y值
        self.yb = 38 #63
        
        #滑块点和连接点之间距离
        self.A3_radis = 21        
        
    def procInput(self):
    
        #计算连接点到第二个圆的半径之间的偏角
        self.A2angle = 180 * cosx(self.A2_radis_l,  self.A2_radis_r, self.A2_radis) / math.pi
        
        #计算第一个圆心和第二个圆心的距离
        self.A1A2_ds = math.sqrt((self.A1_x - self.A2_x) **2 + (self.A1_y - self.A2_y) **2)   
    
        #判断滑块的区间
        self.up =  self.yb >= self.A2_y 
        '''
        print(self.A1_x)
        print(self.A1_y)
        print(self.A1_radis)
        print(self.A2_x)
        print(self.A2_y)
        print(self.A2_radis)
        print(self.A2_radis_r)
        print(self.A2_radis_l)
        print(self.A1A2_lg)
        print(self.yb)
        print(self.A3_radis)
        print(self.A2angle)
        print(self.A1A2_ds)
        print(self.up)
        print('***********')        
        '''
        
    def read_cfg(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            while True:
                line = f.readline()                
                if len(line) == 0: break
                line = line.strip()      
                if len(line) == 0:continue                 
                if line[0] == '#': continue                
                temp = line.split()
                if not temp: continue
                if temp[0] == 'A1_x': self.A1_x = float(temp[2])
                if temp[0] == 'A1_y': self.A1_y = float(temp[2])
                if temp[0] == 'A1_radis': self.A1_radis = float(temp[2])
                if temp[0] == 'A2_x': self.A2_x = float(temp[2])
                if temp[0] == 'A2_y': self.A2_y = float(temp[2])
                if temp[0] == 'A2_radis': self.A2_radis = float(temp[2])                
                if temp[0] == 'A2_radis_r': self.A2_radis_r = float(temp[2])
                if temp[0] == 'A2_radis_l': self.A2_radis_l = float(temp[2])                
                if temp[0] == 'A1A2_lg': self.A1A2_lg = float(temp[2])
                if temp[0] == 'yb': self.yb = float(temp[2])
                if temp[0] == 'A3_radis': self.A3_radis = float(temp[2])
                '''
                print(self.A1_x)
                print(self.A1_y)
                print(self.A1_radis)
                print(self.A2_x)
                print(self.A2_y)
                print(self.A2_radis)
                print(self.A2_radis_r)
                print(self.A2_radis_l)
                print(self.A1A2_lg)
                print(self.yb)
                print(self.A3_radis)
                print('***********')
                '''
                
                
    def readPara(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            ans = []
            while True:
                line = f.readline()                
                if len(line) == 0: break
                line = line.strip()      
                if len(line) == 0:continue                 
                if line[0] == '#': continue                
                temp = line.split()
                if not temp: continue
                ans.append(temp)
        return np.array(ans).astype(float)        
    
    
    def findPara(self, path, minv=2.45, line=100):
        ret = self.readPara(path)
        ma, mi, ans = self.findanglelimit()
        #print(ma,mi)        
        mindst = self.getdistance(mi[0], mi[0]+23)
        print('原始最小距离是', mindst)
        totaldst = self.getdistance(mi[0], ma[0])
        print('原始最长距离', totaldst)       
        
        #A2圆半径
        if ret[0][0] == ret[0][1]:
            AList = np.array([ret[0][1]])
        else:    
            AList = np.arange(ret[0][0], ret[0][1], ret[0][2])
        #A2半径到连接点距离
        if ret[1][0] == ret[1][1]:
            BList = np.array([ret[1][1]])
        else:         
            BList = np.arange(ret[1][0], ret[1][1], ret[1][2])  
        
        #连杆
        if ret[2][0] == ret[2][1]:
            CList = np.array([ret[2][1]])
        else:    
            CList = np.arange(ret[2][0], ret[2][1], ret[2][2])
        
        #A2圆心坐标
        if ret[3][0] == ret[3][1]:
            DList = np.array([ret[3][1]])
        else:    
            DList = np.arange(ret[3][0], ret[3][1], ret[3][2])
        
        if ret[4][0] == ret[4][1]:
            EList = np.array([ret[4][1]])
        else:                
            EList = np.arange(ret[4][0], ret[4][1], ret[4][2])
        isfind = False
        
        max = 0
        num = 0
        
        ansList = []
        for A in AList:
            for B in BList:
                if A + B <= self.A2_radis_r : continue
                if A + self.A2_radis_r <= B: continue
                if B + self.A2_radis_r <= A: continue    
                for C in CList: 
                    for D in DList:
                        for E in EList:                     
                            self.A2_radis = A    
                            self.A2_radis_l = B
                            self.A1A2_lg = C
                            self.A2_x = D
                            self.A2_y = E   
                            ma, mi, _ = self.findanglelimit()
                            v = self.getdistance(mi[0], ma[0])               
                            mindst = self.getdistance(mi[0], mi[0]+23)
                            #if v > totaldst + 0.2 or v < totaldst - 0.2: continue 
                            num += 1
                            if num % 20 == 0:
                                print('A2_rad:%.2f, A2_rad_l:%.2f,lg:%.2f,A2_x:%.2f,A2_y:%.2f,\
                                总距离: %.3f, 最小距离: %.3f' %(A, B, C, D, E, v, mindst) )
                            
                            if v > totaldst + 0.2 or v < totaldst - 0.2: continue                             
                            if mindst > max:
                                max = mindst
                                t1 = A
                                t2 = B 
                                t3 = C
                                t4 = D
                                t5 = E
                                t6 = v
                                t7 = mindst
                            if (mindst > minv + 0.1) or (mindst < minv): continue
                            ansList.append([A, B, C, D, E, v, mindst])                            
                            print('find best:')
                            print('A2_rad:%.2f, A2_rad_l:%.2f,lg:%.2f,A2_x:%.2f,A2_y:%.2f,\
                            总距离: %.3f, 最小距离: %.3f' %(A, B, C, D, E, v, mindst) )
                            
                            
                
        if  len(ansList) == 0: 
            print('没有找到合适的参数, 最好参数是:')
            if max > 0:
                print('A2_rad:%.2f, A2_rad_l:%.2f,lg:%.2f,A2_x:%.2f,A2_y:%.2f,\
            总距离: %.3f, 最小距离: %.3f' %(t1,t2,t3,t4,t5,t6,t7) )
        else:
            print('\n最好的参数:\n')
            ansList = np.array(ansList)
            idx = ansList[:, 6].argsort()
            ansList = ansList[idx]
            for ix, one  in enumerate(ansList):
                #print( ix, one)
                if ix == line : break
                print('A2_rad:%.2f, A2_rad_l:%.2f,lg:%.2f,A2_x:%.2f,A2_y:%.2f,\
                            总距离: %.3f, 最小距离: %.3f' %(one[0], one[1], one[2], one[3], one[4], one[5], one[6]))
                                        
    
    #第一个圆转动角度a, 求出滑块的位置
    def findsliderpos(self, a):
        #把a转化为连杆系统角度
        A1_a = angle2sysangle(self.A1_x, self.A1_y, self.A2_x, self.A2_y, a)
        
        #求出第二圆的连杆转动角度
        A2_a_up, A2_a_down = minorAngle(self.A1_radis, self.A2_radis, 
                  self.A1A2_ds, self.A1A2_lg, A1_a)
                  
                  
        if self.up: A2_a = A2_a_up
        else: A2_a = A2_a_down
        
        #把A2_a转为绝对坐标角度
        A2_abs_a =  sysangle2angle(self.A1_x, self.A1_y, self.A2_x, self.A2_y, A2_a)
        
        
        #减去连接点的夹角
        A2_abs_a = A2_abs_a - self.A2angle        
        
        
        #找到连接点的坐标
        ma =  math.pi *  A2_abs_a / 180    
        last_x = self.A2_x + self.A2_radis_r * math.cos(ma)
        last_y = self.A2_y + self.A2_radis_r * math.sin(ma)
        
        temp = math.sqrt(self.A3_radis **2 -  (self.yb - last_y) ** 2)
        
        #上区间返回左点，下区间返回右点
        return (last_x - temp, self.yb) if self.up else (last_x + temp, self.yb)
        

    #找出极限位置的相应角度
    def findanglelimit(self, offset=1):
    
        aglist = np.arange(0, 360, offset)
        temp = []
        for i in aglist:
            lg_i = angle2sysangle(self.A1_x, self.A1_y, self.A2_x, self.A2_y, i)
            up_a, down_a = minorAngle(self.A1_radis, self.A2_radis, self.A1A2_ds, 
                                      self.A1A2_lg, lg_i)              
            if self.up:
                angle = up_a
            else: 
                angle = down_a      
            pos = sysangle2angle(self.A1_x, self.A1_y, self.A2_x, self.A2_y, angle)   
            temp.append([i, lg_i, angle, pos])    
            
        temp = np.array(temp)
        max_id = temp[:, 3].argmax()
        min_id = temp[:, 3].argmin()
        ans = pd.DataFrame()
        ans['first_ag'] = temp[:, 0]
        ans['first_lg_ag'] = temp[:, 1]
        ans['second_lg_ag'] = temp[:, 2]
        ans['second_ag'] = temp[:, 3]                
        return temp[max_id], temp[min_id], ans
    

    #主动圆从a1角度转动到a2角度，求滑块移动的距离
    def getdistance(self, a1, a2):
        
        #找到最大最小位置时的角度
        max_ang, min_ang, _ = self.findanglelimit()
                
        dis = 0
        #a1角度的滑块位置
        a1_pos = self.findsliderpos(a1)
        #a2角度的滑块位置    
        a2_pos = self.findsliderpos(a2)
        
        #分情况处理
        if a1 <= min_ang[0]:
            if a2 <= min_ang[0]:                   
                dis =  abs(a2_pos[0] -  a1_pos[0])
            elif a2 <= max_ang[0]:
                temp = self.findsliderpos(min_ang[0])
                dis = abs(temp[0] - a1_pos[0]) + abs(a2_pos[0] - temp[0])            
            else:
                temp1 = self.findsliderpos(min_ang[0])
                dis += abs(temp1[0] - a1_pos[0])
                temp2 = self.findsliderpos(max_ang[0]) 
                dis += abs(temp1[0] - temp2[0]) + abs(a2_pos[0] - temp2[0])  
        elif a1 <= max_ang[0]:
            if a2 <= max_ang[0]:            
                dis =  abs(a1_pos[0] - a2_pos[0])
            else:  
                temp = self.findsliderpos(max_ang[0]) 
                dis =  abs(temp[0] - a1_pos[0]) + abs(a2_pos[0] - temp[0])
        else:
            dis =  abs(a1_pos[0] - a2_pos[0])            
        return dis            


def createDst1(setup_path, ans):
    obj = Slider()
    obj.read_cfg(setup_path)
    
    ma, mi, _ = obj.findanglelimit()    
    mindst = obj.getdistance(mi[0], mi[0]+23)
    totaldst = obj.getdistance(mi[0], ma[0])
    
    temp = [0]
    for pr, ne in zip(ans[:-1], ans[1:]):
        dst = obj.getdistance(pr, ne)
        temp.append(dst)    
    return np.array(temp), mindst, totaldst

def createDst(obj, ans):
    obj.procInput()    
    ma, mi, _ = obj.findanglelimit()    
    mindst = obj.getdistance(mi[0], mi[0]+23)
    totaldst = obj.getdistance(mi[0], ma[0])
    
    temp = [0]
    for pr, ne in zip(ans[:-1], ans[1:]):
        dst = obj.getdistance(pr, ne)
        temp.append(dst)    
    return np.array(temp), mindst, totaldst
    
def calDst(obj):
    obj.procInput()    
    ma, mi, _ = obj.findanglelimit()    
    mindst = obj.getdistance(mi[0], mi[0]+23)
    totaldst = obj.getdistance(mi[0], ma[0])
    return mindst, totaldst
    
    

def showSliderInfo(setup_path, mode=1):
    obj = Slider()
    obj.read_cfg(setup_path)
    ma, mi, ans = obj.findanglelimit()
    print(ma,mi)

    mindst = obj.getdistance(mi[0], mi[0]+23)
    print('最低点转23度:',  int(mi[0]), int(mi[0]+23), mindst)
    totaldst = obj.getdistance(mi[0], ma[0])
    print('total distance:', totaldst)
    
    if mode == 1: offset = 1
    else: offset = 5
    
    temp = np.arange(0, 360, offset)
    temp = np.append(temp, [360]) + int(mi[0])
    temp1 = (temp + int(178 - mi[0])) % 360
       
    temp = dict(zip(temp, temp1))  
    temp = list(zip(temp.keys(), temp.values()))
    
    ans = []
    for pr, ne in zip(temp[:-1], temp[1:]):
        dst = obj.getdistance(pr[0], ne[0])
        ans.append([pr[1], ne[1], dst])    
    ans = np.array(ans)    
    ret = pd.DataFrame()
    ret['start'] = ans[:,0].astype(int)
    ret['end'] = ans[:,1].astype(int)
    ret['dst'] = ans[:,2]    
    pd.set_option('display.max_rows', None)
    print(ret)
     
if __name__ == '__main__': 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=0, metavar='mode', help='input run mode (default: 1)')    
    args = parser.parse_args()
    
    setup_path = '../config/slider_setup.txt'
    
    #createDst(setup_path, offset=5)
    #exit()
    if args.m == 0:
        showinfo(setup_path, mode=1)
    elif args.m == 1:
        obj = Slider()
        obj.findPara('../config/para.txt')
        
    
  