#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_yazlab import Ui_MainWindow #pyuic'le donusturulmus ui dosyası import edilir

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.count = 1 # Oyun Sayısı
        self.ksi = 0.1 # Ogrenme katsayisi
        self.finished = 0 # Oyun devam ediyor mu bitti mi 
        self.game = {8:self.pushButton_10,0:self.pushButton_2,1:self.pushButton_3,2:self.pushButton_4,3:self.pushButton_5,4:self.pushButton_6,5:self.pushButton_7,6:self.pushButton_8,7:self.pushButton_9}
        #Buttonlara indislerle erisebilmek için tanımlanmış sözlük
        self.resultSet = {"positive":200,"negative":-100} # Negative - Positive donusturmesi
        self.board = ["b" for i in range(9)] # Oyun tahtasıni belirten dizi
        self.w = [0.5 for i in range(9)]
    
        for i in self.game: # butun buttonlar aynı fonksyona atanır
            self.game[i].clicked.connect(self.buttonPressed)
    
        self.label_2.setText("%d.Oyun" %(self.count)) 
        self.pushButton.clicked.connect(self.clear)
        self.sfile = open("tic-tac-toe.data","a+")
        self.lines = self.sfile.readlines() # Dosyanin her satiri lines dizisinin bir elemanı
    
        for line in self.lines: # datasette her şey virgülle ayrılıyormus onu yanlıs hatırlayınca attığım string taklaları
            line = line.replace(",","")
            self.result = self.resultSet[line[line.__len__()-9:line.__len__()-1]]
            line = line[:line.__len__()-9]
            self.generate(line)
            self.lms() 
            #print ( "tahta = %s sonuc = %.2f V(b) = %.2f  \n" %(line,self.result,self.vb))
            #print ( "x1 = %.2f x2 = %.2f x3 = %.2f x4 = %.2f x5 = %.2f x6 = %.2f \n" %(self.x[1],self.x[2],self.x[3],self.x[4],self.x[5],self.x[6]))
            #print ( "w1 = %.2f w2 = %.2f w3 = %.2f w4 = %.2f w5 = %.2f w6 = %.2f \n" %(self.w[1],self.w[2],self.w[3],self.w[4],self.w[5],self.w[6]))

    def generate(self,s): # X'leri tespit eden fonksyon
        self.x = [0.0 for i in range(9)]
        directions = [s[:3],s[3:6],s[6:9],s[::3],s[1::3],s[2::3],s[::4],s[2:8:2]] # Tahtayı satır,sütün,diagonal hallere dönüştürüp diziye atadım
        for d in directions:
            cx = d.count("x")
            co = d.count("o")
            cb = d.count("b")
            if ("xxb" in d  or "bxx" in d):
                self.x[1]+=1
            if ("oob" in d or "boo" in d):
                self.x[2]+=1
            if (cx == 1 and cb == 2):
                self.x[3]+=1
            if (co == 1 and cb == 2):
                self.x[4]+=1
            if (cx == 3):
                self.x[5]+=1
            if (co == 3):
                self.x[6]+=1
            if ("xbx" in d):
                self.x[7]+=1
            if ("obo" in d):
                self.x[8]+=1
        

    def Vb(self): # Vb'yi hesaplayan fonksyon
        self.vb = self.w[0] + self.w[1] * self.x[1] +  self.w[2] * self.x[2] + self.w[3] * self.x[3] + self.w[4] * self.x[4] + self.w[5] * self.x[5] + self.w[6] * self.x[6] # + self.w[7] * self.x[7] + self.w[8] * self.x[8]
    
    def lms(self): # W'leri güncelleyen fonksyon
        self.Vb()
        self.w[1] = self.w[1] + self.ksi * (self.result - self.vb) * self.x[1]
        self.w[2] = self.w[2] + self.ksi * (self.result - self.vb) * self.x[2]
        self.w[3] = self.w[3] + self.ksi * (self.result - self.vb) * self.x[3]
        self.w[4] = self.w[4] + self.ksi * (self.result - self.vb) * self.x[4]
        self.w[5] = self.w[5] + self.ksi * (self.result - self.vb) * self.x[5]
        self.w[6] = self.w[6] + self.ksi * (self.result - self.vb) * self.x[6]
        #self.w[7] = self.w[7] + self.ksi * (self.result - self.vb) * self.x[7]
        #self.w[8] = self.w[8] + self.ksi * (self.result - self.vb) * self.x[8]

    def computer(self): #Bilgisayarın hamlelerini hesaplayan fonksyon
        max_vb = -200
        max_index = -1
        for i in range(18): 
            if (self.board[i%9] == "b"): # Tahtanın bos olan her elemani icin oraya hamle yapılsa vbler ne olur hesaplayan if kosulu
                would = [x for x in self.board] 
                self.result = -100 # oyunun kazanılmadığı her durumda Vtrain(b) - 100 dur diye dusundum
                if (i/9 < 1):
                    would[i%9] = "o"
                    self.generate("".join(would))
                    self.Vb()
                    self.vb*=-1
                else:
                    would[i%9] = "x"
                    self.generate("".join(would))
                    self.Vb()
                print ("Vb = %.2f max_vb = %.2f index = %d max_index = %d " %(self.vb,max_vb,i,max_index))
                print ( "x1 = %.2f x2 = %.2f x3 = %.2f x4 = %.2f x5 = %.2f x6 = %.2f x7 = %.2f x8 = %.2f \n" %(self.x[1],self.x[2],self.x[3],self.x[4],self.x[5],self.x[6],self.x[7],self.x[8]))
                # Bu printleri linux konsolunda dosyaya yazdırıp rapor oluşturmak için kullanıyorum
                if (self.vb > max_vb):
                    max_vb = self.vb
                    max_index = i % 9
        if (max_index != -1):
            self.board[max_index] = "x"
            self.game[max_index].setText("X")
            self.check()
            t = "".join(self.board)
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))

    def check(self): # Oyun bitti mi kim kazandı belirleyen fonksyon
        self.generate("".join(self.board))
        t = "".join(self.board)
        if (self.x[5] > 0):
            self.finished = 1
            self.label.setText("Oyunu X kazandi")
            self.result = 200
            print("%d.Oyunu X kazandi" %(self.count))
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))
        if (self.x[6] > 0):
            self.finished = 2
            self.label.setText("Oyunu O kazandi")
            self.result = -100
            print("%d.Oyunu O kazandi" %(self.count))
            print ("%s\n%s\n%s" %(t[:3],t[3:6],t[6:9]))


    def buttonPressed(self): # Hamle yapmak için bir yere tıklandığında 
        button = self.sender() # Hangi buttondan tıklandıysa o nesneyi button değişkenine atar
        temp = [key for key,value in self.game.iteritems() if value.objectName() == button.objectName()][0]
        # Nesne isminden dizi indisine ulasilir
        if (self.board[temp] == "b" and self.finished == 0): # O nokta bos ve oyun bitmemis iken
            self.board[temp] = "o"
            button.setText("O") # Kullanıcı hamlesini yapar
            self.check() 
            if (self.finished == 0):
                self.computer() # Oyun bitmemisse bilgisayar hamlesini yapar

    def clear(self): # Tahtayı sıfırlayıp yeni oyun baslatır w'lerle ellesmediği için program öğrenip sonraki oyunlarda daha düzgün hamleler yapabiliyor.
        self.count+=1
        self.finished = 0
        self.label.setText("") 
        temp = [key for key,value in self.resultSet.iteritems() if value == self.result][0]
        endgame = ",".join(self.board)+","+temp+"\n"
        #if (endgame not in self.lines):
        #    self.sfile.write(endgame)        
        print("-----------------------------\n")
        self.label_2.setText("%d.Oyun" %(self.count))
        self.board = ["b" for x in range(9)]
        for i in self.game:
            self.game[i].setText("")

app = QtGui.QApplication(sys.argv)
run = MainWindow()
run.show()
sys.exit(app.exec_())

