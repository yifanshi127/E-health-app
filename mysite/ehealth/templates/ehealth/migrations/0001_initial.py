# Generated by Django 2.2.5 on 2019-10-25 14:35

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('personalheight', models.IntegerField()),
                ('personalweight', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_date', models.DateTimeField(auto_now_add=True)),
                ('originalEMG', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('frequencyEMG', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('mediafreq', models.IntegerField()),
                ('temperature', models.FloatField()),
                ('spO2', models.IntegerField()),
                ('pulse', models.IntegerField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ehealth.Person')),
            ],
        ),
    ]