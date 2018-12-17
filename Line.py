import requests,os,sys,csv
from bs4 import BeautifulSoup

def getNewChapterList(no,urr):
    print('in getNewChapterList')
    sig=True
    clst=[]
    i=1
    while sig:
        sad='&page='+str(i)
        print(urr+sad)
        (ll,sig)=getNewChapterListFromPage(no,(urr+sad))
        if len(ll)!=0 and ll[0]==False :
            return []
        clst+=ll
        i+=1
    print(clst)
    return list(reversed(clst))

def getNewChapterListFromPage(no,urr):
    print('in getNewChapterListFromPage')
    try:
        page = requests.get(urr,timeout=10)
        if(page.status_code!=200):
            return ([False],False)
        re=page.content
        soup=BeautifulSoup(re,'html.parser')
        tags=soup.find_all('ul',id="_listUl")[0].find_all('li')
        sig=True
        ll=[]
        for tag in tags:
            stra=tag.a.get('href')
            nnii=(tag.a.find_all('span',class_="tx")[0].string)
            ni=int(nnii.replace('#',''))
            if ni==no:
                ll.append(stra)
                sig=False
                break
            if ni<no:
                sig=False
                break
            ll.append(stra)
    except requests.exceptions.RequestException as e:
        ##print(e)
        return ([False],False)
    return (ll,sig)

def getChapter(urr,fldrnm):
    print('in getChapter')
    no=1
    nis=urr.split('/')[6]
    fldrn=fldrnm
    print(nis)
    fldrnm=fldrnm+'\\'+nis
    fldrnm='..\\' + fldrnm
    if not os.path.exists(fldrnm):
        os.makedirs(fldrnm)
    fldrnm=fldrnm+'\\'
    try:
        page=requests.get(urr,timeout=10)
        re=page.content
        if(page.status_code!=200):
            return False
    except requests.exceptions.RequestException as e:
        return False
    soup=BeautifulSoup(re,'html.parser')
    tags=soup.find_all('div',id="_imageList")[0].find_all('img',class_="_images")
    for tag in tags:
        try:
            imur=tag.get('data-url')
            print(imur)
            img=requests.get(imur,timeout=10,headers={'referer': urr})
            if(img.status_code!=200):
                return False
            nm=str(no)+'.jpg'
            no+=1
            with open((fldrnm+nm),'wb') as stream:
                for chunk in img.iter_content(100000):
                    stream.write(chunk)
        except requests.exceptions.RequestException as e:
            return False
    return True

def updateLog(isn,fldrnm):
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
    print('in run')
    iss=getNewChapterList(isn,url)
    con=True
    ##print(iss)
    for i in iss:
        con=getChapter(i,fldrn)
        if not con:
            break
        isn+=1
    updateLog(isn,fldrn)
