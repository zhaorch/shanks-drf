"""shanksDRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from django.views.static import serve
from django.urls import path,re_path,include
from rest_framework.routers import DefaultRouter
from shanksDRF.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from users.views import UserViewSet
from project.views import AppViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name="users")
router.register(r'apps', AppViewSet, base_name="apps")

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    re_path(r'^ueditor/', include('DjangoUeditor.urls')),

    re_path(r'docs/', include_docs_urls(title="渣渣网")),

    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWF 认证接口
    path(r'login/', obtain_jwt_token),

    path('', include(router.urls)),
]
