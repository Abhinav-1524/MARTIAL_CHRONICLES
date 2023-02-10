import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
import urllib
import requests
from api import API_KEY
import threading
import ezgmail




class App(QMainWindow):
    def __init__(self):
        super(App,self).__init__()
        uic.loadUi("design.ui",self)
        self.setWindowTitle("MARTIAN_CHRONICLES")
        self.show()


        #variable declaration
        self.num = 0
        self.image_list =[]


        #rove radio buttons
        self.oppurtunity = self.findChild(QRadioButton,'radioButton')
        self.spirit = self.findChild(QRadioButton,'radioButton_2')
        self.curiosity = self.findChild(QRadioButton,'radioButton_3')

        #camera radio buttons
        self.FHAZ = self.findChild(QRadioButton,'radioButton_6')
        self.RHAZ = self.findChild(QRadioButton,'radioButton_5')
        self.NAVCAM = self.findChild(QRadioButton,'radioButton_4')


        #frame
        self.frame = self.findChild(QFrame,'frame')
        
        

        #calender
        self.calendar = self.findChild(QCalendarWidget,'calendarWidget') 

        #stacked widget
        self.stackedWidget = self.findChild(QStackedWidget,'stackedWidget')
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)

        #assigning the stacking
        self.image_view = self.findChild(QPushButton,'pushButton')
        self.fetch_page_but = self.findChild(QPushButton,'pushButton_2')
     
        self.share = self.findChild(QPushButton,'pushButton_5')
        self.share.setIcon(QIcon('share_logo'))

        #frame resize
        self.down_frame=self.findChild(QFrame,'frame_3')
        QSizeGrip(self.down_frame)


        self.fetch_page_but.clicked.connect(self.goToPage1)
        self.image_view.clicked.connect(self.goToPage2)
        self.share.clicked.connect(self.goToPage3)
        
         #main function callings
        self.pushButton_8.clicked.connect(self.test)
        self.pushButton_8.clicked.connect(self.images)
        
        self.pushButton_8.clicked.connect(self.threading)

        #next and previous
        self.nxt_but = self.findChild(QPushButton,'pushButton_3')
        self.nxt_but.setIcon(QIcon('next.jpg'))
        self.prv_but = self.findChild(QPushButton,'pushButton_4')
        self.prv_but.setIcon(QIcon('previous.jpg'))

        self.nxt_but.clicked.connect(self.next)
        self.prv_but.clicked.connect(self.previous)

        #mailing part
        self.send=self.findChild(QPushButton,'pushButton_7')
        self.send_all=self.findChild(QPushButton,'pushButton_6')


        self.send.clicked.connect(self.mail_thread)
        self.send_all.clicked.connect(self.mail_all_thread)

        #mail descriptions
        self.to = self.findChild(QLineEdit,'lineEdit')
        self.subject=self.findChild(QLineEdit,'lineEdit_2')
        self.body=self.findChild(QLineEdit,'lineEdit_3')
        
        
        



    def Rover(self):    
        if (self.curiosity.isChecked()):
            return("curiosity")

        elif (self.oppurtunity.isChecked()):
            return("oppurtunity")

        elif (self.spirit.isChecked()):
            return("spirit")

    def camera(self):
        if (self.FHAZ.isChecked()):
            return("FHAZ")
        elif (self.RHAZ.isChecked()):
            return("RHAZ")
        elif (self.NAVCAM.isChecked()):
            return("NAVCAM")


    def dateSelected(self):
        selectedDate = self.calendar.selectedDate()
        pyDate = selectedDate.toPyDate()
        return (pyDate.strftime("%Y-%m-%d"))






    def goToPage1(self):
        self.stackedWidget.setCurrentIndex(0)

    def goToPage2(self):
        self.stackedWidget.setCurrentIndex(1)

    def goToPage3(self):
        self.stackedWidget.setCurrentIndex(2)

    
    

    def test(self):
        print(self.Rover())
        print(self.camera())
        print(self.dateSelected())
        

    def fetch(self):
        try:
            data = requests.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{self.Rover()}/photos?camera={self.camera()}&earth_date={self.dateSelected()}&api_key={API_KEY}")
            self.rover_data = data.json()
            print(len(self.rover_data['photos']))
            if len(self.rover_data['photos']) == 0:
                callinstance=Photo_error()
                callinstance.exec()

        except:
            callinstance=Api_error()
            callinstance.exec()

        try:
                for pic in self.rover_data['photos']:
                        self.num=self.num+1
                        urllib.request.urlretrieve(f"{pic['img_src']}",f"image{self.num}.jpg")
                        self.image_list.append(f"image{self.num}.jpg")
                    
        except:
            callinstance=Photo_error()
            callinstance.exec()
            
        
            
    
    def images(self):
        self.stackedWidget.setCurrentIndex(1)
        self.label = QLabel(self.frame)
        self.pixmap=QPixmap(f"image1.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()


#next and previous events
    def next(self):
        if len(self.image_list) == 1:
            self.num = 1

        elif self.num >= 0 and self.num < len(self.image_list):
            self.num = self.num+1

        elif self.num == len(self.image_list):
            self.num = 1
        
        print(len(self.image_list))
        print(self.num)
        self.pixmap=QPixmap(f"image{self.num}.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()
        
        

    def previous(self):
        if len(self.image_list) == 1 or len(self.image_list) == 0:
            self.num = 1
        
        elif self.num > 1 and self.num <= len(self.image_list):
            self.num -= 1

        elif self.num == 1 :
            self.num = len(self.image_list)

        print(len(self.image_list))
        print(self.num)
        self.pixmap=QPixmap(f"image{self.num}.jpg")
        self.pixmap =self.pixmap.scaled(self.frame.width(),self.frame.height())
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.frame.width(),self.frame.height())
        self.label.show()

        

       
#mailing events
    def mail(self):
        
        self.to_text = self.to.text()
        self.sub_text = self.subject.text()
        self.body_text = self.body.text()

        print(self.to_text,self.sub_text,self.body_text)
        ezgmail.send(self.to_text ,self.sub_text,self.body_text,attachments=f"image{self.num}.jpg")
        print("sent")

    
    def mail_all(self):

        self.to_text = self.to.text()
        self.sub_text = self.subject.text()
        self.body_text = self.body.text()


        print(self.to_text,self.sub_text,self.body_text)
        ezgmail.send(self.to_text ,self.sub_text,self.body_text,attachments=self.image_list,cc="")
        print("sent")

            
#threading events
    def threading(self):
        thread= threading.Thread(target=self.fetch)
        thread.start()

    def mail_thread(self):
        thread = threading.Thread(target=self.mail)
        thread.start()

    def mail_all_thread(self):
        thread=  threading.Thread(target=self.mail_all)
        thread.start()


#photo error class       
class Photo_error(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Photo_Error.ui",self)
        self.setWindowTitle("Photo Error")
        

        self.ok = self.findChild(QPushButton,'pushButton')
        self.ok.clicked.connect(lambda : self.close())



#api error class
class Api_error(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Api_error",self)
        self.setWindowTitle("API_ERROR")

        self.button = self.findChild(QPushButton,'pushButton')
        self.button.clicked.connect(lambda : self.close())

        

   

  



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())




