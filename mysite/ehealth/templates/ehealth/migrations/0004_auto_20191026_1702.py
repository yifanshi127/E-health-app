# Generated by Django 2.2.5 on 2019-10-26 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehealth', '0003_auto_20191026_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthdata',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='healthdata', to='ehealth.Person'),
        ),
    ]