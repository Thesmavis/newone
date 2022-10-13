from functools import partial
from django.shortcuts import render
from .models import User,Admin_New,Client_Company
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics, mixins, response, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, status, exceptions
from app_product_details.models import *





class Logout(APIView):
    def post(self, request):
     

        user_id = request.user.id           
        print(user_id,'lllllllllllll') 
        is_allowed_user = True
        token = request.auth

        h=BlackListedToken.objects.filter(user=request.user, token=token).exists()
        if h ==True:
       
            print('kkkkkkkkkkkkk')
            return Response("Logout")      
        else:
            m= BlackListedToken(user=request.user, token=token)
            m.save()
            print('ppppppppppppppppp')
            return Response("You have successfully logged out")


class view_companies(generics.ListCreateAPIView):
    queryset = Client_Company.objects.all()
    serializer_class = ClientSerializer   


class view_RegisteredUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerialzer   


class new_register_user(generics.GenericAPIView, mixins.ListModelMixin,APIView):

    serializer_class=RegisterSerialzer
    queryset = User.objects.all()

    def post(self,request):

        ser=RegisterSerialzer(data=request.data)
        data={}
        if ser.is_valid():

            g = ser.save()
            data['status']=True
            data['username']=g.username
            data['tenant_company']=g.client_company.company_name
            data['is_admin'] = g.is_admin
            data['is_business'] = g.is_business
            data['is_customer'] = g.is_customer
            data['user_id']=g.pk

        else:
            data['error']=ser.errors


        return Response(data)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class forgotpasswordview(APIView):
    permission_classes  = [IsAuthenticated]
    def post(self,request):

        ser=Forgotpasswordserializer(data=request.data)
        data={}
        if ser.is_valid(raise_exception=True):
            ser.save()
            data['status']=True
            data['forgotpassword']='success'
            return Response(data)

        return Response('oops!!!failed retry after some time')




class user_edit(APIView):
    permission_classes  = [IsAuthenticated]
    def get(self,request,id=None):

        if id:
            queryset=User.objects.get(id=id)
            serializer=RegisterSerialzer(queryset)

            return Response(serializer.data)
        else:
            queryset1=User.objects.all()
            serializer1=RegisterSerialzer(queryset1,many=True)

            return Response(serializer1.data)

    def patch(self,request,id=None):

        queryset=User.objects.get(id=id)
        serializer=RegisterSerialzer1(queryset,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response('Updated')
        else:
            return Response('Error')




class Client_Company_view(APIView):
    serializer_class=ClientSerializer
    queryset=Client_Company.objects.all()
    def get(self,request,id=None):

        if id:
            df=Client_Company.objects.get(id=id)
            ser=ClientSerializer(df)
            return Response(ser.data)

        else:
            a=Client_Company.objects.all()
            ser1=ClientSerializer(a,many=True)
            return Response(ser1.data)

    def post(self,request):

        ser3=ClientSerializer(data=request.data)
        if ser3.is_valid():
            ser3.save()
            return Response('success')

        else:
            return Response(ser3.errors)

    def patch(self,request,id=None):
        wer=Client_Company.objects.get(id=id)
        ser4=ClientSerializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')

    def delete(self,request,id=None):
        se=Client_Company.objects.get(id=id)
        se.delete()
        return Response('success')





class empl_details_view(generics.GenericAPIView, APIView):
    permission_classes  = [IsAuthenticated]
    serializer_class=empl_details__serializer
    queryset=employee_details.objects.all()
    def get(self,request,id=None):

        if id:
            df=employee_details.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
            ser=empl_details__serializer(df)
            return Response(ser.data)

        else:
            a=employee_details.objects.all()
            ser1=empl_details__serializer(a,many=True)
            return Response(ser1.data)

    def post(self,request):

        ser3=empl_details__serializer(data=request.data)
        if ser3.is_valid():
            ser3.save()
            return Response('success')

        else:
            return Response(ser3.errors)

    def patch(self, request,id=None):
        wer=employee_details.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        ser4=empl_details__serializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')

    def delete(self,request,id=None):
        se=employee_details.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        se.delete()
        return Response('success')





class employee_address_view(generics.GenericAPIView, APIView):
    serializer_class=employee_address_Serializer
    queryset=employee_address.objects.all()
    def get(self,request,id=None):

        if id:
            df=employee_address.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
            ser=employee_address_Serializer(df)
            return Response(ser.data)

        else:
            a=employee_address.objects.current_tenant(id = request.headers['tenant-id']).all()
            ser1=employee_address_Serializer(a,many=True)
            return Response(ser1.data)
            

    def post(self,request):
        result_data = {}
        print("------")
        employee = request.data[0]
        emp_add = request.data[1]
        print(request.headers,'kkkkkkkkkkkkkkkkkkkk')
        tenant_id = request.headers['tenant-id']
        employee = employee_details.objects.current_tenant(id = request.headers['tenant-id']).get(id = employee['emp_id'])
        for i in emp_add:
            mobile = i['mobile']
            email = i['email']
            adressline1 = i['adressline1']
            adressline2 = i['adressline2']
            adressline3 = i['adressline3']
            landmark = i['landmark']
            city = i['city']
            
        ser3=employee_address(tenant_id = tenant_id, Emp_rollno = employee, mobile =mobile, email =email , adressline1 = adressline1,adressline2  =adressline2, adressline3 =adressline3, landmark =landmark, city =city)
        ser3.save()
        result_data['status'] = True
        result_data['Post'] = "success."
        return Response(result_data)

        


    def patch(self, request,id=None):
        wer=employee_address.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        ser4=employee_address_Serializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')


    def delete(self,request,id=None):
        se=employee_address.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        se.delete()
        return Response('success')





class view_salesprogress(generics.ListCreateAPIView):
    permission_classes  = [IsAuthenticated]
    queryset = Marketing_employee_sales.objects.all()
    serializer_class = Marketing_employee_sales_serializer

    def get(self,request,id=None):
        if id:
            details = Marketing_employee_sales.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).get(id = id)
            serializer = Marketing_employee_sales_serializer(details)

            return Response(serializer.data)

        else:

            details = Marketing_employee_sales.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).all()
            serializer = Marketing_employee_sales_serializer(details, many = True)

            return Response(serializer.data)

    def delete(self,request,id=None):
        se=Marketing_employee_sales.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).get(id = id)  
        se.delete()
        return Response('success')

    def patch(self,request,id=None):
        wer=Marketing_employee_sales.objects.get(id=id)
        ser4=Marketing_employee_sales_serializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')



class tag_view(generics.GenericAPIView, APIView):
    permission_classes  = [IsAuthenticated]
    serializer_class=tag_serializer
    queryset=tag.objects.all()
    def get(self,request,id=None):

        if id:
            df=tag.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
            ser=tag_serializer(df)
            return Response(ser.data)

        else:
            a=tag.objects.all()
            ser1=tag_serializer(a,many=True)
            return Response(ser1.data)

    def post(self,request):
        ser3=tag_serializer(data=request.data)
        if ser3.is_valid():
            ser3.save()
            return Response('success')

        else:
            return Response(ser3.errors)

    def patch(self, request,id=None):
        wer=tag.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        ser4=tag_serializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')

    def delete(self,request,id=None):
        se=tag.objects.current_tenant(id = request.headers['tenant-id']).get(id = id)
        se.delete()
        return Response('success')




    
class view_meeting(generics.ListCreateAPIView):
    permission_classes  = [IsAuthenticated]
    queryset = meeting.objects.all()
    serializer_class = meeting_serializer

    def get(self,request,id=None):
        if id:
            df=meeting.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
            ser=meeting_serializer(df)
            return Response(ser.data)
        else:
            a=meeting.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).all()
            ser1=meeting_serializer(a,many=True)
            return Response(ser1.data)

    def post(self,request, id=None):
        tenant_id = request.headers['tenant-id']
        a=request.data
        print(a)
        employee = employee_details.objects.get(id=a['employee_id'])
        customer_id = Customer.objects.get(id=a['customer_id'])
        reasons = tag.objects.get(id=a['emp_reason_id'])
        meet=meeting(tenant_id = tenant_id, image=a['image'],employee=employee,registered_customers=customer_id, reasons = reasons)
        meet.save()
        return Response('success')      

    def delete(self,request,id=None):
        se=meeting.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
        se.delete()
        return Response('success')

    def patch(self,request,id=None):
        wer=meeting.objects.current_financialyear(id=request.headers['tenant-id'],stdate = request.headers['sdate'],lstdate=request.headers['ldate']).get(id=id)
        ser4=meeting_serializer(wer,data=request.data,partial=True)

        if ser4.is_valid():
            ser4.save()

            return Response('success')

        else:
            return Response('error')





