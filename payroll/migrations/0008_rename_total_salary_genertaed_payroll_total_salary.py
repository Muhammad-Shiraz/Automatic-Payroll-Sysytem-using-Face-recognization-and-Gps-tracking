# Generated by Django 5.1.6 on 2025-04-07 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0007_rename_total_salary_payroll_total_salary_genertaed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payroll',
            old_name='total_salary_genertaed',
            new_name='total_salary',
        ),
    ]
