from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from lists.models import Item,List
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    """添加了新的视图，home可以精简了
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        # .objects.create 是创建新 Item 对象的简化方式无须再调用 .save() 方法
        return redirect('/lists/the-only-list-in-the-world/')
    """
    #items = Item.objects.all()
    # render第一个参数是请求对象、第二个参数是渲染的模板名、函数的第三个参数是一个字典把模板变量的名称映射在值上
    # return render(request, 'home.html', {'items': items})
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    error = None
    """7.12.4
    items = Item.objects.filter(list = list_)
    return render(request, 'list.html', {'items': items})
    """
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            # print(f"item.text == {item.text}")
            # print(List.objects.count(),Item.objects.count())
            item.full_clean()
            # print(f"item.text == {item.text}")
            # item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            print(f"item.text == 1111")
            ## full_clean 只是在验证，并没有删除节点
            item.delete()
            print(List.objects.count(), Item.objects.count())
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': list_,'error': error})

def new_list(request):
    list_ = List.objects.create()
    item  = Item.objects.create(text = request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{list_.id}/')

