"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static

from config.settings import base, debug
from py_board import views

# === re_path 패턴 정규식 === #
# ^ 문자열이 시작할 때
# $ 문자열이 끝날 때
# \d 숫자
# + 바로 앞에 나오는 항목이 계속 나올 때
# () 패턴의 부분을 저장할 때

urlpatterns = [
    path('admin/', admin.site.urls),
    path('py_board/', include('py_board.urls')),
    path('common/', include('common.urls')),
    path('', views.index, name='index'),
]

# 어떤 URL을 정적으로 추가할래? > MEDIA_URL을 static 파일 경로로 추가
# 실제 파일은 어디에 있는데? > MEDIA_ROOT 경로내의 파일을 static 파일로 설정
if debug.DEBUG:
    # import debug_toolbar
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

# django.contrib.auth.urls 포함된 url
# ^login/$ [name='login']
# ^logout/$ [name='logout']
# ^password_change/$ [name='password_change']
# ^password_change/done/$ [name='password_change_done']
# ^password_reset/$ [name='password_reset']
# ^password_reset/done/$ [name='password_reset_done']
# ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
# ^reset/done/$ [name='password_reset_complete']