from django.contrib import admin

from raspberryio.qanda.models import Question, Answer

class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_filter = ('question',)

admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
