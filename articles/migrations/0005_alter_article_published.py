# Generated by Django 3.2.5 on 2023-04-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_article_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.DateField(blank=True, null=True),
        ),
    ]