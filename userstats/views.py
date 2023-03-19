import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from expenses.models import Expense
from income.models import Income


class ExpenseSummaryStatsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {
            'amount': str(amount)
        }

    def get_category(self, expense):
        return expense.category

    def get(self, request):
        today = datetime.date.today()
        year = today - datetime.timedelta(365)
        expenses = Expense.objects.filter(owner=request.user, date__gte=year, date__lte=today)
        result = {}
        categories = list(set(map(self.get_category, expenses)))

        # for expense in expenses:
        for category in categories:
            result[category] = self.get_amount_for_category(expenses, category)

        return Response({'category_data': result}, status=status.HTTP_200_OK)


class IncomesSummaryStatsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_amount_for_source(self, incomes_list, source):
        incomes = incomes_list.filter(source=source)
        amount = 0
        for income in incomes:
            amount += income.amount
        return {
            'amount': str(amount)
        }

    def get_source(self, income):
        return income.source

    def get(self, request):
        today = datetime.date.today()
        year = today - datetime.timedelta(365)
        incomes = Income.objects.filter(owner=request.user, date__gte=year, date__lte=today)
        result = {}
        sources = list(set(map(self.get_source, incomes)))

        # for expense in expenses:
        for source in sources:
            result[source] = self.get_amount_for_source(incomes, source)

        return Response({'source_data': result}, status=status.HTTP_200_OK)
