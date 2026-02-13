from rest_framework import serializers
from .models import Character
from .defaults import default_epicorpg_sheet

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "id",
            "player_name",
            "system_key",
            "xp_total",
            "portrait_url",
            "sheet_data",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "system_key", "created_at", "updated_at"]

    def validate_sheet_data(self, value):
        # Se vier vazio/nulo, preenche com ficha padrão
        if value is None or value == {}:
            return default_epicorpg_sheet()
        if not isinstance(value, dict):
            raise serializers.ValidationError("sheet_data precisa ser um objeto JSON.")
        return value

    def create(self, validated_data):
        # Garante ficha padrão quando não mandar sheet_data
        if "sheet_data" not in validated_data:
            validated_data["sheet_data"] = default_epicorpg_sheet()
        return super().create(validated_data)