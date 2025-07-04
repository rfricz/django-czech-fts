# Generated by Django 5.2.1 on 2025-05-25 17:42

import django.contrib.postgres.indexes
import django.contrib.postgres.search
import fts.web.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('part_no', models.CharField(blank=True, max_length=100)),
                ('desc', models.TextField(blank=True)),
                ('search_vector', models.GeneratedField(db_persist=True, expression=django.contrib.postgres.search.CombinedSearchVector(django.contrib.postgres.search.SearchVector('name', config='cs', weight='A'), '||', django.contrib.postgres.search.SearchVector('desc', config='cs', weight='B'), django.contrib.postgres.search.SearchConfig('cs')), output_field=django.contrib.postgres.search.SearchVectorField())),
            ],
            options={
                'ordering': ['id'],
                'indexes': [django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.indexes.OpClass(fts.web.models.ImmutableUnaccent('name'), name='gin_trgm_ops'), name='name_idx'), django.contrib.postgres.indexes.GinIndex(fields=['part_no'], name='part_no_idx', opclasses=['gin_trgm_ops']), django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='search_vector_idx')],
            },
        ),
    ]
