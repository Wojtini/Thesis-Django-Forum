# Generated by Django 4.1 on 2022-10-23 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_rename_image_file_remove_entry_attached_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_file', models.ImageField(upload_to='')),
                ('thumbnail_file', models.ImageField(null=True, upload_to='')),
                ('mini_file', models.ImageField(null=True, upload_to='')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.user')),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.AlterField(
            model_name='entry',
            name='attached_files',
            field=models.ManyToManyField(to='forum.entryfile'),
        ),
    ]
