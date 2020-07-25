from django.contrib import admin

from .models import TimePeriod, ClientCard, CalendarDate

admin.site.register(TimePeriod)
admin.site.register(ClientCard)
admin.site.register(CalendarDate)
