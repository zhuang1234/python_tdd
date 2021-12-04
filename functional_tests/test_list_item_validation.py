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
    # @skip
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页不小心提交了一个空待办事项
        # 输入框中没输入内容她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 首页刷新了显示一个错误消息
        # 提示待办事项不能为空
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        # 她输入一些文字然后再次提交这次没问题了
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # 她有点儿调皮又提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 在清单页面她看到了一个类似的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        # 输入文字之后就没问题了
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

