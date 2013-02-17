from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from actstream import action
from mezzanine.utils.sites import current_site_id

from raspberryio.qanda.models import Question, Answer
from raspberryio.qanda.forms import QuestionForm, AnswerForm


def question_list(request):
    questions = Question.objects.all()
    return render(request, 'qanda/question_list.html', {
        'questions': questions,
    })


def question_detail(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug)
    answers = question.answers.all()
    context = {
        'question': question,
        'answers': answers,
    }
    if request.user.is_authenticated:
        context.update({
            'answer_create_form': AnswerForm(),
        })
    return render(request, 'qanda/question_detail.html', context)


@login_required
def question_create_edit(request, question_slug=None):
    user = request.user
    site = Site.objects.get(id=current_site_id)
    if question_slug:
        question = get_object_or_404(Question, slug=question_slug)
    else:
        question = Question(user=user, site=site)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():
        question_form.save()
        action.send(user, verb='asked', target=question)
        return redirect(question)
    return render(request, 'qanda/question_create_edit.html', {
        'question': question,
        'question_form': question_form,
    })


@login_required
def answer_create_edit(request, question_slug, answer_pk=None):
    question = get_object_or_404(Question, slug=question_slug)
    if answer_pk:
        answer = get_object_or_404(Answer, pk=answer_pk)
    else:
        answer = Answer(user=request.user, question=question)
    answer_form = AnswerForm(request.POST or None, instance=answer)
    if answer_form.is_valid():
        answer_form.save()
        action.send(request.user, verb='answered', target=answer)
        return redirect(answer)
    return redirect(question)
