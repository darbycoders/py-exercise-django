from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm

# Create your views here.
@login_required(login_url='common:login')
def question_create(req):
  if req.method == 'POST':
    form = QuestionForm(req.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.author = req.user
      question.created_at = timezone.now()
      question.save()
      return redirect('py_board:index')
  else:
    form = QuestionForm()

  context = {'form': form}
  return render(req, 'question_form.html', context)

@login_required(login_url='common:login')
def question_modify(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if req.user != question.author:
    messages.error(req, '수정권한이 없습니다')
    return redirect('py_board:detail', question_id=question.id)
  if req.method == "POST":
    form = QuestionForm(req.POST, instance=question)
    if form.is_valid():
      question = form.save(commit=False)
      question.updated_at = timezone.now()  # 수정일시 저장
      question.save()
      return redirect('py_board:detail', question_id=question.id)
  else:
    form = QuestionForm(instance=question)

  context = {'form': form}
  return render(req, 'question_form.html', context)

@login_required(login_url='common:login')
def question_delete(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if req.user != question.author:
    messages.error(req, '삭제권한이 없습니다')
    return redirect('py_board:detail', question_id=question.id)
  question.delete()
  return redirect('py_board:index')

@login_required(login_url='common:login')
def question_vote(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if req.user == question.author:
    messages.error(req, '본인이 작성한 글은 추천할수 없습니다')
  else:
    question.voter.add(req.user)

  return redirect('py_board:detail', question_id=question.id)
  