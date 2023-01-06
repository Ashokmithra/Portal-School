from tkinter import N
import django
from django.contrib import admin

from .models import User, Teacher, Student, Note, Event
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Note)
admin.site.register(Event)
