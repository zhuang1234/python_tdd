# from django.test import LiveServerTestCase
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10
# import unittest

# class NewVisitorTest(unittest.TestCase):
# class NewVisitorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        # 通过环境变量 STAGING_SERVER 决定使用哪个服务器
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url= 'http://'+staging_server
    
    def tearDown(self) -> None:
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, rowtext):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows =table.find_elements_by_tag_name('tr')
                self.assertIn(rowtext, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() -start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retereve_it_later(self):
        # 伊迪丝听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
    def test_layout_and_styling(self):
        # 伊迪丝访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框完美地居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        # assertAlmostEqual 的作用是帮助处理舍入误差以及偶尔由滚动条等事物导致的异常这里指定计算结果在正负 10 像素范围内为可接受
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在一个文本框中输入了“Buy peacock feathers”购买孔雀羽毛
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 她按回车键后页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”使用孔雀羽毛做假蝇
        # 伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)


        # 页面再次更新她的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # 伊迪丝想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个URL发现她的待办事项列表还在

        # 她很满意去睡觉了
        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 她注意到清单有个唯一的URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 现在一名叫作弗朗西斯的新用户访问了网站

        # 使用两个 # 表示“元注释”。元注释的作用是说明测试的工作方式 以及为什么这么做。
        # 使用两个井号是为了和功能测试中解说用户故事的常规注释区分开。
        # 这个元注释是发给未来自己的消息如果没有这条消息到时你可能会觉得奇怪想知道到底为什么要退出浏览器再启动一个新会话
        ## 我们使用一个新浏览器会话  
        ## 确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 弗朗西斯输入一个新待办事项新建一个清单
        # 他不像伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两人都很满意然后去睡觉了


# fail('Finish the test!')
#之后都使用 Django 的测试运行程序运行功能测试。可以删除
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
