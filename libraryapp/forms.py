from django import forms
from .models import Student, BookRequest, Department, Program, Designation



class ProgramForm(forms.ModelForm):
    d_id = forms.ModelChoiceField(queryset=Department.objects.all(), label='Department')  # Assuming you want to choose from existing departments

    class Meta:
        model = Program
        fields = ['program', 'd_id']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department']

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['designation']

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']


class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['title', 'author', 'publisher', 'category', 'edition', 'no_of_copies']

class StudentSearchForm(forms.Form):
    search_term = forms.CharField(label='Search by ID or Name', max_length=100, required=True)