import xadmin
from .models import App, App_Param



class AppAdmin(object):
    list_display = ["name", "name_exe","path","version", "created_time","updated_time"]
    search_fields = ['name', ]
    list_editable = ["name", ]
    list_filter = ["name","name_exe"]


class AppParamAdmin(object):
    list_display = ["name", "value", "desc", "is_visiable", "app"]
    list_filter = ["name",]
    search_fields = ['name',]


xadmin.site.register(App, AppAdmin)
xadmin.site.register(App_Param, AppParamAdmin)