# Generated by Django 4.2.12 on 2024-06-04 20:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('medicAI', '0004_hospital_visit_er_doctor_hospital_visit_symptoms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medical_Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('test_name', models.CharField(max_length=200)),
                ('test_notes', models.CharField(blank=True, max_length=500, null=True)),
                ('hostpital_visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicAI.hospital_visit')),
            ],
        ),
    ]
