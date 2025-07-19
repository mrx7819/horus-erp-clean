from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def vistasprotegidas(request):
    return render(request, 'index.html')

def term_cond(request):
    return render(request, 'term_cond.html')