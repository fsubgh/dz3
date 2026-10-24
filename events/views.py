from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F, Count
from django.core.paginator import Paginator
from .models import Event


def home(request):
    query = request.GET.get('q', '')

    events = Event.objects.active().select_related(
        'author'
    ).prefetch_related(
        'categories',
        'participants'
    ).annotate(
        participants_count=Count('participants', distinct=True),
        categories_count=Count('categories', distinct=True)
    )

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()

    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/home.html', {
        'page_obj': page_obj,
        'query': query,
    })


def detail(request, event_id):
    event = get_object_or_404(
        Event.objects.active().with_details().annotate(
            participants_count=Count('participants', distinct=True),
            categories_count=Count('categories', distinct=True)
        ),
        id=event_id
    )

    Event.objects.filter(id=event.id).update(
        views_count=F('views_count') + 1
    )

    event.refresh_from_db()

    return render(request, 'events/detail.html', {
        'event': event,
    })


def statistics(request):
    events = Event.objects.annotate(
        participants_count=Count('participants', distinct=True),
        categories_count=Count('categories', distinct=True)
    )

    sort = request.GET.get('sort', 'desc')

    if sort == 'asc':
        events = events.order_by('participants_count')
    else:
        events = events.order_by('-participants_count')

    return render(request, 'events/statistics.html', {
        'events': events,
        'sort': sort,
    })
