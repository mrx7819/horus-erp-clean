# Generated by Django 5.1.2 on 2024-12-11 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0007_alter_producto_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='img',
            field=models.ImageField(blank=True, upload_to='static/images/productos/'),
        ),
    ]
