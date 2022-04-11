from django.urls import path, re_path

from . import views

app_name = 'py_board'

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:question_id>/', views.detail, name='detail'),
  
  path('question/create/', views.question_create, name='question_create'),
  path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
  path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
  path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
  
  path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
  path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
  path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
  path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),
]