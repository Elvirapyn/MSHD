# Generated by Django 3.0.3 on 2020-05-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommDisaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.CharField(max_length=20)),
                ('Date', models.CharField(max_length=32)),
                ('Location', models.CharField(max_length=32)),
                ('Type', models.CharField(max_length=32)),
                ('SequenceNumber', models.CharField(max_length=32)),
                ('Grade', models.IntegerField()),
                ('Picture', models.CharField(max_length=200)),
                ('Note', models.CharField(max_length=32)),
                ('ReportingUnit', models.CharField(max_length=32)),
            ],
        ),
    ]
