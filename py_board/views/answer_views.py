from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Question, Answer
from ..forms import AnswerForm

# Create your views here.
# # 방법1
# def answer_create(req, question_id):
#   print(question_id)
#   question = get_object_or_404(Question, pk=question_id)
#   question.answer_set.create( # answer_set는 Answer model과 관계의 의미
#     content=req.POST.get('content'),
#     created_at=timezone.now()
#   )
#   return redirect('py_board:detail', question_id=question.id)

# # 방법2
# def answer_create(req, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   answer = Answer(
#     question=question,
#     content=req.POST.get('content'),
#     created_at=timezone.now()
#   )
#   answer.save()
#   return redirect('py_board:detail', question_id=question.id)

# 방법3
@login_required(login_url='common:login')
def answer_create(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  
  if req.method == 'POST':
    form = AnswerForm(req.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = req.user  # author 속성에 로그인 계정 저장
      answer.created_at = timezone.now()
      answer.question = question
      answer.save()
      return redirect('{}#answer_{}'.format(
        resolve_url('py_board:detail', question_id=question.id), answer.id
      ))
      # return redirect('py_board:detail', question_id=question.id)
  else:
    return HttpResponseNotAllowed('Only POST is possible.')

  context = {'question': question, 'form': form}
  return render(req, 'question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(req, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if req.user != answer.author:
    messages.error(req, '수정권한이 없습니다')
    return redirect('py_board:detail', question_id=answer.question.id)
  if req.method == "POST":
    form = AnswerForm(req.POST, instance=answer)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.updated_at = timezone.now()
      answer.save()
      return redirect('{}#answer_{}'.format(
        resolve_url('py_board:detail', question_id=answer.question.id), answer.id
      ))
  else:
    form = AnswerForm(instance=answer)

  context = {'answer': answer, 'form': form}
  return render(req, 'answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(req, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if req.user != answer.author:
    messages.error(req, '삭제권한이 없습니다')
  else:
    answer.delete()

  return redirect('py_board:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user == answer.author:
    messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
  else:
    answer.voter.add(request.user)
  return redirect('{}#answer_{}'.format(
    resolve_url('py_board:detail', question_id=answer.question.id), answer.id
  ))