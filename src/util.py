# coding: utf-8
import numpy as np
import math



#计算3角形边长a对应的角
def cosx(a, b, c):
        cos = (b*b + c*c - a*a) / (2 * b * c)
        return math.acos(cos)    


'''
主动圆转动a角度，求被动圆转的角度:    
设置两圆心之间连线作为初始线
A1 是主动圆， A2是被动圆
C1 是主动圆转动a角度后的点  C2是被动圆连杆位置
A1A2 : 两圆心之间的距离
LG: 连杆距离        
返回上下两个位置角度
'''
def minorAngle(A1_radis, A2_radis, A1A2, LG, a):    

    #分为两种情况
    if a <= 180:     
        ar = a * math.pi / 180
        #计算主动圆转动a度后的C1点到被动圆心A2的距离
        c1a2 = math.sqrt((A1_radis **2 + A1A2 **2 - 2 * A1_radis * A1A2 * math.cos(ar))) 
        
        #计算C1A2C2的角度
        c1a2c2 = 180 * cosx(LG, c1a2, A2_radis) / math.pi    
        
        #计算C1A2A1的角度
        c1a2a1 = 180 * cosx(A1_radis, A1A2, c1a2) / math.pi
        
        pos_up = 180 - (c1a2c2 + c1a2a1)
        pos_down = 180 + (c1a2c2 - c1a2a1)
        
    else:
        ar = (360 - a) * math.pi / 180      
        #计算主动圆转动a度后的C1点到被动圆心A2的距离
        c1a2 = math.sqrt((A1_radis *A1_radis + A1A2 * A1A2 - 2 * A1_radis * A1A2 * math.cos(ar))) 
        #计算C1A2C2的角度
        c1a2c2 = 180 * cosx(LG, c1a2, A2_radis) / math.pi    
        #计算C1A2A1的角度
        c1a2a1 = 180 * cosx(A1_radis, A1A2, c1a2) / math.pi
        pos_up = 180 - (c1a2c2 - c1a2a1)
        pos_down = 180 + (c1a2c2 + c1a2a1)        
    
    return pos_up, pos_down 

#把绝对坐标系的角度转为连杆系统角度
#A1_x, A1_y 是A1圆心坐标
#A2_x, A2_y 是A2圆心坐标
def angle2sysangle(A1_x, A1_y, A2_x, A2_y, a):
    x = A2_x - A1_x
    y = A2_y - A1_y
    if x == 0 and y == 0: return a
    elif x == 0 and y > 0: return (a - 90 + 360) % 360
    elif x == 0 and y < 0: return (a + 90) % 360
    temp = math.atan( y / x) * 180 / math.pi
    return (a - temp + 360) % 360  


#把连杆系统角度转为绝对坐标系的角度
#A1_x, A1_y 是A1圆心坐标
#A2_x, A2_y 是A2圆心坐标
def sysangle2angle(A1_x, A1_y, A2_x, A2_y, a):
    x = A2_x - A1_x
    y = A2_y - A1_y
    if x == 0 and y == 0: return a
    elif x == 0 and y > 0: return (a + 90) % 360
    elif x == 0 and y < 0: return (a - 90 + 360) % 360
    temp = math.atan( y / x) * 180 / math.pi    
    return (a + temp + 360) % 360  

#求解二次方程 Ax**2 + b * x + c = 0
def solve(a, b, c):
    delta = b**2 - 4*a*c 
    if delta < 0: 
        return None
    x1 = (b + delta**0.5) / (-2 * a)
    x2 = (b - delta**0.5) / (-2 * a)
    return [x1, x2]
    
#求解直线方程 y = kx + d 和 (x - a) **2 + ( y - b) ** 2 = c 
def twoSolve(k, d, a, b, c):
    d1 = k * a + d - b    
    a1 = 1 + k **2
    b1 = 2 * k * d1
    c1 = d1**2 - c**2
    ans =  solve(a1, b1, c1)
    if ans is None: return None
    ans[0] += a
    ans[1] += a   
    return [[ans[0], k * ans[0] + d], [ans[1], k * ans[1] + d]]    
    