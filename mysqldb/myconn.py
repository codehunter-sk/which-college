def myconn():
    global mycon , ds
    import mysql.connector as ds
    import sys

    try:
        hostid='localhost'
        userid='root'
        mycon=ds.connect(host=hostid,
                         user=userid,
                         passwd='123')
        return mycon
    except:
        e=sys.exc_info()
        from tkinter import messagebox as msgbox
        msgbox.showinfo(title = 'Oooopppssss...' , message = 'Errorrrrrrrr!\nCan\'t connect to server!')
        exit(0)

def addspace(colval,num):
    if colval == None:
        colval = 'None'
    colval=str(colval)
    while len(colval) < num:
        colval +=' '
    return colval

if __name__=='__main__':
    myconn()
