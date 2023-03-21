from django.shortcuts import render
from app_employment.models import Vacancy
from django.contrib.auth.decorators import permission_required


@permission_required('app_employment.view_vacancy')
def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'app_employment/vacancy_list.html', {'vacancy_list': vacancies})

