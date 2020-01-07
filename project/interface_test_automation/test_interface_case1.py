#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import  unittest
import json
# 测试用例(组)类
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', test_data=None, http=None, db1_cursor=None, db2_cursor=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db1_cursor = db1_cursor
        self.db2_cursor = db2_cursor


class TestInterfaceCase1(ParametrizedTestCase):
   def setUp(self):
       pass

   # 测试接口1
   def test_login_normal(self):
       
       headers = {
           'Content-Type': 'application/json'
        }
       self.http.set_header(headers)
       #response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
       #response = self.http.post(self.test_data.request_url,  str(self.test_data.request_param))
       status_code,response =self.http.post_json(self.test_data.request_url,str(self.test_data.request_param),header=headers)
       print('status_code:',status_code)
       print("打印返回后的dict类型响应：",response)
       print("实际获取响应的对象的类型 %s"  %type(response))
       #python json.dumps()的中文编码问题
       #参考：https://blog.csdn.net/angl129/article/details/98180036
       self.test_data.response=json.dumps(response,ensure_ascii=False)
       print("打印self.json1: %s" ,self.test_data.response)
       if {} == response:
            self.test_data.result = 'Error'
            try:
                 #更新结果表中的用例运行结果
                 self.db1_cursor.execute('UPDATE test_result SET result = %s ,response = %s WHERE case_id = %s', (self.test_data.result, self.test_data.response,self.test_data.case_id))
                 self.db1_cursor.execute('commit')
                
                 
            except Exception as e: 
                 print('???????  %s'  %e)
                 self.db1_cursor.execute('rollback')
            return 

       try:
           # 断言
#            self.assertTrue(response['login'], msg='登录成功')
           if status_code == 201:
             self.assertTrue(response['login'], msg='登录成功')
           if status_code == 400:
             self.assertIn("密码错误",response['error_message'] , msg='密码不存在')
           if status_code == 404:
             self.assertEqual(response['error_message'], "店铺不存在", msg='店铺不存在')
           self.test_data.result = 'Pass'
           #dump() missing 1 required positional argument: 'fp' 要用dumps
           #参考：https://pdf-lib.org/Home/Details/2970
           #python json.dumps()的中文编码问题
           #参考：https://blog.csdn.net/angl129/article/details/98180036
           self.test_data.response=json.dumps(response,ensure_ascii=False)
           print("打印self.json2: %s" ,self.test_data.response)
       except AssertionError as e:
           print('***  %s' % e)
           self.test_data.result = 'Fail'
           self.test_data.reason = '  @@@  %s' % e # 记录失败原因

       #更新结果表中的用例运行结果
       try:
            self.db1_cursor.execute('UPDATE test_result SET request_param = %s WHERE case_id = %s', (str(self.test_data.request_param), self.test_data.case_id))
            self.db1_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
            self.db1_cursor.execute('UPDATE test_result SET reason = %sWHERE case_id = %s', (self.test_data.reason,self.test_data.case_id))
            self.db1_cursor.execute('UPDATE test_result SET response = %sWHERE case_id = %s', (self.test_data.response,self.test_data.case_id))
            self.db1_cursor.execute('commit')
       except Exception as e:
           print('$$$ %s'  % e)
           self.db1_cursor.execute('rollback')

   def tearDown(self):
       pass