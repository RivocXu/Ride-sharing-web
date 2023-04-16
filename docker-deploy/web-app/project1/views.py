from django.shortcuts import render


def runoob(request):
    context = {}
    context['name'] = '菜鸟教程xx'
    return render(request, 'runoob.html', context)