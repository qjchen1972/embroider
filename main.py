from gui.my_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
import sys
import numpy as np
import src.cam as cam
import src.slider as slider
import threading

class MyMainWindow(QMainWindow, Ui_MainWindow):

    updated = QtCore.pyqtSignal(str)
    appended = QtCore.pyqtSignal(str)
    seted = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)       
        self.setWindowTitle('绣花机计算') 
        
        self.cam = cam.Cam()
        self.slider = slider.Slider()
        self.init_Cam()
        self.init_Slider()
        self.init_Para()
        
        
        self.tabWidget.currentChanged.connect(self.tabhchange)
        
        self.close_Button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.close_Button_2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.close_Button_3.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.tabWidget.setTabText(0, "凸轮计算")
        self.tabWidget.setTabText(1, "滑轮计算")
        self.tabWidget.setTabText(2, "找到最佳参数")
        
        self.createtl_Button.clicked.connect(self.createTl)
        self.createtl_Button_2.clicked.connect(self.createSl)
        self.caldst_Button_2.clicked.connect(self.calDst)
        self.find_Button_3.clicked.connect(self.findBest)
        self.updated.connect(self._updatemsg)
        self.appended.connect(self._appendmsg)
        self.seted.connect(self._setmsg)
        
    def tabhchange(self):
        idx = self.tabWidget.currentIndex()
        #print(idx)
        #if idx == 0: self.init_Cam()
            
        
    def init_Cam(self):
        #初始化值
        obj = self.cam
        self.A1_x_lineEdit.setText(str(obj.A1_x))
        self.A1_y_lineEdit.setText(str(obj.A1_y))
        self.A1_radis_l_lineEdit.setText(str(obj.A1_radis_l))
        self.A1_radis_r_lineEdit.setText(str(obj.A1_radis_r))
        self.A1_r_l_a_lineEdit.setText(str(obj.A1_r_l_a))
        
        self.A2_x_lineEdit.setText(str(obj.A2_x))
        self.A2_y_lineEdit.setText(str(obj.A2_y))
        self.A2_radis_l_lineEdit.setText(str(obj.A2_radis_l))
        self.A2_r_l_a_lineEdit.setText(str(obj.A2_r_l_a))
        self.maxHigh_lineEdit.setText(str(obj.maxHigh))        
        
        self.input_tlpath_lineEdit.setText('input.txt')
        self.output_tlpath_lineEdit.setText('output.dat')
    
        
    def init_Slider(self):
        obj = self.slider
        self.A1_x_lineEdit_2.setText(str(obj.A1_x))
        self.A1_y_lineEdit_2.setText(str(obj.A1_y))
        self.A1_radis_lineEdit_2.setText(str(obj.A1_radis)) 
        
        self.A2_x_lineEdit_2.setText(str(obj.A2_x))
        self.A2_y_lineEdit_2.setText(str(obj.A2_y))        
        self.A2_radis_lineEdit_2.setText(str(obj.A2_radis)) 
        self.A2_radis_r_lineEdit_2.setText(str(obj.A2_radis_r))
        self.A2_radis_l_lineEdit_2.setText(str(obj.A2_radis_l))
        self.A1A2_lg_lineEdit_2.setText(str(obj.A1A2_lg))
        self.yb_lineEdit_2.setText(str(obj.yb))
        self.A3_radis_lineEdit_2.setText(str(obj.A3_radis))
        self.output_tlpath_lineEdit_2.setText('output_info.txt')
        
    def init_Para(self):
        #初始化值        
        self.A2_radis_lineEdit_start.setText("23")
        self.A2_radis_lineEdit_end.setText("24")
        self.A2_radis_lineEdit_zone.setText("0.1")
        
        self.A2_radis_l_lineEdit_start.setText("33")
        self.A2_radis_l_lineEdit_end.setText("34")
        self.A2_radis_l_lineEdit_zone.setText("0.1")
        
        self.A1A2_lg_lineEdit_start.setText("51")
        self.A1A2_lg_lineEdit_end.setText("52")
        self.A1A2_lg_lineEdit_zone.setText("0.1")
        
        self.mindst = 2.45
        self.mindst_lineEdit_3.setText(str(self.mindst))
        self.totaldstloss = 0.2
        self.totaldst_lineEdit_3.setText(str(self.totaldstloss))
        self.shownum = 100
        self.shownum_lineEdit_3.setText(str(self.shownum))
        
        
    def _input_Cam(self):
        obj = self.cam
        obj.A1_x = float(self.A1_x_lineEdit.text())  
        obj.A1_y = float(self.A1_y_lineEdit.text())  
        obj.A1_radis_l = float(self.A1_radis_l_lineEdit.text())  
        obj.A1_radis_r = float(self.A1_radis_r_lineEdit.text())  
        obj.A1_r_l_a = float(self.A1_r_l_a_lineEdit.text())  
        
        obj.A2_x = float(self.A2_x_lineEdit.text())  
        obj.A2_y = float(self.A2_y_lineEdit.text())  
        obj.A2_radis_l = float(self.A2_radis_l_lineEdit.text())  
        obj.A2_r_l_a = float(self.A2_r_l_a_lineEdit.text())  
        obj.maxHigh = float(self.maxHigh_lineEdit.text())        
        
        self.input_path = self.input_tlpath_lineEdit.text()
        self.cam_output_path = self.output_tlpath_lineEdit.text()    
    
    def createTl(self):
        self._input_Cam()
        mode = 0
        if self.zone_mode.isChecked():
            mode = 1
        try:
            cam.createCadFile(self.cam, 
                              self.input_path, 
                              self.cam_output_path, 
                              mode=mode)
            self.Msg_textEdit.append('create %s OK!' %(self.cam_output_path))
        except Exception as e:
            print(e)
            self.Msg_textEdit.append('create %s Fail!' %(self.cam_output_path))          
        #print(input_path, output_path)
        #print(obj.A1_x, obj.A1_y, obj.A1_radis_l, obj.A1_radis_r, obj.A1_r_l_a)
        #print(obj.A2_x, obj.A2_y, obj.A2_radis_r, obj.A2_r_l_a, obj.maxHigh)
    
    def _input_Slider(self):
        obj = self.slider
        obj.A1_x = float(self.A1_x_lineEdit_2.text())  
        obj.A1_y = float(self.A1_y_lineEdit_2.text())
        obj.A1_radis = float(self.A1_radis_lineEdit_2.text())
        
        obj.A2_x = float(self.A2_x_lineEdit_2.text())  
        obj.A2_y = float(self.A2_y_lineEdit_2.text())
        obj.A2_radis = float(self.A2_radis_lineEdit_2.text())
        obj.A2_radis_r = float(self.A2_radis_r_lineEdit_2.text())
        obj.A2_radis_l = float(self.A2_radis_l_lineEdit_2.text())
        obj.A1A2_lg = float(self.A1A2_lg_lineEdit_2.text())
        obj.yb = float(self.yb_lineEdit_2.text())
        obj.A3_radis = float(self.A3_radis_lineEdit_2.text())
        self.slider_output_path = self.output_tlpath_lineEdit_2.text()
        
    def calDst(self):
        self._input_Slider()
        mind, totald = slider.calDst(self.slider)
        self.Msg_textEdit_2.setText(
             '最小距离(23度)是 %.3f 总的距离是 %.3f' %(mind, totald))        

    def createSl(self):
        self._input_Slider()
        self._input_Cam()    
        mode = 0
        if self.zone_mode.isChecked():
            mode = 1        
        try:        
            ans = cam.createRadis(self.cam, self.input_path, mode=mode)
            temp, mindst, totaldst = slider.createDst(self.slider, ans[:, 0])
            ans = np.concatenate((ans, temp[:, None]), axis=1)
            print(ans)
            with open(self.slider_output_path, 'w') as f:
                f.write('最低点转23度滑块移动距离: %.3f\n' %(mindst))
                f.write('\n滑块总的移动距离: %.3f\n' %(totaldst))            
                f.write('\n度数     极坐标     滑块移动距离\n')
                for one in ans:                   
                   f.write(
                   '  %d          %.3f       %.3f\n' %(one[0], one[2], one[3]))
                   
            self.Msg_textEdit_2.append(
            'create %s OK!' %(self.slider_output_path))
        except Exception as e:
            print(e)
            self.Msg_textEdit_2.append(
            'create %s Fail!' %(self.slider_output_path))        
    
    def _input_Para(self):
        self.A2_radis_l_start = float(self.A2_radis_l_lineEdit_start.text())
        self.A2_radis_l_end = float(self.A2_radis_l_lineEdit_end.text())
        self.A2_radis_l_zone = float(self.A2_radis_l_lineEdit_zone.text())
        
        self.A2_radis_start = float(self.A2_radis_lineEdit_start.text())
        self.A2_radis_end = float(self.A2_radis_lineEdit_end.text())
        self.A2_radis_zone = float(self.A2_radis_lineEdit_zone.text())
        
        self.A1A2_lg_start = float(self.A1A2_lg_lineEdit_start.text())
        self.A1A2_lg_end = float(self.A1A2_lg_lineEdit_end.text())
        self.A1A2_lg_zone = float(self.A1A2_lg_lineEdit_zone.text())        
        self.mindst = float(self.mindst_lineEdit_3.text())
        self.totaldstloss = float(self.totaldst_lineEdit_3.text())
        self.shownum = float(self.shownum_lineEdit_3.text())
    
    def _updatemsg(self, msg):
        self.Msg_textEdit_3.setText(msg)
    
    def _appendmsg(self, msg):
        self.Msg_textEdit_4.append(msg) 
        
    def _setmsg(self, msg):
        self.Msg_textEdit_4.setText(msg) 
        
    def _findProc(self, obj, update, append, seted):    
        obj.procInput()
        ma, mi, ans = obj.findanglelimit()
        mindst = obj.getdistance(mi[0], mi[0]+23)
        totaldst = obj.getdistance(mi[0], ma[0])
        str = '初始状态: 总距离: %.3f, 最小距离: %.3f' %(mindst, totaldst)
        append.emit(str)
        
        AList = np.arange(self.A2_radis_start, self.A2_radis_end, self.A2_radis_zone)
        if AList.size == 0:
           np.append(AList,self.A2_radis_start)
           
        BList = np.arange(self.A2_radis_l_start, 
                          self.A2_radis_l_end, self.A2_radis_l_zone)
        if BList.size == 0:
           np.append(BList,self.A2_radis_l_start)
        
        CList = np.arange(self.A1A2_lg_start, 
                          self.A1A2_lg_end, self.A1A2_lg_zone)
        if CList.size == 0:
           np.append(CList,self.A1A2_lg_start)
    
        ansList = []
        for A in AList:
            for B in BList:
                if A + B <= obj.A2_radis_r : continue
                if A + obj.A2_radis_r <= B: continue
                if B + obj.A2_radis_r <= A: continue    
                for C in CList:                    
                    obj.A2_radis = A    
                    obj.A2_radis_l = B
                    obj.A1A2_lg = C
                    
                    ma, mi, _ = obj.findanglelimit()
                    v = obj.getdistance(mi[0], ma[0])               
                    mindst = obj.getdistance(mi[0], mi[0]+23)
                    str = '%.3f  %.3f   %.3f => 总距离: %.3f, 最小距离: %.3f' \
                          %(A, B, C, v, mindst)
                    update.emit(str)                    
                    if abs(v - totaldst) > self.totaldstloss: 
                        continue                    
                    append.emit(str)
                    ansList.append([A, B, C, v, mindst, abs(mindst - self.mindst)])
                           
        seted.emit('\n最好的%d个参数:\n' %self.shownum)
        ansList = np.array(ansList)
        idx = ansList[:, 5].argsort()
        ansList = ansList[idx]
        for ix, one  in enumerate(ansList):
            if ix == self.shownum : break
            str = '%.3f  %.3f   %.3f => 总距离: %.3f, 最小距离: %.3f' \
                          %(one[0], one[1], one[2], one[3], one[4])
            append.emit(str)        
    
    
    def findBest(self):
        self._input_Slider()
        self.slider.procInput()
        self._input_Para()
        obj = self.slider
        thread = threading.Thread(target=self._findProc, 
                         args=(obj, self.updated, self.appended, self.seted))
        
        thread.start()      
        
if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())    
        