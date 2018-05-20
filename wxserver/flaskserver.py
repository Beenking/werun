#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
# 导入数据库模块
import pymysql
import requests
import json
# 导入Flask框架，这个框架可以快捷地实现了一个WSGI应用
from flask import Flask
# 默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import Response
from flask import render_template
# 导入前台请求的request模块
from flask import request
import traceback

# 传递根目录
from WXBizDataCrypt import WXBizDataCrypt

app = Flask(__name__)

appid = 'wx46a8613d76cb807d'
secret = '87a55a5b8627122cfc1b2a82e6030cf0'
openid = ''  # get after longin
session_key = ''  # get after login
db = pymysql.connect("localhost", "root", "", "werun", charset="utf8")


# 默认路径访问登录页面
@app.route('/')
def login():
    return render_template('login.html')


# 默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')


# 设置响应头
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    user = request.args.get('user', type=str)
    password = request.args.get('password', type=str)
    sql = "INSERT INTO temp_user(user, password) VALUES ('%s', '%s')" % (user, password)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        return render_template('login.html')
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()


# 获取登录参数及处理
@app.route('/login')
def getLoginRequest():
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    user = request.args.get('user', type=str)
    password = request.args.get('password', type=str)
    sql = "select * from tb_user where user='%s' and password='%s'" % (user, password)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results) == 1:
            return '登录成功'
        else:
            return '用户名或密码不正确'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()


@app.route('/wxusr', methods=['POST'])
def wxusr_login():
    # get openid and session_key with code from weixin api server
    code = request.form['code']
    url_openid = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s' % (appid, secret, code)
    res = requests.get(url_openid, verify=False)
    dict_user_id = json.loads(res.content)
    global openid, session_key
    openid = dict_user_id['openid']
    session_key = dict_user_id['session_key']

    dict_user_info = {}
    user_info = request.form['userInfo']
    dict_user_info = json.loads(s=user_info)
    dict_user_info['openid'] = openid
    dict_user_info['session_key'] = session_key
    d = dict_user_info
    print(dict_user_info)
    sql = "INSERT INTO tb_user(openid,session_Key,nickName,gender,language,city,province,country,avatarUrl) " \
          "VALUES('%s','%s','%s',%d,'%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE nickName='%s'" \
          % (d['openid'], d['session_key'], d['nickName'], d['gender'], d['language'], d['city'], d['province'],
             d['country'], d['avatarUrl'], d['nickName'])
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    return "success"


@app.route('/getStepData', methods=['POST'])
def get_step_data():
    global res
    if request.method == 'POST':
        dic = request.form.to_dict()
        if not appid == '' and not session_key == '':
            pc = WXBizDataCrypt(appid, session_key)
            step_data = pc.decrypt(dic['encryptedData'], dic['iv'])

            step_today = step_data['stepInfoList'][29]['step'];
            sql = "UPDATE tb_user SET steps=%d WHERE openid='%s'" % (step_today, openid)
            print(sql)
            cursor = db.cursor()
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

            print(step_data)
            res = step_data
        else:
            print('appid: ', appid)
            print('session_key:', session_key)
            res = ''
    return json.dumps(res, ensure_ascii=False)


@app.route('/ranks', methods=['POST'])
def get_ranks():
    cursor = db.cursor()
    dic = request.form.to_dict()
    if dic['user'] == 'wb':
        sql = "select nickName, steps, upvotes, avatarUrl  from tb_user"
        try:
            # 执行sql语句
            cursor.execute(sql)
            data = cursor.fetchall()
            jsonData = []
            for row in data:
                result = {}
                result['name'] = row[0]
                result['steps'] = row[1]
                result['upvotes'] = row[2]
                result['avatar'] = row[3]
                jsonData.append(result)
            jsondator = json.dumps(jsonData, ensure_ascii=True)
            return jsondator
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()
    else:
        return ''


# 使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
# 启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
