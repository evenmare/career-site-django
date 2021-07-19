import job_app.data as data


def default_data(request):
    return {
        'title': data.title,
        'subtitle': data.subtitle,
        'back': data.back,
        'next': data.next_step,
        'home': data.home,
    }
