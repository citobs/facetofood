from django.contrib import admin

from mysite.models import Post, resultall,choice


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']



admin.site.register(Post)
admin.site.register(resultall)
admin.site.register(choice)
