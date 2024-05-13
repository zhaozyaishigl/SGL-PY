# import logging
# import unittest,os,time
# from lib.HTMLTestRunner import HTMLTestRunner
# from lib.send_email import send_email
# from config.config import *
# from test.suit.test_suit import *
import logging
import pickle
import sys
# class MyTestCase(unittest.TestCase):
#     def test_all(self):
#         logging.info("运行所有的case")
#         suit=unittest.defaultTestLoader.discover(test_path,'test*.py')
#         # t=time.strftime('%Y_%m_%d_%H_%M_%S')
#         with open(report_file,'wb')as f:
#             HTMLTestRunner(
#                 stream=f,
#                 title='xzs测试用例',
#                 description='xzs登录和注册用例集',
#                 verbosity=2
#             ).run(suit)
#
#         send_email(report_file)
#         logging.info("=======================测试结束======================")
# if __name__ == '__main__':
#     unittest.main()


import time, unittest
from lib.HTMLTestRunner import HTMLTestRunner
from lib.send_email import send_email
from config.config import *
from test.suit.test_suit import get_suit

def discover():
    return unittest.defaultTestLoader.discover(test_case_path,'test*.py')

def run(suite): #执行测试用例，生成测试报告
    logging.info("====测试开始====")
    with open(report_file,'wb')as f:
        result =HTMLTestRunner(
            stream=f,
            title="接口测试",
            description="测试描述",
            verbosity=2
        ).run(suite)
    if result.failures:
        save_faliures(result, last_fails_file)#保存失败用例到文件
        logging.error("测试失败，失败用例已保存到文件：{}".format(last_fails_file))
    else:
        logging.info("测试成功")
    send_email(report_file)
    logging.info("====测试结束====")
    #发送邮件
    send_email(report_file)
    logging.info("********发送邮件**********")

def run_all(): #运行所有用例
    run(discover())

def run_suite(suite_name): #运行自定义的testsuite
    suite=get_suit(suite_name) #通过套件名称返回套件实例
    print(suite)
    if isinstance(suite,unittest.TestSuite):
        run(suite) #运行套件
    else:
        print("TestSuite不存在")




def collect():
    suite=unittest.TestSuite()
    def _collect(tests):
        # 如果下级元素是TestCase则继续往下找
        if isinstance(tests,unittest.TestSuite):
            #如果TestSuite中有用例则继续往下找
            if tests.countTestCases() !=0:
                #遍历调用
                for i in tests:
                    #递归调用
                    _collect(i)
        else:
            # 如果下级元素是TestCase,则添加到TestSuite中
            suite.addTest(tests)
            #unittest.defaultTestLoader.discover(test_case_path)
    _collect(discover())
    return suite
def collect_only(): #仅列出所有用例
    t0=time.time()
    i =0
    for case in collect():
        i+=1
        print("{}.{}".format(str(i),case.id()))
    print("-----------------------")
    print("Collect {} tests is {:.3f}s".format(str(i),time.time() - t0))

def makesuite_by_testlist(testlist_file):
    with open(testlist_file,encoding='utf-8') as f:
        testlist = f.readlines()
    print(testlist)
    # for i in testlist:
    #     print(i.strip())
    #     print(i.startswith("#"))
    #去掉每行结尾的“/n”和#号开头的行
    testlist = [i.strip()for i in testlist if not i.startswith("#")]
    print(testlist)

    suite = unittest.TestSuite()
    all_cases = collect()  #获取工程test/case目录以及子目录下所有TestCase
    for case in all_cases:
        case_name = case.id().split('.')[-1]
        if case_name in testlist:  #从所有TestCase中匹配testlist中定义好的用例
            suite.addTest(case)
    return suite

#根据tag来组建suite
def makesuite_by_tag(tag):
    #申明一个suite
    suite = unittest.TestSuite()
    #获取当前所有的testcase
    for i in collect():
        #tag和标签都包含的时候
        if i._testMethodDoc and tag in i._testMethodDoc:
            #添加到suite中
            suite.addTest(i)
    return suite

def save_faliures(result, file):#file为序列化保存的文件名，配置在config/config。py中
    suite = unittest.TestSuite()
    for case_result in result.failures:
    #case_result是个元祖，第一个元素是用例对象，后面是失败原因等等
        suite.addTest(case_result[0])
    with open(file, 'wb') as f:
        pickle.dump(suite, f)#序列化到指定文件
def rerun_fails():#失败用例重跑方法
    #将用例路径添加到包搜索路径中，不然反序列化Testsuite会找不到用例
    sys.path.append(test_case_path)
    with open(last_fails_file, 'rb')as f:
        suite = pickle.load(f) # 反序列化得到失败的TesrSuite
    run(suite)

if __name__ == '__main__':
    suite = makesuite_by_tag("level1")
    run(suite)
