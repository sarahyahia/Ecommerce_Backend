# Generated by Django 4.0.2 on 2022-02-10 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productchangeslog_date_added_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productchangeslog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='productchangeslog',
            name='status',
            field=models.CharField(choices=[('deleted', 'deleted'), ('updated', 'updated')], default='updated', max_length=255),
        ),
        migrations.AddField(
            model_name='productchangeslog',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
