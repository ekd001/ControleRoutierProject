from rest_framework import serializers
from  .models import User,Agent,ControlPoint,ControlPointByAgent,Criteria,RoadControl,CriteriaByControl,Almond
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only' : True}

        }

        #test register ok ,so on hash le password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class  AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ControlPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPoint
        fields = ['id', 'name', 'ville', 'quartier', 'agents']

class ControlPointByAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPointByAgent
        fields = ['id', 'agent', 'control_point', 'state']

class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['id', 'name', 'description']

class RoadControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadControl
        fields = "__all__"

class CriteriaByControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaByControl
        fields = ['id', 'criteria', 'road_control']#, 'state', 'almond'

class AlmondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almond
        fields = ['id','road_control','montant', 'paid']
