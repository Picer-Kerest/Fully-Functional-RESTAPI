from django.urls import path
from .views import ExpenseDetailView, ExpensesList


urlpatterns = [
    path('', ExpensesList.as_view(), name='expenses'),
    path('<int:id>', ExpenseDetailView.as_view(), name='expense-detail'),
]

