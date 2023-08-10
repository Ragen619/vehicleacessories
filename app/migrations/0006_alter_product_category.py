# Generated by Django 4.2.2 on 2023-08-10 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('C', 'Car decoration'), ('CS', 'Car serviceparts'), ('M', 'Modifications'), ('BS', 'Bike serviceparts')], max_length=2),
        ),
    ]