from django.contrib import admin

from app.models import College, CollegeStream, Streams, Student

# Register your models here.
admin.site.register(College)
admin.site.register(Streams)
admin.site.register(Student)
admin.site.register(CollegeStream)
