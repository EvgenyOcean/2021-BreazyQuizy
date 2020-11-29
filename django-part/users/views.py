from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegisterSerializer


class UserCreate(APIView):
    """ 
    Creates the user. 
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = {"message": f"{user.username} was successfully created!"}
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    '''
    This view fires once user logs out
    '''
    # shouldn't it be IsAuthenticated?
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'refresh token is missing or incorrect'}, status=status.HTTP_400_BAD_REQUEST)