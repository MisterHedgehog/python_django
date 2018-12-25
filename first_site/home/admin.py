from django.contrib import admin

from .models import Choice, Question, Product, Ingredient, Unit


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Вопрос',           {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class IngredientInLine(admin.TabularInline):
    model = Ingredient
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Характеристики',  {'fields': ['name', 'weight', 'color', 'storage_time'], 'classes':['collapse']})
    ]
    inlines = [IngredientInLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Unit)
