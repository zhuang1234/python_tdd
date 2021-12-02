from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest, response
from django.template.loader import render_to_string
from lists.models import Item,List
from django.core.exceptions import ValidationError
from lists.views import home_page, new_list



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

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            ## 保存数据时 Django 的模型不会运行全部验证
            ## Django 提供了一个方法用于运行全部验证即 full_clean
            item.full_clean()

