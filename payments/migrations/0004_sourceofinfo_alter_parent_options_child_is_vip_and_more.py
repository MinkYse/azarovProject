# Generated by Django 5.1 on 2024-09-01 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_remove_parent_child_child_parents_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceOfInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='parent',
            options={'verbose_name': 'Родитель', 'verbose_name_plural': 'Родители'},
        ),
        migrations.AddField(
            model_name='child',
            name='is_vip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='child',
            name='source_of_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payments.sourceofinfo'),
        ),
    ]
