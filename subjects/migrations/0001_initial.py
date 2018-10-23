# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(editable=False)),
                ('parent', models.IntegerField(default=0, editable=False)),
                ('lft', models.IntegerField(verbose_name=b'left Traversal')),
                ('rght', models.IntegerField(verbose_name=b'right Traversal')),
                ('keywords', models.TextField()),
                ('notes', models.TextField()),
            ],
        ),
    ]
