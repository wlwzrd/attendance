# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20150814_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursesection',
            options={'verbose_name': 'Course Section', 'verbose_name_plural': 'Course Sections'},
        ),
        migrations.AlterField(
            model_name='course',
            name='short_name',
            field=models.CharField(help_text=b'Could be a course code', unique=True, max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='coursesection',
            unique_together=set([('course', 'period', 'teacher')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentattendance',
            unique_together=set([('student', 'date')]),
        ),
    ]
