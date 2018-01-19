# !/usr/bin/python
import wx
from DTR import computeDTR


def main():


    # def onButton(event):
    #     print "Button pressed."

    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py')
    frame.SetDimensions(0, 0, 200, 50)

    # Create open file dialog
    openFileDialog = wx.FileDialog(frame, "Open", "", "",
                                   "Text Files (*.txt)|*.txt",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    openFileDialog.ShowModal()
    # print(openFileDialog.GetPath())
    file = openFileDialog.GetPath()
    openFileDialog.Destroy()

    data = computeDTR(file)

    text = ""
    text += data["period"] + "\n"
    text += "-----------------------------------"
    # print "------------------------------"
    # print "*SUMMARY", data["summary"]
    for d in data["summary"]:
        # text += "\nName: " + d["emp"] + ", Total in Hours: " + str(d["sum_hrs"])
        for day in d['data']:

            if day["hrs"] == 8.0:
                new_sum = d["sum"] + 480
                d.update({"sum": new_sum})

            # text += "\nDate: " + day["date"] + ", Time: " + str(day["time_range"])+ ", in Minutes: " + str(day["total_mins"])+ ", in Hours: " + str(day["hrs"])
            text += "\nDate: " + day["date"] + ", Time: " + str(day["time_range"]) + ", in Hours: " + str(day["hrs"])

        subtotal_hrs = '{:02d}:{:02d}'.format(*divmod(int(d["sum"]), 60))

        text += "\nName: " + d["emp"].upper() + ", Total in Minutes: " + str(d["sum"]) + ", Total in Hours: " + str(
            subtotal_hrs)

        text += "\n--------------------------------------------"

    import subprocess
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print dir_path

    full_path = dir_path + '/outfile_print.txt'

    outfile = open(full_path, 'w')
    outfile.write(text)
    outfile.close()
    try:
        # subprocess.call(['notepad.exe', '/p', full_path])
        subprocess.call(['notepad.exe', full_path])
    except:
        subprocess.call(['gedit', full_path])


if __name__ == '__main__':
    main()