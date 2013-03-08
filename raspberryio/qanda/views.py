from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.decorators.cache import cache_page

from hilbert.decorators import ajax_only
from mezzanine.utils.sites import current_site_id

from raspberryio.project.utils import AjaxResponse, cache_on_auth
from raspberryio.aggregator.models import FeedType, FeedItem, APPROVED_FEED
from raspberryio.qanda.models import Question, Answer
from raspberryio.qanda.forms import QuestionForm, AnswerForm


@cache_on_auth(60 * 5)
def index(request):
    questions = Question.objects.all()
    feed_type = get_object_or_404(FeedType, slug='raspberry-pi')
    return render(request, 'qanda/index.html', {
        'questions': questions,
        'feed_items': FeedItem.objects.filter(feed__feed_type=feed_type, feed__approval_status=APPROVED_FEED),
        'feed_type': feed_type
    })


@cache_on_auth(60 * 2)
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
    if request.user.is_authenticated():
        votes = request.user.answer_votes.filter(question=question) \
            .values_list('pk', flat=True)
        context.update({
            'votes': votes,
            'answer_create_form': AnswerForm(),
        })
    return render(request, 'qanda/question_detail.html', context)


@login_required
def question_create_edit(request, question_slug=None):
    user = request.user
    site = Site.objects.get(id=current_site_id)
    if question_slug:
        question = get_object_or_404(Question, slug=question_slug)
        if question.user != user and not user.is_superuser:
            return HttpResponseForbidden(
                'You are not the owner of this question'
            )
    else:
        question = Question(user=user, site=site)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():
        question_form.save()
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
        return redirect(answer)
    return redirect(question)


@login_required
@ajax_only
def upvote_answer(request, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk)
    result = answer.add_voter(request.user)
    return AjaxResponse(request, result)
