from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, response
from django.template.loader import render_to_string
from lists.models import Item

from lists.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    '''
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    '''
    def test_home_page_returns_correct_html(self):
        '''
        request = HttpRequest()
        response = home_page(request)
        '''
        response = self.client.get('/')
        html =response.content.decode('utf8')

        if False:
            expected_html = render_to_string('home.html')
            self.assertEqual(html, expected_html)
        else:
            self.assertTrue(html.startswith('<html>'))
            self.assertIn('<title>To-Do lists</title>', html)
            self.assertTrue(html.strip().endswith('</html>'))

            self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):
        response =self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        # 修改针对保存 POST 请求数据的单元测试不让它渲染包含待办事项的响应而是重定向到首页
        self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # 保持最小测试单元
    def test_redirects_after_POST(self):
        response =self.client.post('/',data={'item_text':'A new list item'}) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    """Noused
    def test_displays_all_list_items(self):
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
    """

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class LiveViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        # self.assertIn('itemey 1', response.content.decode())
        # self.assertIn('itemey 2', response.content.decode())  
        ## Django 提供了 assertContains 方法它知道如何处理响应以及响应内容中的字节 
        ## assertContains 的附加好处————它直接指出测试失败的原因
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')




