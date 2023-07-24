from django.forms import ModelForm
from .models import myTodo

class myTodoForm(ModelForm):
    class Meta:
        model = myTodo
        fields = ['title', 'memo', 'important']
