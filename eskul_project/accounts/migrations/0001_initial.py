
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nis', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('nama', models.CharField(max_length=100)),
                ('kelas', models.CharField(max_length=20)),
                ('has_eskul', models.BooleanField(default=False)),
            ],
        ),
    ]
