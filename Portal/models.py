from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    marks = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['name', 'subject']

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def clean(self):
        # Model-level validation (optional duplication of form checks)
        if not self.name.replace(" ", "").isalpha():
            raise ValidationError("Name should contain only alphabetic characters and spaces.")

        if not self.subject.replace(" ", "").isalpha():
            raise ValidationError("Subject should contain only alphabetic characters and spaces.")

        if not (0 <= self.marks <= 100):
            raise ValidationError("Marks should be between 0 and 100.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called before saving
        super().save(*args, **kwargs)