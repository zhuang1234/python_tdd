from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, response
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item,List
from lists.forms import ItemForm,EMPTY_ITEM_ERROR
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
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        ## assertIsInstance 检查表单是否属于正确的类
        self.assertIsInstance(response.context['form'], ItemForm)

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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    """
    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    """
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data = {'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        # 修改针对保存 POST 请求数据的单元测试不让它渲染包含待办事项的响应而是重定向到首页
        self.client.post('/lists/new',data={'text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    # 保持最小测试单元
    """
    def test_redirects_after_POST(self):
        response =self.client.post('/lists/new',data={'text':'A new list item'}) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    """
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # expected_error = "You can't have an empty list item"
        ## <span class="help-block">You can&#x27;t have an empty list item</span>
        expected_error = escape("You can't have an empty list item")
        # print(response.content.decode())
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

