from rest_framework import serializers

from .models import Run, User, AthleteInfo


class UserSerializerForRun(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = UserSerializerForRun(read_only=True, source='athlete')

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type', 'runs_finished']

    def get_type(self, obj):
        if obj.is_staff: return 'coach'
        else: return 'athlete'


class AthleteInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    weight = serializers.IntegerField()

    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight', 'user_id']

    def validate_weight(self, weight):
        if weight <= 0 or weight >= 900:
            raise serializers.ValidationError("Это поле должно содержать от 0 до 900 кг.")
        return weight

    def get_user_id(self, obj):
        return obj.user.id