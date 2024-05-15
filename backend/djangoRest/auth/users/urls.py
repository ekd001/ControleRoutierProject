
from django.urls import path
from .views import (RegisterView, LoginView, UserView, LogoutView, AgentView,AgentRegisterView,ControlPointAPIView,
                    ControlPointByAgentAPIView,CriteriaAPIView,RoadControlAPIView,
                    CriteriaByControlAPIView,AlmondAPIView)

urlpatterns = [

    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('agentregister', AgentRegisterView.as_view()),
    path('agent', AgentView.as_view()),
    path('controlpoint', ControlPointAPIView.as_view()),
    path('controlpoint/<int:pk>', ControlPointAPIView.as_view()),
    path('controlpointbyagent', ControlPointByAgentAPIView.as_view()),
    path('controlpointbyagent/<int:pk>', ControlPointByAgentAPIView.as_view()),
    path('criteria', CriteriaAPIView.as_view()),
    path('criteria/<int:pk>', CriteriaAPIView.as_view()),
    path('roadcontrol', RoadControlAPIView.as_view()),
    path('roadcontrol/<int:pk>', RoadControlAPIView.as_view()),
    path('criteriabycontrol', CriteriaByControlAPIView.as_view()),
    path('criteriabycontrol/<int:pk>', CriteriaByControlAPIView.as_view()),
    path('almond', AlmondAPIView.as_view()),
    path('almond/<int:pk>', AlmondAPIView.as_view()),



]
#model>serializer>view>urls....test api.....