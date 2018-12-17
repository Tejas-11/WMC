import requests,os,sys,csv
from bs4 import BeautifulSoup

def isNum(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def name_fun(var):##not for fun
    ##some stupid shit i have to do  due to a exception
    ##in the chapter naming format
    ##issue not completely solved as the url of the issue also does not have the chapter number in it.
    sslala=var.split('-')
    return [sslala[0].split(' ')[0],sslala[1].split(' ')[1]]

def getNewIssuesUrr(no,urr):
    print('in getnewissurl')
    try:
        page = requests.get(urr,timeout=10)
        if(page.status_code!=200):
            return []
        re=page.content
        soup = BeautifulSoup(re,'html.parser')
        tags=soup.find_all('tr')
        issues=[]
        isn=no
        ll=len(tags)
        ##we use i in range() instead of tag in tags because tags[0] is
        ##a title and does not have a link.So don't change this.
        for i in range(1,ll):
            ##some stupid shit i have to do  due to a exception
            ##in the chapter naming format
            ssla=name_fun(tags[i].td.a.string)
            if(isNum(ssla[0])):
                isn=int(ssla[0])
            elif(isNum(ssla[1])):
                isn=int(ssla[1])
            else:
                continue
            if(isn<no):
                isn+=1
                break
            nur="https://readms.net"+(tags[i].td.a.get('href'))[:-1]
            issues.append(nur)
        no=isn
    except requests.exceptions.RequestException as e:
        ##print(e)
        return []
    return (list(reversed(issues)),no);

def getIssue(urr,fldrnm):
    print('in getIssue')
    no=1
    temp=urr.split('/')
    fldrn=fldrnm
    isn=temp[len(temp)-3]
    nis='Ch'+str(isn)
    fldrnm=fldrnm+'\\'+nis
    fldrnm='..\\'+fldrnm
    if not os.path.exists(fldrnm):
        os.makedirs(fldrnm)
    fldrnm=fldrnm+'\\'
    while True:
        try:
            ##print ((urr+str(no)))
            page = requests.get((urr+str(no)),timeout=10)
            if(page.status_code!=200):
                updateLog(int(isn),fldrn)
                return False
            re=page.content
            soup = BeautifulSoup(re,'html.parser')
            tags=soup.find_all('img')[0].get('src')
            print (tags)
            nm=str(no)+'.png'
            print(nm)
            img = requests.get(("https:"+tags),timeout=15)
            if(img.status_code!=200):
                return False
            with open((fldrnm+nm),'wb') as stream:
                for chunk in img.iter_content(100000):
                    stream.write(chunk)
            tags=soup.find_all('li',class_="next disabled")
            if(len(tags)==1):
                break
            tagg=soup.find_all('li',class_="next")[0].a.get('href')
            temp=tagg.split('/')
            if(isn!=temp[len(temp)-3]):
                break
            no+=1
        except requests.exceptions.RequestException as e:
            return False
    return True

def updateLog(isn,fldrnm):
    print('in updateLog')
    fl=[]
    with open('aist.csv', newline='') as f:  
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            if(row[0]==fldrnm):
                row[2]=str(isn)
            fl.append(row)
    with open('aist.csv', 'w',newline='') as f:  
        writer = csv.writer(f,delimiter=',')
        for row in fl:
            writer.writerow(row)

def runn(fldrn,url,isn):
    print('runn')
    (iss,isn)=getNewIssuesUrr(isn,url)
    con=True
    for i in iss:
        con=getIssue(i,fldrn)
        if not con:
            break
        isn+=1
    updateLog(isn,fldrn)
