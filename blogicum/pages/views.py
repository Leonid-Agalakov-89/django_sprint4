from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """
    View-класс для представления
    страницы "О проекте"
    """

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """
    View-класс для представления
    страницы "Правила"
    """

    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    """
    View-функция для представления
    кастомной страницы ошибки 404 "Ошибка проверки CSRF, запрос отклонён"
    """
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """
    View-функция для представления
    кастомной страницы ошибки 404 "Страница не найдена"
    """
    return render(request, 'pages/404.html', status=404)


def server_error(request, *args, **argv):
    """
    View-функция для представления
    кастомной страницы ошибки 500 "Сервер не может обработать запрос к сайту"
    """
    return render(request, 'pages/500.html', status=500)
