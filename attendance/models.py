from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Period(models.Model):
    """ Defines the useed surind academic year
    """
    name=models.CharField(max_length=6,help_text="Example 2015-1 or 2015-2")
    class Meta:
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
    def __unicode__(self):
        return self.name

class Student(models.Model):
    """ Represent a student that is enrolled in at least one course with 
    one teacher. Each student is used only for one teacher becasue the 
    attendance will be used for private teachers.
    """
    code = models.IntegerField()
    first_name = models.CharField(max_length=150, blank=False, null=False, verbose_name="First Name")
    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=150, blank=False, null=False, verbose_name="Last Name")
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True, null=True)
    email = models.EmailField(help_text="Email address")
    owner = models.ForeignKey(User)
    class Meta:
        verbose_name='Student'
        verbose_name_plural='Students'
    def __unicode__(self):
        if self.middle_name:
            return u"{0}, {1} {2}".format(self.last_name, self.first_name, self.middle_name)
        else:
            return u"{0}, {1}".format(self.last_name, self.first_name)

class Course(models.Model):
    """ Represent a normal course on the university/school catalogue 
    """
    name = models.CharField(max_length=255, null=False, unique=True)
    short_name = models.CharField(max_length=10, help_text="Could be a course code", null=False, unique=True)
    description = models.TextField(max_length=600)
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    def __unicode__(self):
        return u'Course: %s |Code %s'%(self.name,self.short_name)

class CourseSection(models.Model):
    """ Represent a section of a course. Each time there is at least one section in the year.
    """
    course = models.ForeignKey(Course)
    is_active = models.BooleanField(default=True)
    period = models.ForeignKey(Period, null=False)
    teacher = models.ForeignKey(User, null=False)
    enrollments = models.ManyToManyField('Student')
    class Meta:
        unique_together=(("course", "period", "teacher"),)
        verbose_name = 'Course Section'
        verbose_name_plural = 'Course Sections'
    def __unicode__(self):
        return u'Course: %s |Teacher %s %s'%(self.course.short_name, self.teacher.first_name, self.teacher.last_name)

class AttendanceStatus(models.Model):
    """ Define the commond status for the attendance
    """
    name = models.CharField(max_length=20, null=False)
    code = models.CharField(max_length=5, null=False)
    description = models.TextField(max_length=250, null=False, help_text="Explanation of the status")
    def __unicode__(self):
        return self.name

class StudentAttendance(models.Model):
    """ Define each call to the attendance for each student in each course.
    """
    student = models.ForeignKey(Student)
    course_section = models.ForeignKey(CourseSection)
    period = models.ForeignKey(Period)
    date = models.DateField(default=datetime.datetime.now)
    status = models.ForeignKey(AttendanceStatus)
    notes = models.CharField(max_length=250, blank=True)
    class Meta:
        unique_together = (("student", "date"),)
        ordering = ('-date', 'student',)
    def __unicode__(self):
        return unicode(self.student) + " " + unicode(self.date) + " " + unicode(self.status)
