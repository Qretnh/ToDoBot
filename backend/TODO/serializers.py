from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from .models import Category, Tag, Task, User
from .services.ids import generate_id


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("user",)


class TaskSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField(write_only=True, required=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
    )
    category = CategorySerializer(read_only=True)

    user = serializers.StringRelatedField(read_only=True)

    due_time = serializers.TimeField(required=False, allow_null=True)

    tags = TagSerializer(many=True, read_only=True)  # для вывода
    tag_ids = serializers.PrimaryKeyRelatedField(  # для записи
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="tags",
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "telegram_id",
            "user",
            "category_id",
            "category",
            "title",
            "description",
            "created_at",
            "due_date",
            "due_time",
            "is_completed",
            "tags",
            "tag_ids",
        ]
        read_only_fields = ("user", "id", "created_at", "tags")

    def create(self, validated_data):
        telegram_id = validated_data.pop("telegram_id")

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        validated_data.pop("user_id", None)

        tags = validated_data.pop("tags", [])

        due_time = validated_data.get("due_time")
        if not due_time:
            from datetime import time

            validated_data["due_time"] = time(hour=18, minute=0)

        task = Task.objects.create(user=user, **validated_data)

        if tags:
            task.tags.set(tags)

        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)

        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    telegram_id = serializers.CharField()
    username = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ["telegram_id", "username"]
