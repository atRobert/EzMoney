from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from .models import UserProfile, UserIncome, UserGoal, UserPay
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from decimal import *
from django.utils import timezone
import random

def home_view(request):

    encouragement = [
                        'You got this!',
                        "Let's get this bread!",
                        'Ez Money!',
                        'Another day, another dollar! Keep it up!']

    def expected_progress(day_start, day_end, end_amount):
         days_elapsed = (timezone.now().date() - day_start).days
         days_of_goal = (day_end - day_start).days
         projection_percentage = Decimal(str(days_elapsed / days_of_goal))
         projection = projection_percentage * Decimal(str(end_amount))
         rounded_percentage = round((projection_percentage * 100))
         return round(projection, 2), rounded_percentage

    def projection_progress(day_start, day_end, current_savings):
        days_elapsed = (timezone.now().date() - day_start).days
        if days_elapsed == 0:
            days_elapsed = 1
        savings_per_day = Decimal(str(current_savings)) / Decimal(str(days_elapsed))
        days_of_goal = (day_end - day_start).days
        savings_by_end = Decimal(str(savings_per_day)) * Decimal(str(days_of_goal))
        return savings_by_end


    user = request.user
    if user.is_authenticated:
        user_profile = UserProfile.objects.get(user = user)
        income_given = user_profile.income_info
        user_current_savings = ''
        user_income_pk = ''
        user_goal_pk = ''
        goal_given = user_profile.goal_info
        added_money = UserPay.objects.filter(user=user).order_by('-id')[:5]
        print(added_money)
        you_percent = ''
        current_expectation = ''
        if income_given:
            user_financial_info = UserIncome.objects.get(user = user)
            print(user_financial_info)
            user_income_pk = user_financial_info.id
            user_current_savings = user_financial_info.current_savings
        if goal_given:
            user_goal_info = UserGoal.objects.get(user = user)
            user_goal_pk = user_goal_info.id
            user_current_goal = user_goal_info.goal_amount
            user_goal_date = user_goal_info.save_date
            current_progress = round((user_current_savings / user_current_goal * 100))
            you_should_be_here, you_percent = expected_progress(
                (user_goal_info.current_date), user_goal_date, user_current_goal)
            current_expectation = round(projection_progress(
                (user_goal_info.current_date), user_goal_date, user_current_savings), 2)
        else:
            user_current_goal = ''
            user_goal_date = ''
            current_progress = ''

        context = {'income_given':income_given,
                    'user_current_savings':user_current_savings,
                    'goal_given':goal_given,
                    'user_income_pk':user_income_pk,
                    'added_money':added_money,
                    'user_current_goal':user_current_goal,
                    'user_goal_date':user_goal_date,
                    'user_goal_pk': user_goal_pk,
                    'current_progress':current_progress,
                    'projected_progress': you_percent,
                    'current_expectation': current_expectation,
                    'encourage': random.choice(encouragement)}

        return render(request, 'userbase/home.html', context)
    else:
        return redirect('login')


class PaymentListView(ListView):
    model = UserPay
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return UserPay.objects.filter(user=user)


def signup_view(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.userprofile.first_name = form.cleaned_data.get('first_name')
            user.userprofile.last_name = form.cleaned_data.get('last_name')
            user.userprofile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'userbase/signup.html', {'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')


class IncomeCreateView(CreateView):
    model = UserIncome
    fields = ['income_type','pay_cycle','income_amount',
                'after_tax', 'monthly_expenses']

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.income_type == 'salary':
            obj.gross_income = obj.income_amount
        else:
            obj.gross_income = obj.income_amount * 2000
        obj.net_income = (
            obj.gross_income * obj.after_tax * Decimal('0.01')) - obj.monthly_expenses
        obj.weekly_net = obj.net_income / 52
        obj.user = self.request.user
        obj.save()
        return redirect('home')


class GoalCreateView(CreateView):
    model = UserGoal
    fields = ['save_date','goal_amount']
    template_name = 'userbase/usergoal_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GoalCreateView, self).get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        user_income = UserIncome.objects.get(user = user)
        weekly_net = user_income.weekly_net
        context['weekly_net'] = weekly_net
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('home')


class PayCreateView(CreateView):
    model = UserPay
    fields = ['date_added','amount_added']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('home')


class GoalUpdateView(UpdateView):
    model = UserGoal
    fields = ['save_date','goal_amount']
    template_name = 'userbase/usergoalupdate_form.html'
    success_url = '/'

    def get_queryset(self):
        user = self.request.user
        return UserGoal.objects.get(user=user)

    def get_object(self):
        user = self.get_queryset()
        return get_object_or_404(UserGoal, id=user.id)


class IncomeUpdateView(UpdateView):
    model = UserIncome
    fields = ['income_type','pay_cycle','income_amount',
                'after_tax', 'monthly_expenses']
    template_name = 'userbase/userincomeupdate_form.html'
    success_url = '/'

    def get_queryset(self):
        user = self.request.user
        return UserIncome.objects.get(user=user).id

    def get_object(self):
        id_ = self.get_queryset()
        return get_object_or_404(UserIncome, id=id_)
