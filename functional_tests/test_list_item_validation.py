# from django.test import LiveServerTestCase
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from unittest import skip
from selenium.common.exceptions import WebDriverException
from .base import FunctionalTest

MAX_WAIT = 10
# import unittest

class ItemValidationTest(FunctionalTest):
    ## unittest提供的修饰器 @skip 可以临时禁止执行这个测试方法
    @skip
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页不小心提交了一个空待办事项
        # 输入框中没输入内容她就按下了回车键

        # 首页刷新了显示一个错误消息
        # 提示待办事项不能为空

        # 她输入一些文字然后再次提交这次没问题了

        # 她有点儿调皮又提交了一个空待办事项
        # 在清单页面她看到了一个类似的错误消息

        # 输入文字之后就没问题了
        self.fail('write me!')




# fail('Finish the test!')
#之后都使用 Django 的测试运行程序运行功能测试。可以删除
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
