from django.db.models import Count, Sum, F
from .models import Task, Budget, Expense, Project

def get_project_progress(project):
    total_tasks = Task.objects.filter(project=project).count()
    completed_tasks = Task.objects.filter(project=project, status='completed').count()
    progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return progress

def get_task_status_distribution(project):
    status_distribution = Task.objects.filter(project=project).values('status').annotate(count=Count('status'))
    return status_distribution

def get_budget_vs_actual_spending(project):
    budget_data = Budget.objects.filter(project=project).values('category').annotate(budgeted=Sum('amount'))
    expense_data = Expense.objects.filter(project=project).values('category').annotate(spent=Sum('amount'))
    data = {item['category']: {'budgeted': item['budgeted'], 'spent': 0} for item in budget_data}
    for item in expense_data:
        if item['category'] in data:
            data[item['category']]['spent'] = item['spent']
        else:
            data[item['category']] = {'budgeted': 0, 'spent': item['spent']}
    return data

def get_expense_breakdown(project):
    expense_breakdown = Expense.objects.filter(project=project).values('category').annotate(amount=Sum('amount'))
    return expense_breakdown