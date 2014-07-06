#encoding=utf-8
from xml.etree import ElementTree as ET



#数据结构
#1、有每个帐号的初始值，初始值有时间
#2、每条记录有时间，类别，描述，帐号，帐号的变更
#3、类别的列表
#4、可以按时间显示每个帐号的余额和总额的余额
#5、有不列入总账的项目
#6、保存文件格式：
'''
<all>
<banlancelist>   账户列表
<item name="" id="" />
</banlancelist>
<typelist>
<type name="" id="">
</typelist>
账户初始值
<banlanceinit>
<item id="" desc= />
</banlanceinit>
流水记录
<recordlist>
单笔流水
<rec date="" type="" desc="">包含所有的流水
    <item banlance="" num="" />
</rec>
</recordlist>
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
print("This is banlance\n")

#每条账户的类
class Record:
    def __init__(self):
        self.date = ""
        self.type = ""
        self.desc = ""
        self.detail = {}
#Record
        
def wait():
    cmd = input("请输入命令:\n")
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
        print("now has these banlances:")
        print(dictBanlanceList)
        print("detaillist :")
        for  rec in listRecs:
            tstr = ""
            for k in rec:
                tstr += rec[k]
                tstr += "\t"
            print(tstr)
    print("list")
#list_cmd

def main_process():
    while True:
        cmd = wait()
        cmdlist = cmd.split()
        if "close" == cmd :
            break
        elif "add" == cmdlist[0] :
            add_cmd(cmdlist)
        elif "save" == cmdlist[0] :
            save_cmd(cmdlist)
        elif "open" == cmdlist[0] :
            open_cmd(cmdlist)
        elif "list" == cmdlist[0] :
            list_cmd(cmdlist)
        else:
            print(cmd);
            continue
#main_process

main_process()


