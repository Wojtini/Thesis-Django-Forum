# Generated by Django 4.1 on 2022-11-02 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_remove_entry_attached_files_remove_entry_replied_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='entry',
            name='popularity',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='which_cycle',
        ),
        migrations.AddField(
            model_name='entry',
            name='calculated_popularity',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CycleThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popularity', models.FloatField()),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.cycle')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.thread')),
            ],
        ),
    ]
