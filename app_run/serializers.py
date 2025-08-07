from rest_framework import serializers

from .models import Run, User, AthleteInfo, Challenge, Position, CollectibleItem



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
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    weight = serializers.IntegerField(min_value=1, max_value=899)

    class Meta:
        model = AthleteInfo
        fields = ['goals', 'weight', 'user_id']



class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'



class PositionSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=8, decimal_places=4, min_value=-90, max_value=90)
    longitude = serializers.DecimalField(max_digits=8, decimal_places=4,min_value=-180, max_value=180)
    run = serializers.PrimaryKeyRelatedField(queryset=Run.objects.all(), write_only=True)

    class Meta:
        model = Position
        fields = ['id', 'latitude', 'longitude', 'run']

    def validate_run(self, value):
        request = self.context.get('request')

        if request and request.method == 'POST':
            if value.status != Run.Status.IN_PROGRESS:
                raise serializers.ValidationError("Статус забега не 'В процессе'")
        return value



class CollectibleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectibleItem
        fields = ['id', 'name', 'uid', 'latitude', 'longitude', 'picture', 'value']



class UserCollectiblesSerializer(UserSerializer):
    items = CollectibleItemSerializer(many=True, read_only=True, default=[])

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ['items']