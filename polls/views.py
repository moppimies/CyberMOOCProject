from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import sqlite3
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Question, Choice
#Login page so I can make a OWASP 9, security loggin failure. Issue: User can vote without logging in

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password = password)
        if user is not None: 
            login(request,user)
            return redirect('/polls')
        else:
            return render(request, 'polls/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'polls/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/login')


def index(request):
    if request.user.is_authenticated:
        question_list = Question.objects.order_by('pub_date')[:5]
        #template = loader.get_template('polls/index.html')
        context = {'latest_question_list': question_list ,}
        #return HttpResponse(template.render(context, request))
        return render(request, 'polls/index.html', context)
    else:   
        return render(request, 'polls/login.html')

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html',{'question': question}) 

    #return HttpResponse("You are looking at question %s" % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    #This is vulnarable to SQL injections, I have fixed it by using by using django methods and models which for the most part are tested and safe.
    #conn = sqlite3.connect("db.sqlite3")
    #cursor = connection.cursor()
    #cursor.execute(f"UPDATE polls_choice SET votes = votes+1 WHERE id = {question_id}" )
    #conn.commit()
    #question = Question.objects.raw(f"SELECT pk=question_id FROM myapp_question")
    question = get_object_or_404(Question, pk=question_id)
  

    Choice.objects.raw(f"UPDATE polls_choice SET votes = {1} WHERE id = {question_id}")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


