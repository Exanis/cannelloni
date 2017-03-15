# -*- coding: utf8 -*-

"Simple view to let angular work"

from django.shortcuts import render

def main(request):
    "Main view"
    return render(request, 'main.html', {})
