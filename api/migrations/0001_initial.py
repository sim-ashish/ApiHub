# Generated by Django 4.2.20 on 2025-04-11 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_id', models.BigIntegerField(default=1)),
                ('name', models.CharField(max_length=100)),
                ('endpoint', models.SlugField(unique=True)),
                ('success_response', models.JSONField()),
                ('error_response', models.JSONField()),
                ('validations', models.JSONField(blank=True, default=dict)),
                ('public', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.BigIntegerField()),
                ('city', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FashionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=200)),
                ('food_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fooditem', to='api.foodcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_subscriber', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='posts/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='api.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='HitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('request_data', models.JSONField(blank=True, null=True)),
                ('returned_status', models.IntegerField()),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customapi')),
            ],
        ),
        migrations.CreateModel(
            name='FoodOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foodorder', to='api.fooditem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Cloth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloth_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cloth_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes', to='api.fashioncategory')),
                ('cloth_material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clothmaterial', to='api.clothmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='APIData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customapi')),
            ],
        ),
    ]
