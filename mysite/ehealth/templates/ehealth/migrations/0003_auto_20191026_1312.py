# Generated by Django 2.2.5 on 2019-10-26 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehealth', '0002_auto_20191026_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthdata',
            name='pulse',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='spO2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='temperature',
            field=models.FloatField(null=True),
        ),
    ]
