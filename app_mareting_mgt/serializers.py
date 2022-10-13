from pkg_resources import require
from .models import *
from app_product_details.serializers import *

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client_Company
        fields = '__all__'


        

class RegisterSerialzer1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class RegisterSerialzer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def save(self):
        ker=User(
                username = self.validated_data['username'],
                email = self.validated_data['email'],
                client_company=self.validated_data['client_company'],
                first_name = self.validated_data.get('first_name'),
                last_name=self.validated_data.get('last_name'),
                is_admin = self.validated_data.get('is_admin'),
                is_business = self.validated_data.get('is_business'),
                is_customer = self.validated_data.get('is_customer'),
            )

        password=self.validated_data['password']
        ker.set_password(password)
        ker.save()

        return ker

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['user_id'] = self.user.username
        data['company'] = self.user.client_company.company_name
        data['tenant_company'] = self.user.client_company.id
        data['email']=self.user.email
        data['is_admin']=self.user.is_admin
       
        return data


class Forgotpasswordserializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)

    class Meta:
        model =User
        fields=['username','password']

    def save(self):
        user=self.validated_data['username']
        password=self.validated_data['password']

        if User.objects.filter(username=user).exists():
            user1=User.objects.get(username=user)
            user1.set_password(password)
            user1.save()

            return user1

        else:
            raise serializers.ValidationError({'error':'please enter valid details'})

class Marketing_employee_sales_serializer1(serializers.ModelSerializer):
    tag = tag()

    class Meta:
        model = Marketing_employee_sales
        fields = '__all__'

class empl_details__serializer(serializers.ModelSerializer):
    class Meta:
        model = employee_details
        fields = '__all__'


class employee_address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = employee_address
        fields = '__all__'


class tag_serializer(serializers.ModelSerializer): 
    tag = tag()
    class Meta:
        model = tag
        fields = '__all__'

# class Sold_product_serializer1(serializers.ModelSerializer):
#     class Meta:
#         model = sold_products
#         fields = '__all__'

class Marketing_employee_sales_serializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing_employee_sales
        fields = '__all__'

class meeting_serializer(serializers.ModelSerializer): 
    class Meta:
        model = meeting
        fields = '__all__'

class tag_serializer(serializers.ModelSerializer):
    class Meta:
        model = tag
        fields = '__all__'

class empl_details__serializer1(serializers.ModelSerializer):
    Emp_no = employee_address_Serializer(many=True,read_only=True)
    rollno = Marketing_employee_sales_serializer(many=True,read_only=True)
    employee_name = Marketing_employee_sales_serializer(many=True,read_only=True)
    employee = meeting_serializer(many=True,read_only=True)
    emp_id_for_tag = tag_serializer(many=True,read_only=True)

    class Meta:
        model = employee_details
        fields = '__all__'


class Marketing_employee_sales_serializer1(serializers.ModelSerializer):
    sales_progress = meeting_serializer(many=True,read_only=True)

    class Meta:
        model = Marketing_employee_sales
        fields = '__all__'



