import socket,time,Line,csv
import MangaStream as Ms

def checkConn():
    host="8.8.8.8"
    port=53
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False

def callAll():
    fl=[]
    with open('aist.csv', newline='') as f:  
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            fl.append(row)
    for row in fl:
        if(row[3]=='manga') and checkConn():
            Ms.runn(row[0],row[1],int(row[2]))
        if(row[3]=='webtoon') and checkConn():
            Line.runn(row[0],row[1],int(row[2]))

def main():
    while not checkConn():
        print('waiting for network')
        time.sleep(300)
    while True:
        print('checking online')
        callAll()
        time.sleep(600)

main()
