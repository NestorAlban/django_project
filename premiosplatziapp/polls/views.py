
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# def index(request):
#     lastest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "lastest_question_list": lastest_question_list
#     })


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/detail.html", {
#         "question": question
#     })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lastest_question_list"
    #lte means least than or equal to
    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(published_date__lte=timezone.now()).order_by( "-published_date")[:5]

#con el - es desde las más nuevas a las viejas, sin el - es de viejas a nuevas

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        """
        return Question.objects.filter(published_date__lte = timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, pk):
    question = get_object_or_404(Question, pk = pk)
    try:
        selected_choice = question.choice_set.get(
            pk = request.POST["choice"]
            )
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "No elegiste una respuesta"
        }) 
    else: 
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse(
            "polls:results", 
            args=(pk,)
        ))


# Create your views here.
