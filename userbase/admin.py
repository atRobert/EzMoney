from django.contrib import admin
from .models import UserIncome, UserGoal, UserProfile, UserPay


class UserPayadmin(admin.ModelAdmin):
    list_display = ('user','amount_added','date_added',)


admin.site.register(UserIncome)
admin.site.register(UserGoal)
admin.site.register(UserProfile)
admin.site.register(UserPay, UserPayadmin)
