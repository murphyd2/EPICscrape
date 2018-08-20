def comment_period():
    import datetime
    frmtstrg = '%m/%d/%Y'
    inputstr= input("write today's date (mm/dd/yyyy):")
    startdate = datetime.datetime.strptime(inputstr, frmtstrg)
    enddate = startdate + datetime.timedelta(30)
    return startdate, enddate
def main():
    today, end= comment_period()
    print("Date given: {} 30 days later: {}".format(today, end))
main()