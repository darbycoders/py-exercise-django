from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Question

# Create your views here.
def index(req):
  page = req.GET.get('page', '1')
  question_list = Question.objects.order_by('-created_at')
  paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
  page_obj = paginator.get_page(page)
  context = {'question_list': page_obj}
  return render(req, 'question_list.html', context)

# shell 이용하여 테스트 리스트 생성하가
"""
from pybo.models import Question
from django.utils import timezone
for i in range(300):
  q = Question(subject='테스트 데이터입니다:[%03d]' % i, content='내용무', created_at=timezone.now())
  q.save()
"""

def detail(req, question_id):
  question = get_object_or_404(Question, id=question_id) # Question.objects.get(id=question_id)
  context = {'question': question}
  return render(req, 'question_detail.html', context)

def index(req):
  page = req.GET.get('page', '1')  # 페이지
  kw = req.GET.get('kw', '')  # 검색어
  question_list = Question.objects.order_by('-created_at')
  if kw:
    question_list = question_list.filter(
      Q(subject__icontains=kw) |  # 제목 검색
      Q(content__icontains=kw) |  # 내용 검색
      Q(answer__content__icontains=kw) |  # 답변 내용 검색
      Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
      Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
    ).distinct()
  paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
  page_obj = paginator.get_page(page)

  context = {'question_list': page_obj, 'page': page, 'kw': kw}
  return render(req, 'question_list.html', context)