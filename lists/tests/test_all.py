from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, response
from django.template.loader import render_to_string
from lists.models import Item,List

from lists.views import home_page, new_list


# Create your tests here.
class HomePageTest(TestCase):
    """
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    """
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
            # self.assertTrue(html.startswith('<html>'))
            self.assertIn('<title>To-Do lists</title>', html)
            self.assertTrue(html.strip().endswith('</html>'))

            self.assertTemplateUsed(response, 'home.html')

    def test_uses_home_template(self):
        response =self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    """7.8.3删除多余测试
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    """
    """Noused
    def test_displays_all_list_items(self):
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
    """

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_item(self):
        list_ =List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    # def test_displays_all_items(self):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'itemey 1', list=correct_list)
        Item.objects.create(text = 'itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = 'itemey 1', list=other_list)
        Item.objects.create(text = 'itemey 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        # self.assertIn('itemey 1', response.content.decode())
        # self.assertIn('itemey 2', response.content.decode())  
        ## Django 提供了 assertContains 方法它知道如何处理响应以及响应内容中的字节 
        ## assertContains 的附加好处————它直接指出测试失败的原因
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
        # response.context 表示要传入 render 函数的上下文——Django 测试客户端把上下文附在 response 对象上方便测试。
        

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        # 修改针对保存 POST 请求数据的单元测试不让它渲染包含待办事项的响应而是重定向到首页
        self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # 保持最小测试单元
    """
    def test_redirects_after_POST(self):
        response =self.client.post('/lists/new',data={'item_text':'A new list item'}) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    """
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')