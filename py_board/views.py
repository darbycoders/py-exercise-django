from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Question, Answer
from .forms import QuestionForm

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

def question_create(req):
  if req.method == 'POST':
    form = QuestionForm(req.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.created_at = timezone.now()
      question.save()
      return redirect('py_board:index')
  else:
    form = QuestionForm()
  context = {'form': form}
  return render(req, 'question_form.html', context)

# # 방법1
# def answer_create(req, question_id):
#   print(question_id)
#   question = get_object_or_404(Question, pk=question_id)
#   question.answer_set.create( # answer_set는 Answer model과 관계의 의미
#     content=req.POST.get('content'),
#     created_at=timezone.now()
#   )
#   return redirect('py_board:detail', question_id=question.id)

# 방법2
def answer_create(req, question_id):
  print(req.method)
  question = get_object_or_404(Question, pk=question_id)
  answer = Answer(
    question=question,
    content=req.POST.get('content'),
    created_at=timezone.now()
  )
  answer.save()
  return redirect('py_board:detail', question_id=question.id)