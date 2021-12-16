from rest_framework import serializers

from recipe.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("user", "name",)

    def create(self, validated_data):
        return super().create(validated_data)
