from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = [
        "published_date", 
        "question_text"
    ]
    inlines = [ChoiceInline]
    list_display = (
        "question_text", 
        "published_date", 
        "was_published_recently"
    )
    list_filter = ["published_date"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
