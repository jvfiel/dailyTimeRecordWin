def readDTR(path):

    inputfile = open(path)
    # outputfile = open('test.csv', 'w')

    # sample text string, just for demonstration to let you know how the data looks like
    # my_text = '"2012-06-23 03:09:13.23",4323584,-1.911224,-0.4657288,-0.1166382,-0.24823,0.256485,"NAN",-0.3489428,-0.130449,-0.2440527,-0.2942413,0.04944348,0.4337797,-1.105218,-1.201882,-0.5962594,-0.586636'

    # dictionary definition 0-, 1- etc. are there to parse the date block delimited with dashes, and make sure the negative numbers are not effected
    reps = {'"NAN"':'NAN', '"':'', '0-':'0,','1-':'1,','2-':'2,','3-':'3,','4-':'4,','5-':'5,','6-':'6,','7-':'7,','8-':'8,','9-':'9,', ' ':',', ':':',' }

    # for i in range(4): inputfile.next() # skip first four lines

    dtr_dict_list = []


    for i,line in enumerate(inputfile):
        if i == 0:
            continue
        x = line.split()
        dtr_dict_list.append({"emp_id":x[2],"emp":x[3],"date":x[6],"time":x[7]})
        # print "0: ", x[0]
        # print "1: ", x[1]
        # print "2: ", x[2]
        # print "3: ", x[3] #NAME
        # print "4: ", x[4]
        # print "5: ", x[5] #DATE
        # print "6: ", x[6]
        # print "7: ", x[7] #TIME

        # print line[0]
        # outputfile.writelines(data_parser(line, reps))


    # print dtr_dict_list

    inputfile.close()
    # outputfile.close()
    return dtr_dict_list

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def get_minutes(date_time_older, date_time_newer):
  date_time_difference = round((date_time_newer-date_time_older).total_seconds()/60)
  return date_time_difference

def computeDTR(file):
    summary = []

    period1 = ""
    period2 = ""

    master = readDTR(file)

    for i,data in enumerate(master):

        if i == 0:
            period1 = data["date"]

        if i == len(master)-1:
            period2 = data["date"]


        # print i
        summary_new = []
        data_dict = {
            "emp":"",
            "data":[
                # {"emp_id": "", "emp": "", "date": "", "time": ""}
            ],
            "sum":0.0,
            "sum_hrs":0.0
        }
        # print data
        # time_log = {"emp_id": "", "emp": "", "date": "", "time": "","hrs":0.0,"total_mins":""}

        if summary == []: #first
            data_dict.update({"emp": data["emp"]})
            # print data_dict
            # print summary, data["emp"]
            summary.append(data_dict)
            # print summary
        else:
            for d in summary:

                found = 0

                # print d
                # print "check emp: ",d['emp'], data["emp"]
                if d['emp'] == data["emp"]:

                    subtotal = d['sum']

                    # print "found emp"
                    d.update({"emp": data["emp"]})
                    found = 1

                    found_date = 0

                    # time_log.update({"date": data["date"], "time": data["time"]})
                    # time_log.update({"date": data["date"]})

                    for log in d['data']:
                        if log["date"] == data["date"]:
                            found_date = 1
                            # log.update({"time":"found"})

                            from datetime import datetime
                            s1 = log["time"]
                            s2 = data["time"]  # for example
                            FMT = '%H:%M:%S'
                            tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                            # log.update({"time_range": s1+' - '+s2})
                            # if tdelta:

                            tdiff = get_minutes(datetime.strptime(s2, FMT), datetime.strptime(s1, FMT))
                            if tdiff < 0:
                                tdiff = abs(tdiff)

                            update_log_dict = {"hrs": (str(days_hours_minutes(tdelta)[1]) +":"+ str(days_hours_minutes(tdelta)[2]).zfill(2)),
                                        "total_mins:":str(tdiff),"time_range": s1+' - '+s2}
                            # print "=====UPDATE LOG DICT====="
                            # print update_log_dict
                            # print "time dff",tdiff
                            # print "=====UPDATE LOG DICT====="
                            update_log = log.copy()
                            update_log.update(update_log_dict)
                            log.update(update_log)

                            # log.update({"total_mins:":tdiff})

                            subtotal+= tdiff

                            # else:
                            #     log.update({"hrs": '8'})

                            break
                            # break

                    if not found_date:
                        time_logs = list(d["data"])
                        # time_logs.append({"date":data["date"],"hrs":8.0,"time_range":data["time"],"total_mins":480,"time": data["time"]})
                        time_logs.append({"date":data["date"],"hrs":8.0,"time_range":data["time"],"total_mins":0.0,"time": data["time"]})
                        d.update({"data":time_logs})
                        # subtotal+=480

                    # subtotal_hrs = subtotal/60
                    subtotal_hrs = '{:02d}:{:02d}'.format(*divmod(int(subtotal), 60))
                    d.update({"sum":subtotal,"sum_hrs":subtotal_hrs})

                    # print "Grant Total Minutes:",subtotal
                    # print "Grant Total Hrs:", subtotal_hrs

                    break
                else:
                    found = 0

            if found:
                pass
            else:
                summary_new = list(summary)
                # print "not found emp.. will add emp"
                data_dict.update({"emp": data["emp"]})
                # print data_dict
                # print summary, data["emp"]
                summary_new.append(data_dict)

        if summary_new:
            summary = list(summary_new)
            # print "added new emp"
            # print summary
        # print summary

    return {"summary":summary,"period":period1+" - "+period2}
