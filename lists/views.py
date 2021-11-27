from django.shortcuts import render,redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        # .objects.create 是创建新 Item 对象的简化方式无须再调用 .save() 方法
        return redirect('/')

    items = Item.objects.all()

    # render第一个参数是请求对象、第二个参数是渲染的模板名、函数的第三个参数是一个字典把模板变量的名称映射在值上
    return render(request, 'home.html', {'items': items})
