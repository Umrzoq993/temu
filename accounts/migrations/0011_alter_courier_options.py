# Generated by Django 5.1.6 on 2025-03-07 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_productimage_options_product_secret_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courier',
            options={'ordering': ['user__full_name'], 'verbose_name': 'Kuryer', 'verbose_name_plural': 'Kuryerlar'},
        ),
    ]
