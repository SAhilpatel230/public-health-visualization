from django.core.management import call_command
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from public_health_visualization_app.models import LifeExpectancy, ImmunizationCoverage, MortalityRate

def index(request):
    # Populate database if needed
    if LifeExpectancy.objects.count() < 200:
        call_command('clean_life_expectancy')
    if ImmunizationCoverage.objects.count() < 200:
        call_command('clean_immunization_coverage')
    if MortalityRate.objects.count() < 200:
        call_command('clean_mortality_rate')

    # Get metric type from query params
    metric = request.GET.get('metric', 'life_expectancy')
    filters = {}
    queryset = None
    overview = {}
    sort_by = request.GET.get('sort', '-id')  # Default sort by most recent (descending id)

    # Handle metric-specific data
    if metric == 'life_expectancy':
        model = LifeExpectancy
        valid_sort_fields = ['id', 'state', 'county', 'life_expectancy', 'standard_error']
        filters = {
            'state': request.GET.get('state'),
            'county': request.GET.get('county') if request.GET.get('county') else '',  # Set county to "All" if empty
            'life_expectancy__gte': request.GET.get('min_value'),
            'life_expectancy__lte': request.GET.get('max_value'),
        }
    elif metric == 'immunization_coverage':
        model = ImmunizationCoverage
        valid_sort_fields = ['id', 'geography', 'estimate']
        filters = {
            'geography': request.GET.get('state'),  # Geography mapped to state
            'estimate__gte': request.GET.get('min_value'),
            'estimate__lte': request.GET.get('max_value'),
        }
    elif metric == 'mortality_rate':
        model = MortalityRate
        valid_sort_fields = ['id', 'state', 'year', 'deaths']
        filters = {
            'state': request.GET.get('state'),
            'year': request.GET.get('year'),
            'deaths__gte': request.GET.get('min_value'),
            'deaths__lte': request.GET.get('max_value'),
        }

    # Validate sort_by field
    if sort_by.lstrip('-') not in valid_sort_fields:
        sort_by = '-id'  # Default to '-id' if invalid sort field

    queryset = model.objects.filter(
        Q(**{k: v for k, v in filters.items() if v is not None and v != ''})
    ).order_by(sort_by)

    overview = queryset.aggregate(
        avg_value=Avg('life_expectancy' if metric == 'life_expectancy' else 'estimate' if metric == 'immunization_coverage' else 'deaths'),
        max_value=Max('life_expectancy' if metric == 'life_expectancy' else 'estimate' if metric == 'immunization_coverage' else 'deaths'),
        min_value=Min('life_expectancy' if metric == 'life_expectancy' else 'estimate' if metric == 'immunization_coverage' else 'deaths'),
        count=Count('id')
    )

    # Paginate the data preview
    paginator = Paginator(queryset, 20)  # Paginate by 20 rows
    page_number = request.GET.get('page', 1)
    preview_data = paginator.get_page(page_number)

    # Get distinct values for filters
    states = LifeExpectancy.objects.values_list('state', flat=True).distinct()
    counties = LifeExpectancy.objects.values_list('county', flat=True).distinct()

    return render(request, 'index.html', {
        'metric': metric,
        'filters': {k: v for k, v in filters.items() if v},
        'sort_by': sort_by,
        'overview': overview,
        'preview_data': preview_data,
        'page_number': page_number,
        'states': states,
        'counties': counties,
    })

def chart_data(request):
    metric = request.GET.get('metric')
    x_axis = request.GET.get('x_axis')
    y_axis = request.GET.get('y_axis')

    data = {
        'labels': [],
        'values': []
    }

    if metric == 'life_expectancy':
        queryset = LifeExpectancy.objects.all()
        data['labels'] = list(queryset.values_list(x_axis, flat=True))
        data['values'] = list(queryset.values_list(y_axis, flat=True))
    elif metric == 'immunization_coverage':
        queryset = ImmunizationCoverage.objects.all()
        data['labels'] = list(queryset.values_list(x_axis, flat=True))
        data['values'] = list(queryset.values_list(y_axis, flat=True))
    elif metric == 'mortality_rate':
        queryset = MortalityRate.objects.all()
        data['labels'] = list(queryset.values_list(x_axis, flat=True))
        data['values'] = list(queryset.values_list(y_axis, flat=True))

    return JsonResponse(data)
