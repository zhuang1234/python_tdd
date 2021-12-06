from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from lists.models import Item,List
# from lists.forms import ItemForm
from django.http import HttpResponse
from lists.forms import ExistingListItemForm, ItemForm

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
    # return render(request, 'home.html')
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    """
    list_ = List.objects.get(id = list_id)
    error = None
    # 7.12.4
    # items = Item.objects.filter(list = list_)
    # return render(request, 'list.html', {'items': items})

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            # print(f"item.text == {item.text}")
            # print(List.objects.count(),Item.objects.count())
            item.full_clean()
            # print(f"item.text == {item.text}")
            # item.save()
            # return redirect(f'/lists/{list_.id}/')
            return redirect(list_)
        except ValidationError:
            print(f"item.text == 1111")
            ## full_clean 只是在验证，并没有删除节点
            item.delete()
            print(List.objects.count(), Item.objects.count())
            error = "You can't have an empty list item"
    form = ItemForm()
    return render(request, 'list.html', {
        'list': list_,"form": form, 'error': error
    })
    """
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            # Item.objects.create(text=request.POST['text'], list=list_)
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})
## 从用户的请求中读取数据结合一些定制的逻辑或 URL 中的信息 list_id 然后把数据传入表单进行验证如果通过验证就保存数据最后重定向或者渲染模板
def new_list(request):
    """
    list_ = List.objects.create()
    item  = Item.objects.create(text = request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    # return redirect(f'/lists/{list_.id}/')
    # return redirect('view_list', list_.id)
    ## 只需把重定向的目标对象传给redirect函数即可redirect函数会自动调用get_absolute_url函数
    return redirect(list_)
    """
    ## 把 request.POST 中的数据传给表单的构造方法
    form = ItemForm(data=request.POST)
    ##  使用 form.is_valid() 判断提交是否成功
    if form.is_valid():
        list_ = List.objects.create()
        # Item.objects.create(text=request.POST['text'], list=list_)
        form.save(for_list=list_)
        return redirect(list_)
    else:
        ## 如果提交失败把表单对象传入模板而不显示一个硬编码的错误消息字符串
        return render(request, 'home.html', {"form": form})
