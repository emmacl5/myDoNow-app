from django.contrib import admin
from .models import myTodo

# Register your models here.
class myTodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(myTodo, myTodoAdmin)
