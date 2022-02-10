# Generated by Django 4.0.2 on 2022-02-10 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_alter_category_options_product_quantity_available_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductChangesLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('differences', models.JSONField()),
                ('old_product', models.JSONField()),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='editor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
