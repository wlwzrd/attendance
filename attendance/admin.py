from django.contrib import admin
from attendance.models import *
from django.contrib.auth.models import User
# Register your models here.

class CourseSectionAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):
    fields = ('code', 'first_name', 'middle_name', 'last_name', 'sex', 'email',)
    list_display = ('code', 'first_name', 'last_name')
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.owner:
            instance.owner = user
        instance.save()
        form.save_m2m()
        return instance

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Select the user who is currently logged in.
        """
        if db_field.name == 'owner':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        """If the user is a superuser, then display all students. 
        Otherwise only show their own enrolled students.
        """
        qs = super(StudentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

class CourseSectionAdmin(admin.ModelAdmin):
    fields = ("course","is_active", "period", "enrollments",)
    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.owner:
            instance.teacher = user
        instance.save()
        form.save_m2m()
        return instance

    def get_queryser(self, request):
        """If the user is a superuser, then display all course sections.
        Otherwise only show their own coursesection.
        """
        qs = super(CourseSectionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user)

admin.site.register(Period)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(AttendanceStatus)
admin.site.register(CourseSection,CourseSectionAdmin)
admin.site.register(StudentAttendance)
