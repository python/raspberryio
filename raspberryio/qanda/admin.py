from django.contrib import admin

from raspberryio.qanda.models import Question, Answer


admin.site.register(Question)
admin.site.register(Answer)
