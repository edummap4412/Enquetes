from django.http  import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Retorna as cinco ultimas publicações"""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    def get_queryset(self):
        """
        Exclui qualquer question que não foi publicada ainda.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ReseultView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question':question,
        'error_message': "Escolha uma uma alternativa"
    }
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(request, 'detail.html', context)

    else:
        selected_choice.votes +=1
        selected_choice.save()

        return HttpResponseRedirect(reverse('results',args=(question.id,)))



