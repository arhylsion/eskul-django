
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soal', models.TextField()),
                ('pilihan_a', models.CharField(max_length=255)),
                ('pilihan_b', models.CharField(max_length=255)),
                ('pilihan_c', models.CharField(max_length=255)),
                ('pilihan_d', models.CharField(max_length=255)),
                ('jawaban_benar', models.CharField(max_length=1)),
                ('point', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('can_retry', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
