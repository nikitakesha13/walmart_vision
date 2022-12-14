from fpdf import FPDF
import cv2
from PIL import Image
import numpy as np

class Report():
    def __init__(self, path, name, date, reba_avg, reba_max, arr): # arr = [(msg, frame_num)]
        # print(reba_avg)
        # print(reba_max)
        self.path = path
        self.name = name
        self.date = date
        self.reba_avg = reba_avg
        self.reba_max = reba_max
        self.arr = arr
        #self.cap = cv2.VideoCapture(self.path + "result.avi")
        self.pdf = FPDF()
        self.pdf.add_page()

    def title(self):
        self.pdf.set_font("helvetica", 'B', size = 20)
        self.pdf.cell(0, 10, txt="Form Analysis Report", new_x="LMARGIN", new_y="NEXT", align='C')
        self.pdf.set_font("helvetica", "", size = 10)
        self.pdf.cell(0, 5, txt="Name: " + self.name, new_x="LMARGIN", new_y="NEXT", align='C')
        self.pdf.cell(0, 5, txt="Date: " + self.date, new_x="LMARGIN", new_y="NEXT", align='C')
    
    def reba(self):
        self.pdf.set_xy(10, 40)
        self.pdf.set_font("helvetica", 'B', size = 12)
        self.pdf.cell(200, 7, txt="REBA Average Score: " + str(self.reba_avg[0]) + " (" + str(self.reba_avg[1]) + ")", new_x="LMARGIN", new_y="NEXT", align='L')
        self.pdf.cell(200, 7, txt="REBA Max Score: " + str(self.reba_max[0])+ " (" + str(self.reba_max[1]) + ")", new_x="LMARGIN", new_y="NEXT", align='L')

    def body(self):
        self.pdf.set_font("helvetica", 'B', size = 12)
        self.pdf.set_xy(10, 60)
        i = 1
        for el in self.arr :
            if self.pdf.will_page_break(57) == True:
                self.pdf.ln(50)
            self.pdf.cell(200, 7, txt=str(i) + ". " + str(el[0]), new_x="LMARGIN", new_y="NEXT", align='L')
            self.pdf.image(self.path + "Captures/Frame_" + str(el[1]) + ".jpg", x=60, h=50)
            self.pdf.ln(7)
            i += 1

    def generate_report(self):
        self.title()
        self.reba()
        self.body()
        self.pdf.output(self.path + "Report.pdf")

'''if __name__ == '__main__':
    msg = "Bad form"
    frame_num = 18
    arr = []
    for i in range(10):
        arr.append((msg, frame_num))
    report = Report('test-video-out/out_2022-11-16_20-17-12/', "Nikita Udodenko", "11/15/2022", (7, 'medium risk'), (10, 'high risk'), arr)
    report.generate_report()'''