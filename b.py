#encoding=utf-8
from xml.etree import ElementTree as ET
import time
import sys



#数据结构
#1、有每个帐号的初始值，初始值有时间
#2、每条记录有时间，类别，描述，帐号，帐号的变更
#3、类别的列表
#4、可以按时间显示每个帐号的余额和总额的余额
#5、有不列入总账的项目
#6、保存文件格式：
#feature list:
#1、可以展示一段时间内的流水信息
#2、可以计算单项和总额的和

print("This is banlance\n")

#每条账户的类
class Record:
    def __init__(self):
        self.date = ""
        self.type = ""
        self.desc = ""
        self.detail = {}
#Record

def input_wrap(str):
    if sys.version_info>(3,0):
        return input(str)
    else :
        return raw_input(str)
def wait():
    cmd = input_wrap("请输入命令:\n")
    return cmd
#wait

def open_cmd(cmdlist):
    global xmlfile,dictBanlanceList,dictTypeList,listRecs
    dictBanlanceList = {}
    dictTypeList = {}
    listRecs=[]
    #http://pycoders-weekly-chinese.readthedocs.org/en/latest/issue6/processing-xml-in-python-with-element-tree.html
    xmlfile = ET.parse(cmdlist[1])
    #banlancelist= xmlfile.findall("banlancelist")

    #print(banlancelist[0].tag)
    #print(banlancelist[0].attrib)
    #for elem in xmlfile.iter(tag='banlancelist'):
    #    print(elem.tag,elem.attrib)
    for elem in xmlfile.iterfind('banlancelist/item'):
        #print(elem.tag,elem.attrib)
        #print(elem.get("name"))
        dictBanlanceList[elem.get("id")] = elem.get("name")
        
    for elem in xmlfile.iterfind("typelist/type"):
        dictTypeList[elem.get("id")] = elem.get("name")
        
    for elem in xmlfile.iterfind("recordlist/rec"):
        rec = {}
        rec["date"]=elem.get("date")
        rec["type"]=elem.get("type")
        rec["desc"]=elem.get("desc")
        for de in elem.iterfind("./item"):
            
            #tdict[de.get("banlance")]=de.get("num")
            rec[de.get("banlance")]=de.get("num")
            '''
            if rec.date in rec.detail:
                rec.detail[rec.date].update(tdict)
            else:
                rec.detail[rec.date] = {}
            '''
        listRecs.append(rec)
    print(listRecs)
#open_cmd

def changelog(msg):
    log_et = ET.Element('log')
    log_et.set("time",time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
    log_et.set("msg",msg)
    changelog_et = xmlfile.find("changelog")
    changelog_et.append(log_et)

#changelog
    
def save_cmd(cmdlist):
    if len(cmdlist) == 2:
        xmlfile.write(cmdlist[1])
    else:
        xmlfile.write("bsrc.new")
    print("save")
#save_cmd

def add_cmd(cmdlist):
    print("add")
    if "rec" == cmdlist[1]:
        #add rec date type desc banlance,num  ..
        if dictTypeList.get(cmdlist[3]) is None:
            print("typeerr:"+cmdlist[3])
            return
        rec = ET.Element('rec')
        rec.set("date",cmdlist[2])
        rec.set("type",cmdlist[3])
        rec.set("desc",cmdlist[4])
        for i in range(5,len(cmdlist)):
            subban =cmdlist[i].split(",")
            
            item = ET.SubElement(rec, 'item')
            item.set("banlance",subban[0])
            item.set("num",subban[1])
        else:
            print("endfor")
        reclist_et = xmlfile.find("recordlist")
        reclist_et.append(rec)
        print(ET.dump(xmlfile))
        #reclist_et.append(rec)
        #print(ET.tostring(xmlfile))
    elif "banlance" == cmdlist[1]:
        banitem = ET.Element("item")
        banitem.set("name",cmdlist[2])
        banitem.set("id",cmdlist[3])
        banitem.set("desc",cmdlist[4])
        banitem.set("date",cmdlist[5])
        banitem.set("init",cmdlist[6])
        banlist_et = xmlfile.find("banlancelist")
        banlist_et.append(banitem)
        print(ET.dump(xmlfile))
    print("addend")
#add_cmd

def list_cmd(cmdlist):
    print(cmdlist[1])
    if "all" == cmdlist[1]:
        #全部展示
        #print("now has these banlances:")
        #print(dictBanlanceList)
        #print("detaillist :")
        bstr = ""
        outputd = []
        traw=[]
        traw.append("日期")
        traw.append("类型")
        traw.append("备注")
        for ban in dictBanlanceList:
            bstr += dictBanlanceList[ban]+"\t"
            traw.append(dictBanlanceList[ban])
        traw.append("总计")
        #表头
        outputd.append(traw.copy())
        traw.clear()
        #print("日期\t类型\t备注\t"+bstr+"总计")

        singleBanSum = {}
        initnumstr = ""
        traw.append("")
        traw.append("初始")
        traw.append("")
        for elem in xmlfile.iterfind('banlancelist/item'):
            singleBanSum[elem.get("id")] = float(elem.get("initnum"))
            initnumstr += elem.get("initnum")+"\t"
            traw.append(elem.get("initnum"))

        #初始值
        #print("\t初始\t\t"+initnumstr)
        outputd.append(traw.copy())
        traw.clear()
        
        for  rec in listRecs:
            tstr = rec["date"]+"\t"
            tstr += dictTypeList[rec["type"]]+"\t"
            tstr += rec["desc"]+"\t"
            traw.append(rec["date"])
            traw.append(dictTypeList[rec["type"]])
            traw.append(rec["desc"])
            tsum = 0
            for k in dictBanlanceList:
                if rec.get(k) is None:
                    tstr += "0\t"
                    traw.append("0")
                else :
                    tstr += rec[k]
                    tstr += "\t"
                    tsum += float(rec[k])
                    traw.append(rec[k])
                    singleBanSum[k] += float(rec[k])
            tstr += str(tsum)
            #print(tstr)
            traw.append(str(tsum))
        outputd.append(traw.copy())
        traw.clear()

        sumnumstr = "\t\t\t"
        traw.append("")
        traw.append("")
        traw.append("")
        for elem in xmlfile.iterfind('banlancelist/item'):
            if singleBanSum.get(elem.get("id")) is None:
                sumnumstr += "0\t"
                traw.append("0")
            else :
                sumnumstr += str(singleBanSum.get(elem.get("id")))+"\t"
                traw.append(str(singleBanSum.get(elem.get("id"))))
        #单项总计
        #print(sumnumstr)
        outputd.append(traw.copy())
        traw.clear()
        print_list(outputd)
    #print("list")
#list_cmd

def print_list(data):
    #print(data)
    for raw in data:
        for ceil in raw:
            #print(raw)
            print("{0:10}".format(ceil),end="|")
        print("",end="\n")
#print_list
        
def help_cmd(cmdlist):
    helpstr = '''
<all>
<banlancelist>   账户列表
<item name="" id="" initnum="" desc=""  date="" />
</banlancelist>
<typelist>
<type name="" id="">
</typelist>
流水记录
<recordlist>
单笔流水
<rec  date="" type="" desc="">包含所有的流水
    <item banlance="" num="" />
</rec>
</recordlist>
<changelog>
    <log msg="" time=""/>
</changelog>
</all>
命令列表
open filename
save [new]
close
add banlance name id  date initnum 
add rec date type desc banlance,num  ...
list all
list banlance
list sum
list file
'''
    print(helpstr)
#help_cmd

def main_process():
    while True:
        cmd = wait()
        cmdlist = cmd.split()
        if "close" == cmd :
            break
        elif "add" == cmdlist[0] :
            changelog(cmd)
            add_cmd(cmdlist)
        elif "save" == cmdlist[0] :
            changelog(cmd)
            save_cmd(cmdlist)
        elif "open" == cmdlist[0] :
            open_cmd(cmdlist)
        elif "list" == cmdlist[0] :
            list_cmd(cmdlist)
        elif "help" == cmdlist[0] :
            help_cmd(cmdlist)
        else:
            print(cmd);
            continue
#main_process

main_process()


