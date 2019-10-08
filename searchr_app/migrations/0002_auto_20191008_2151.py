# Generated by Django 2.2.3 on 2019-10-08 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchr_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_result_title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('date_last_searched', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Search Result',
                'verbose_name_plural': 'Search Results',
            },
        ),
        migrations.RemoveField(
            model_name='keyword',
            name='phrase',
        ),
        migrations.AddField(
            model_name='keyword',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keyword',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Phrase',
        ),
        migrations.AddField(
            model_name='searchresult',
            name='keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searchr_app.Keyword'),
        ),
    ]
