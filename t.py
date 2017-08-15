# -*- coding: utf8 -*-
import concurrent.futures
import urllib.request
import re
import json
import ast
 
 
visitedURL = {}     
         
maxpageID = [0]
pageDict = {}
 
def createPageID(url):
    pID = maxpageID.pop()+1
    maxpageID.append(pID)
    pID = 'page_'+str(pID)
    visitedURL[url] = pID
    return pID
 
 
maxpicID = [0]
picDict = {}
def createPicID(url):
    pID = maxpicID.pop()+1
    maxpicID.append(pID)
    pID = 'pic_'+str(pID)
    visitedURL[url] = pID
    return pID
 
 
 
stoppedQueue = []
waitingQueue = []
downloadingQueue = []
savedDict = dict()
 
#for page downloading
pageTpe = concurrent.futures.ThreadPoolExecutor(max_workers=8)
#for picture downloading
picTpe = concurrent.futures.ThreadPoolExecutor(max_workers=4)
 
 
def runMachine():
    #add at least 4 tasks to download
    while waitingQueue:
        if len(downloadingQueue)<4:
            picID = waitingQueue.pop(0)
            processload(picID)
 
def processload(picID):
    downloadingQueue.append(picID)
    #open conn,loading a picture
    picInfo = picDict[picID]
    url = picInfo['url']
    filename = url.split('/')[-1]
    conn = urllib.request.urlopen(url,timeout=10)
    picInfo['total'] = int(conn.info().get('Content-Length').strip())
    outputfile = open('pics/'+filename,'wb')
    picInfo['progress'] = 0
    updateStatus(picInfo)
    while True:
        chunk = conn.read(4096)
        picInfo['progress']+=len(chunk)
        updateStatus(picInfo)
        if not chunk:
            picInfo['state'] = 2
            downloadingQueue.remove(picID)
            savedDict[picID] = True
            updateStatus(picInfo)
            outputfile.close()
            conn.close()
            break
        outputfile.write(chunk)
        #reportProgress(url,progress,total)
    #report
 
def updateStatus(picInfo):
    url = picInfo['url']
    if picInfo['state']==2:
        print(url,'finished!')
    elif  picInfo['total'] and picInfo['progress']:
        print('{} progress: {:.2%}'.format(url,(picInfo['progress']/picInfo['total'])))
         
    pass
 
def log(*args):
    f = open('t.txt','ba')
    f.write((','.join(map(str,args))+'\n').encode('utf-8'))
    f.close()
 
def load_pic(url,pageID):
    if url in visitedURL:
        return
    picID = createPicID(url)
    #状态:0,未开始,1,排队待下,2,下载完毕
    picDict[picID] = {'url':url,'pageID':pageID,'total':0,'progress':0,'state':1}
    waitingQueue.append(picID)
     
 
def load_page(url):
    if url in visitedURL:
            return
    pID = createPageID(url)
    pageDict[pID] = {'url':url,'links':None}
    conn = urllib.request.urlopen(url)
    text = conn.readall().decode('GBK').encode('utf-8').decode('utf-8')
    conn.close()
    try:
            startIndex = text.index('<div class="mod newslist clear">')
            endIndex = text.index('<div class="mod curPosition clear">',startIndex)
            text = text[startIndex:endIndex]
            patt = re.compile('href="([^"]+?).htm"><img', re.DOTALL | re.IGNORECASE)
            jsurls = [x+'.hdBigPic.js' for x in patt.findall(text)]
            pageurllist = []
            for jsurl in jsurls:
                    if jsurl in visitedURL:
                            continue
                    jsID = createPageID(jsurl)
                    pageDict[jsID] = {'url':jsurl,'links':None}
                    jslinks = []
                    try:
                            conn = urllib.request.urlopen(jsurl)
                    except BaseException as e:
                            print('failed')
                            continue
                    try:
                        text = conn.readall().decode('GBK').encode('utf-8').decode('utf-8')
                        text = text[:text.index('/*  |xGv00|')]
                        obj = ast.literal_eval(text)
                        picnum = int(obj['Children'][0]['Children'][0]['Children'][0]['Content'])
                        picsobj = obj['Children'][0]['Children'][1]['Children']
                        for x in picsobj:
                            picurl = x['Children'][2]['Children'][0]['Content']
                            jslinks.append(picurl)
                        if jslinks:
                            pageDict[jsID]['links'] = jslinks
                            print(jsurl,'{} pics'.format(len(jslinks)))
                        try:
                            title = obj['Children'][0]['Children'][8]['Children'][0]['Content']
                        except:
                            title = 'unknown'
                        pageurllist.append(jsurl)
                        for picurl in jslinks:
                            load_pic(picurl,jsID)
                    except BaseException as e:
                            print(jsurl,'failed')
                            raise e
            pageDict[pID]['links'] = pageurllist
             
                     
    except ValueError as e:
            print('error',e)
            #can't find proper place
            pass
    runMachine()
     
urls = ['http://games.qq.com/l/photo/gmcos/yxcos.htm']
 
load_page(urls[0])
