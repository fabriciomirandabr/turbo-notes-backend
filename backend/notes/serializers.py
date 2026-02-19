from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Note


class CategorySerializer(serializers.ModelSerializer):
    note_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "color", "note_count"]

    def get_note_count(self, obj):
        return obj.notes.count()


class NoteSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "category",
            "category_detail",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_category(self, value):
        if value and value.user != self.context["request"].user:
            raise serializers.ValidationError(
                "Category does not belong to you.",
                code="invalid_category",
            )
        return value


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists.",
                code="email_exists",
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        defaults = [
            ("Random Thoughts", "#EF9C66"),
            ("School", "#FCDC94"),
            ("Personal", "#78ABA8"),
        ]
        for name, color in defaults:
            Category.objects.create(name=name, color=color, user=user)
        return user
