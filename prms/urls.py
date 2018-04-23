"""prms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from account import urls as account_urls
from checkin import urls as checkin_urls
from leave import urls as leave_urls
from group_file import url as group_file_urls
from brief import url as brief_urls
from api import urls as api_urls


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


urlpatterns = [
    url(r'^admin/jsi18n', i18n_javascript),  # 普通表单也可使用admin控件
    url(r'^admin/', admin.site.urls),  # 管理后台
    url(r'^', include(account_urls)),
    url(r'^', include(checkin_urls)),
    url(r'^', include(leave_urls)),
    url(r'^', include(group_file_urls)),
    url(r'^', include(brief_urls)),
    url(r'^api/', include(api_urls)),
]

# 上传文件需要开启
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
