from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'subject', 'marks']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'marks': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name should only contain alphabetic characters and spaces.")
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data['subject'].strip()
        if not subject.replace(" ", "").isalpha():
            raise forms.ValidationError("Subject should only contain alphabetic characters and spaces.")
        if len(subject) < 2:
            raise forms.ValidationError("Subject must be at least 2 characters long.")
        return subject

    def clean_marks(self):
        marks = self.cleaned_data['marks']
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        subject = cleaned_data.get('subject')

        # Prevent duplicate name-subject pairs (already handled by unique_together, but form-level check avoids DB error)
        if name and subject:
            qs = Student.objects.filter(name__iexact=name.strip(), subject__iexact=subject.strip())
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
