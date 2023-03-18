from django.urls import path
from .views import IncomesList, IncomeDetailView


urlpatterns = [
    path('', IncomesList.as_view(), name='incomes'),
    path('<int:id>', IncomeDetailView.as_view(), name='income-detail'),
]

