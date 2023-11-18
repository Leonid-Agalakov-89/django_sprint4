from django.shortcuts import render


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
