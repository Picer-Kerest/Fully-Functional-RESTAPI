from django.urls import path
from .views import ExpenseSummaryStatsView, IncomesSummaryStatsView


urlpatterns = [
    path('expenses-stats', ExpenseSummaryStatsView.as_view(), name='expenses-stats'),
    path('incomes-stats', IncomesSummaryStatsView.as_view(), name='incomes-stats'),
]

