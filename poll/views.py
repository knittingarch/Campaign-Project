
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list': latest_question_list }
    return render(request, 'poll/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.session.get('has_voted', False):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': ("You've already voted."),
            })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "Make sure to select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        request.session['has_voted'] = True
        return HttpResponseRedirect(reverse('results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    trial = question.choice_set.aggregate(Max('votes'))
    winner = trial.items()[0][1]
    return render(request, 'poll/results.html', {
        'question': question,
        'winner': winner,
    })