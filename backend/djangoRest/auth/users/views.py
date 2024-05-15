import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Agent, ControlPoint, ControlPointByAgent, Criteria, RoadControl, CriteriaByControl, Almond
from .serializers import UserSerializer, AgentSerializer, ControlPointSerializer, ControlPointByAgentSerializer, CriteriaSerializer, RoadControlSerializer, CriteriaByControlSerializer, AlmondSerializer
from jwt import encode
from rest_framework_jwt.settings import api_settings
from rest_framework import status

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(serializer.data)

class AgentRegisterView(APIView):
    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(serializer.data)

class LoginView(APIView):
    def post(self, request): #now on va ajouter le loginview aux urls
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first() or Agent.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found !')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password !')

        #return Response(user)

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),  # 1hour ...... How long the token will last
            'iat' : datetime.datetime.utcnow() #date de creation du token
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not authenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class AgentView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not authenticated!')

        user = Agent.objects.filter(id=payload['id']).first()
        serializer = AgentSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ControlPointAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            control_point = ControlPoint.objects.get(pk=pk)
            serializer = ControlPointSerializer(control_point)
        else:
            control_points = ControlPoint.objects.all()
            serializer = ControlPointSerializer(control_points, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ControlPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        control_point = ControlPoint.objects.get(pk=pk)
        control_point.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ControlPointByAgentAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            control_point_by_agent = ControlPointByAgent.objects.get(pk=pk)
            serializer = ControlPointByAgentSerializer(control_point_by_agent)
        else:
            control_points_by_agent = ControlPointByAgent.objects.all()
            serializer = ControlPointByAgentSerializer(control_points_by_agent, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ControlPointByAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        control_point_by_agent = ControlPointByAgent.objects.get(pk=pk)
        serializer = ControlPointByAgentSerializer(control_point_by_agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        control_point_by_agent = ControlPointByAgent.objects.get(pk=pk)
        control_point_by_agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CriteriaAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            criteria = Criteria.objects.get(pk=pk)
            serializer = CriteriaSerializer(criteria)
        else:
            criterias = Criteria.objects.all()
            serializer = CriteriaSerializer(criterias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CriteriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        criteria = Criteria.objects.get(pk=pk)
        serializer = CriteriaSerializer(criteria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        criteria = Criteria.objects.get(pk=pk)
        criteria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoadControlAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            road_control = RoadControl.objects.get(pk=pk)
            serializer = RoadControlSerializer(road_control)
        else:
            road_controls = RoadControl.objects.all()
            serializer = RoadControlSerializer(road_controls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoadControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        road_control = RoadControl.objects.get(pk=pk)
        serializer = RoadControlSerializer(road_control, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        road_control = RoadControl.objects.get(pk=pk)
        road_control.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CriteriaByControlAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            criteria_by_control = CriteriaByControl.objects.get(pk=pk)
            serializer = CriteriaByControlSerializer(criteria_by_control)
        else:
            criterias_by_control = CriteriaByControl.objects.all()
            serializer = CriteriaByControlSerializer(criterias_by_control, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CriteriaByControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        criteria_by_control = CriteriaByControl.objects.get(pk=pk)
        serializer = CriteriaByControlSerializer(criteria_by_control, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        criteria_by_control = CriteriaByControl.objects.get(pk=pk)
        criteria_by_control.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlmondAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            almond = Almond.objects.get(pk=pk)
            serializer = AlmondSerializer(almond)
        else:
            almonds = Almond.objects.all()
            serializer = AlmondSerializer(almonds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlmondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        almond = Almond.objects.get(pk=pk)
        serializer = AlmondSerializer(almond, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        almond = Almond.objects.get(pk=pk)
        almond.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
