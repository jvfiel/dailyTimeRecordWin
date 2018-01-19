from Tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkFileDialog
from DTR import computeDTR

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Cyberbee DTR")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):

        ftypes = [('Text Files', '.txt')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            # text = self.readFile(fl)
            # self.txt.insert(END, text)

            # computeDTR()
            data = computeDTR(fl)
            text = ""
            self.txt.delete(1.0,END)
            self.txt.insert(END, data["period"])
            print "------------------------------"
            print "*SUMMARY", data["summary"]
            for d in data["summary"]:
               # text += "\nName: " + d["emp"] + ", Total in Hours: " + str(d["sum_hrs"])
               for day in d['data']:

                    if day["hrs"] == 8.0:
                        new_sum = d["sum"] + 480
                        d.update({"sum":new_sum})

                    # text += "\nDate: " + day["date"] + ", Time: " + str(day["time_range"])+ ", in Minutes: " + str(day["total_mins"])+ ", in Hours: " + str(day["hrs"])
                    text += "\nDate: " + day["date"] + ", Time: " + str(day["time_range"])+ ", in Hours: " + str(day["hrs"])

               subtotal_hrs = '{:02d}:{:02d}'.format(*divmod(int(d["sum"]), 60))

               text += "\nName: " + d["emp"] + ", Total in Minutes: " + str(d["sum"]) + ", Total in Hours: " + str(subtotal_hrs)

               text += "\n--------------------------------------------"
            import subprocess

            import os
            dir_path = os.path.dirname(os.path.realpath(__file__))
            print dir_path

            full_path = dir_path+'/outfile_print.txt'

            outfile = open(full_path, 'w')
            outfile.write(text)
            outfile.close()
            try:
                # subprocess.call(['notepad.exe', '/p', full_path])
                subprocess.call(['notepad.exe', full_path])
            except:
                subprocess.call(['gedit', full_path])

            self.txt.insert(END, text)

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text


def main():

    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()