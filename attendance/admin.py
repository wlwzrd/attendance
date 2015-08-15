from django.contrib import admin
from attendance.models import *
# Register your models here.

class CourseSectionAdmin(admin.ModelAdmin):
    pass

class FilterStudentAdmin(admin.ModelAdmin):
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

    def queryset(self, request):
        #qs = super(StudentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return Student.objects.all()
        return Student.objects.filter(owner=request.user)
    
class StudentAdmin(FilterStudentAdmin):
    fields = ('code', 'first_name', 'middle_name', 'last_name', 'sex', 'email',)
    list_display = ('code', 'first_name', 'last_name')

admin.site.register(Period)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(AttendanceStatus)
admin.site.register(CourseSection,CourseSectionAdmin)
admin.site.register(StudentAttendance)
