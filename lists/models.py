from django.db import models

# Create your models here.
# 在Django 3.2中开始新项目时，主键的默认类型设置为BigAutoField，这是一个64位整数（64 bit integer）。
# 但是，早期版本将隐式主键的类型设置为整数（integer）。
# 这意味着当您升级到3.2版本时，您将开始看到有关您没有显式定义的主键类型的警告。
# 满足Django对显式设置主键类型的要求很容易，但您还需要选择是否要将主键字段类型从整数升级到64位整数。
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


## 若想保存对象之间的关系要告诉 Django 两个类之间的关系这种关系使用 ForeignKey 字段表示
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    """django 升级到2.0之后,表与表之间关联的时候,必须要写on_delete参数,否则会报异常
            on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
    	    on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
    	    on_delete=models.DO_NOTHING,  # 删除关联数据,什么也不做
    	    on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
    	    # models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
    	    on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
    	    models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
    	    on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
    	    on_delete=models.SET,         # 删除关联数据,
    	    a. 与之关联的值设置为指定值,设置：models.SET(值)
    	    b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
         """

    ## 记得查阅Django 文档中对模型属性 Meta 的说明
    class Meta:
        unique_together = ('list', 'text')



## 删除迁移是种危险操作但偶尔需要这么做因为不可能从一开始就正确定义模型。
## 如果删除已经用于某个数据库的迁移Django 就不知道当前状态因此也就不知道如何运行以后的迁移。
## 只有当你确定某个迁移没被使用时才能将其删除。根据经验已经提交到 VCS 的迁移决不能删除