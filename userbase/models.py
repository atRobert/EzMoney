from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    income_info = models.BooleanField(default=False)
    goal_info = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()



class UserIncome(models.Model):
    INCOME_CHOICES = (
        ('salary','Salary'),
        ('hourly','Hourly'),
    )

    PAY_CHOICES = (
        ('weekly','Weekly'),
        ('biweekly','Biweekly'),
        ('twice', 'Twice a month'),
        ('monthly', 'Monthly')
    )

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    income_type = models.CharField(
                    max_length=32,
                    choices=INCOME_CHOICES,
                    blank=False)
    pay_cycle   = models.CharField(
                    max_length=32,
                    choices=PAY_CHOICES,
                    blank=False)

    income_amount = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = False,
                        max_digits = 8)

    current_savings = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = False,
                        max_digits = 10)

    after_tax = models.IntegerField(
                        default = 50,
                        blank=False)

    monthly_expenses = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = False,
                        max_digits = 10)

    gross_income = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = True,
                        max_digits = 10)

    net_income = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = True,
                        max_digits = 10)

    weekly_net = models.DecimalField(
                        default = 0.00,
                        decimal_places = 2,
                        blank = True,
                        max_digits = 10)


    def __str__(self):
        return self.user.username



def update_user_income(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserProfile.objects.filter(user = instance.user)
        qs.update(income_info=True)

#When user adds an income, it will switch UserProfile.income_info to True
post_save.connect(update_user_income, sender=UserIncome)



class UserGoal(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    save_percent = models.IntegerField(
                        default = 50,
                        blank=False)

    save_date    = models.DateField(
                    blank=False,
                    default = timezone.now() + timedelta(days=28))

    goal_amount  = models.DecimalField(
                    default = 0.00,
                    decimal_places =2,
                    blank = False,
                    max_digits = 10)

    current_date = models.DateField(
                    blank=False,
                    default = timezone.now())

    def __str__(self):
        return self.user.username


def update_user_goal(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserProfile.objects.filter(user = instance.user)
        qs.update(goal_info=True)

#When user adds an income, it will switch UserProfile.income_info to True
post_save.connect(update_user_goal, sender=UserGoal)


class UserPay(models.Model):
    list_display = ('date_added', 'amount_added', 'user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    date_added = models.DateField(
                    blank=False,
                    default = timezone.now())

    amount_added = models.DecimalField(
                    default = 0.00,
                    decimal_places = 2,
                    blank = False,
                    max_digits = 10)

    # def __str__(self):
    #     return self.user.username + ' added ' + str(self.amount_added)

#Allows user to update their total savings when they add money!
def update_user_saving(sender, instance, created, *args, **kwargs):
    if created:
        user = instance.user
        qs = UserIncome.objects.filter(user = user)
        current_user = UserIncome.objects.get(user= user)
        qs.update(current_savings = instance.amount_added + current_user.current_savings)


post_save.connect(update_user_saving, sender=UserPay)
