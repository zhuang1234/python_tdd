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

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # 伊迪丝访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框完美地居中显示
        inputbox = self.get_item_input_box()
        # assertAlmostEqual 的作用是帮助处理舍入误差以及偶尔由滚动条等事物导致的异常这里指定计算结果在正负 10 像素范围内为可接受
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
