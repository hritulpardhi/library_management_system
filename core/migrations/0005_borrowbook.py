# Generated by Django 5.0.6 on 2024-07-03 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_books_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('borrowed_at', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_book', to='core.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_user', to='core.books')),
            ],
            options={
                'db_table': 'borrow_book',
                'managed': True,
            },
        ),
    ]
