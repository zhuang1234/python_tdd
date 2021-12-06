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
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页不小心提交了一个空待办事项
        # 输入框中没输入内容她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        """
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
        """
        # 浏览器截获了请求
        # 清单页面不会加载
        ## 不再检查我们自定义的错误消息而是通过 CSS 伪选择符 :invalid 检查。这个伪选择符是浏览器为输入无效内容的 HTML5 输入框添加的。
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # 她在待办事项中输入了一些文字
        # 错误消失了
        ## 输入有效的内容时伪选择符逆转
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # 现在能提交了
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 她有点儿调皮打算再提交一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器这次也不会放行
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # 输入一些文字后就能纠正这个错误
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # 伊迪丝访问首页新建一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # 她不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 她看到一条有帮助的错误消息
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
         # 伊迪丝新建一个清单但方法不当所以出现了一个验证错误
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

         # 为了消除错误她开始在输入框中输入内容
        self.get_item_input_box().send_keys('a')

         # 看到错误消息消失了她很高兴
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))