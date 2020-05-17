from django.shortcuts import render
from front import models
from django.shortcuts import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import xlrd
from utils import restful
import datetime,time

def index(request):
    return render(request, "index.html")

#啦啦啦啦啦啦啦，我添加了一行注释

@csrf_exempt
def upload_file(request):
    uploadFileObj = request.FILES['myFile']
    uploadFileName = "dataResource/" + uploadFileObj.name
    MScode = request.POST.get("types")
    print("MScode: "+MScode)
    print(uploadFileName)
    with open(uploadFileName ,'wb') as saveFile:
        for chunk in uploadFileObj.chunks():
            saveFile.write(chunk)
    f = open(uploadFileName, encoding='utf-8')
    data_json = json.load(f)
    code = 0
    sequenceNum =[]
    data = xlrd.open_workbook('shandongdata.xlsx', encoding_override='utf-8')  # 读取表
    for dataj in data_json:
        DisasterType,sqNumber = TransData(dataj["Code"])  # 解码ID，返回后七位的灾情信息码中的大类代码和子类代码
        code = DisasterType
        sequenceNum.append(sqNumber)
        dataj["ReportingUnit"] = MScode+ "-" + dataj["ReportingUnit"]  # 将编码MSCode加在reportingunit字段中
        disInfo = dataj["Code"]  # 获取19位编码
        dataj["Location"] = TransDataAddress(data,disInfo[0:12]) # 获取19位ID的前十二位编码，即基础地理信息码  # 获取19位ID的前十二位编码，即基础地理信息码
        print("DisasterType:"+DisasterType)
        print("data:"+str(dataj))
    databaseOperation(code, data_json,sequenceNum)
    print('ok')
    return restful.result(message="upload success", data={"MScode": MScode, "uploadFileName": uploadFileObj.name})



# 解析19位灾情信息编码
def TransData(IDNUmber):
    if(CheckIDNumber(IDNUmber)):
        disInfo=IDNUmber[-7:] #获取灾情信息编码，从倒数第七个字符到结尾
        sequenceNumber = disInfo[-4:]
        fdisInfo=disInfo[0] #获取大类代码
        sdisInfo=disInfo[1:3] #获取子类代码
        print('灾情信息编码：'+disInfo+' 大类代码：'+fdisInfo+' 子类代码：'+sdisInfo)
        if(fdisInfo=='1'and sdisInfo=='11'):
            dbTableNmae="DeathStatistics"  # 人员失踪及死亡：死亡
            dbTableType=fdisInfo+sdisInfo
        elif(fdisInfo=='2'and sdisInfo=='21'):
            dbTableNmae="CivilStructure"  # 房屋破坏：土木
            dbTableType = fdisInfo + sdisInfo
        elif(fdisInfo=='3'and sdisInfo=='36'):
            dbTableNmae="CommDisaster"  # 生命线工程灾情：通信
            dbTableType = fdisInfo + sdisInfo
        elif(fdisInfo=='4'and sdisInfo=='41'):
            dbTableNmae="CollapseRecord"    # 次生灾害：崩塌
            dbTableType = fdisInfo + sdisInfo
        elif(fdisInfo=='5'and sdisInfo=='52'):
            dbTableNmae="DisasterPrediction"  # 震情：灾情预测
            dbTableType = fdisInfo + sdisInfo
        else:
            dbTableNmae="000"
            dbTableType=fdisInfo+sdisInfo
        print(dbTableNmae+dbTableType)
        return dbTableType,sequenceNumber# 返回灾情信息编码的大类代码+子类代码


# 解析19位ID编码的前12位，得到具体的地理位置信息
def TransDataAddress(data,address_code):
    table = data.sheets()[0]  # 选定表
    nrows = table.nrows  # 获取行号
    # print('共有'+str(nrows)+'行数据')
    address_info = '地址'
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        if (alldata[9] == address_code):
            # print(alldata[9])
            result = alldata[10] + alldata[11] + alldata[12] + alldata[13] + alldata[14]
            # print('查到的地址为：'+result)
            address_info = result
            # print('address_info:'+address_info)
            break
        else:
            address_info = '未找到'

    return address_info


@csrf_exempt
def test_url(request):
    print("test_url")
    result = request.POST.get("data1")
    return HttpResponse(result)


#数据表操作和文件的存储
def databaseOperation(code, datas,sequenceNumber):
    # 找到解析的336编码，不同编码不同目录
    if (code == '336'):
        fileName = '336/CommDisaster.json'
    if (code == '111'):
        fileName = '111/DeathStatistics.json'
    if (code == '221'):
        fileName = '221/CivilStructure.json'
    if (code == '441'):
        fileName = '441/CollapseRecord.json'
    if (code == '552'):
        fileName = '552/DisasterPrediction.json'

    # 为了方便操作，每次运行，，我都先清空数据表了
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    table_name = "front_commdisaster"
    sql = "Delete From {0}".format(table_name)
    cur.execute(sql)
    cur.execute("UPDATE sqlite_sequence set seq=0 where name='MSHD_commdisaster';")
    conn.commit()
    # 将数据存入数据库
    i=0
    for data in datas:
        models.CommDisaster.objects.create(Code=data["Code"], Date=data["Date"], Location=data["Location"],
                                           Type=data["Type"], Grade=data["Grade"], Picture=data["Picture"],
                                           Note=data["Note"], ReportingUnit=data["ReportingUnit"],
                                           SequenceNumber=sequenceNumber[i])
        i=i+1
    # 将字典封装成json文件
    json_file = json.dumps(datas)
    # 保存json文件
    with open(fileName, 'w') as file_obj:
        json.dump(json_file, file_obj)
    return datas


# 测试数据是否是json格式，如果是json格式则抛出异常
def test_is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


# 测试数据源的ID是否为19位编码
def test_source_data_ID_number(ID_number):
    if(len(ID_number)==19):
        return True
    else:
        return False


# 检查ID是否为19位编码
def CheckIDNumber(IDNumber):
    if(len(IDNumber)==19):
        return True
    else:
        return False


#将json文件传到前段html文件中
def data(request):
    list=request.path_info.split('/')
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    sql = "select * from front_commdisaster"  # MSHD_commdisaster为表名
    cur.execute(sql)
    datas = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    return render(request, 'data.html', {'items': datas,'type': list[2]})


# 用户访问 /request 网页并传入 code disasterType  o_URL requestunit
# ex: http://localhost:8000/request/?code=3700000000003366789&disasterType=336&o_url=168.336.222&requestUnit=水星水星
def data_request(request):
    # 获取问号后传递的参数
    code = request.GET.get("code")
    disaster_type = request.GET.get("disasterType")
    o_url = request.GET.get("o_url")
    request_unit = request.GET.get("requestUnit")
    # 获取当前时间，以年-月-日-时-分格式显示
    now_time = datetime.datetime.now()
    str_time = now_time.strftime("%Y-%m-%d %X")
    tup_time = time.strptime(str_time, "%Y-%m-%d %X")
    time_str = str(tup_time.tm_year) + "-" + str(tup_time.tm_mon) +"-"+str(tup_time.tm_mday)+" "+ str(tup_time.tm_hour) + ":" +str(tup_time.tm_min)
    # 将记录写入数据库
    models.requestList.objects.create(code=code, disasterType=disaster_type,
                                      status=0, o_URL=o_url,requestunit=request_unit,
                                      date=time_str)
    # 依据disasterType查找数据并返回
    if (disaster_type == '336'):
        table_name =  "front_commdisaster"
    if (disaster_type == '111'):
        print("暂时没有这个表")
    if (disaster_type == '221'):
        print("暂时没有这个表")
    if (disaster_type == '441'):
        print("暂时没有这个表")
    if (disaster_type== '552'):
        print("暂时没有这个表")

    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    sql_word = ('select * from', table_name,'where code =', code)
    sql =' '.join(sql_word)
    cur.execute(sql)
    request_data = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    # json格式返回前端
    response = HttpResponse(json.dumps(request_data),
                            content_type="application/json")
    return response


# 选择查看已发送还是未发送
def status(request):
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    sql_word = "select * from `front_requestList`"  # 显示全部数据

    cur.execute(sql_word)
    request_data = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()

    # 进行筛选，已发送数据、未发送数据、发送数据
    if request.POST:
        status = request.POST.get('status',None)
        if (status == "已处理"):   # 已发送数据
            sql_word = "select * from `front_requestList` where status = 1 "
            conn = sqlite3.connect("db.sqlite3")
            cur = conn.cursor()
            cur.execute(sql_word)
            request_data = cur.fetchall()  # 搜取所有结果
            cur.close()
            conn.close()
            response = HttpResponse(json.dumps(request_data))
            print(response)

        if (status == "未处理"):  # 未发送数据
            sql_word = "select * from `front_requestList` where status = 0 "
            conn = sqlite3.connect("db.sqlite3")
            cur = conn.cursor()
            cur.execute(sql_word)
            request_data = cur.fetchall()  # 搜取所有结果
            cur.close()
            conn.close()
            response = HttpResponse(json.dumps(request_data))
            print(response)

        if (status == "发送数据"):  # 发送数据，更改status的值
            sql_word1 = "update front_requestList set status = 1 where status = 0 "    # 更新数据
            conn = sqlite3.connect("db.sqlite3")
            cur = conn.cursor()
            cur.execute(sql_word1)
            conn.commit()
            print("更新成功")
            sql_word2 = "select * from `front_requestList` where status = 0 "  # 显示剩余的status = 0的数据
            cur.execute(sql_word2)
            request_data = cur.fetchall()  # 搜取所有结果
            print(request_data)
            cur.close()
            conn.close()
            response = HttpResponse(json.dumps(request_data))
            print(response)

    return render(request,'status.html', {'items': request_data})