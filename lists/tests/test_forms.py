from django.test import TestCase
from lists.forms import ItemForm,EMPTY_ITEM_ERROR

class ItemFormTest(TestCase):
    """
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        ## form.as_p() 的作用是把表单渲染成 HTML
        self.fail(form.as_p())
    """
    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        ## 调用 form.is_valid() 得到的返回值是 True 或 False 不过还有个附带效果即验证输入的数据生成 errors 属性。
        # errors 是个字典把字段的名字映射到该字段的错误列表上一个字段可以有多个错误
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_ITEM_ERROR])
        # form.save()