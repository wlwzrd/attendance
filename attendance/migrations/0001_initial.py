# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=5)),
                ('description', models.TextField(help_text=b'Explanation of the status', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('short_name', models.CharField(help_text=b'Could be a course code', max_length=10)),
                ('description', models.TextField(max_length=600)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='attendance.Course')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Example 2015-1 or 2015-2', max_length=6)),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.IntegerField(max_length=20)),
                ('first_name', models.CharField(max_length=150, verbose_name=b'First Name')),
                ('middle_name', models.CharField(max_length=150, null=True, verbose_name=b'Middle Name', blank=True)),
                ('last_name', models.CharField(max_length=150, verbose_name=b'Last Name')),
                ('sex', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('email', models.EmailField(help_text=b'Email address', max_length=254)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('notes', models.CharField(max_length=250, blank=True)),
                ('course_section', models.ForeignKey(to='attendance.CourseSection')),
                ('period', models.ForeignKey(to='attendance.Period')),
                ('status', models.ForeignKey(to='attendance.AttendanceStatus')),
                ('student', models.ForeignKey(to='attendance.Student')),
            ],
            options={
                'ordering': ('-date', 'student'),
            },
        ),
        migrations.AddField(
            model_name='coursesection',
            name='enrollments',
            field=models.ManyToManyField(to='attendance.Student'),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='period',
            field=models.ForeignKey(to='attendance.Period'),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='teacher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='studentattendance',
            unique_together=set([('student', 'date', 'status')]),
        ),
    ]
