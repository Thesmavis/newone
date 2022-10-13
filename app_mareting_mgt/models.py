from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.db.models.fields.related import ForeignKey
from pyexpat import model
import datetime
from app_product_details.models import *
# from taggit.managers import TaggableManager
# from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import gettext_lazy as _
# from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase



class Admin_New(models.Manager):
    def get_queryset(self,username):
        return super().get_queryset().filter(username=username , is_admin=True)



class Client_Company(models.Model):
    company_name = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=1024, null=True,blank=True)
    address_line1 = models.CharField(null=True, max_length=1024)
    address_line2 = models.CharField(null=True, max_length=1024)
    address_line3 = models.CharField(null=True, max_length=1024)
    office_email = models.CharField(null=True,blank=True, max_length=1024)
    office_pnone_no = models.CharField(max_length=1024, null=True,blank=True)
    gst_no = models.CharField(max_length=1024, null=True,blank=True)
    acc_no = models.CharField(max_length=1024, null=True,blank=True)
    ifsc_code = models.CharField(null=True,blank=True, max_length=1024)
    bank_name = models.CharField(null=True,blank=True, max_length=1024)
    branch_name = models.CharField(null=True,blank=True, max_length=1024)
    joined_date = models.DateField(auto_now=True)
    domain = models.CharField(max_length=1024,null=True,blank=True)

    def __str__(self):
        return (self.company_name)

class User(AbstractUser):
    client_company = models.ForeignKey(Client_Company, related_name='client_company', on_delete=models.CASCADE,null=True,blank=True)
    is_admin=models.BooleanField(default=False)
    is_business=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)
    objects = UserManager()
    city = models.CharField(null=True, max_length=1024)
    date_of_birth = models.DateField(null=True)
    admin_user = Admin_New()

    def __str__(self):
        return (self.username)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=1024)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class TenantQuerySet(models.QuerySet):
    def current_tenant(self, id):
        return self.filter(tenant_id=id)


class FinancialQuerySet(models.QuerySet):
    def current_financialyear(self, id, stdate, lstdate):
        cdatec = datetime.datetime.now()
        print(id, 'daaaat')
        if (stdate == '' or lstdate == ''):
            if(cdatec.month <= 3):
                current_finyear_start = datetime.datetime(cdatec.year-1, 4, 1)
                current_finyear_end = datetime.datetime(cdatec.year, 3, 31)
            else:
                current_finyear_start = datetime.datetime(cdatec.year, 4, 1)
                current_finyear_end = datetime.datetime(cdatec.year + 1, 3, 31)
        else:
            current_finyear_start = stdate
            current_finyear_end = lstdate

        return self.filter(financial_period__gte=current_finyear_start, financial_period__lte=current_finyear_end,tenant_id=id)



def idnumber():
    lastreportnumber = employee_details.objects.all().order_by('id').last()
    if not lastreportnumber :
        return 'EMPL0001'
    report_no = lastreportnumber .idnumber
    report_no_int = int(report_no.split('EMPL000')[-1])
    print(report_no )
    newreportno_int=report_no_int +1
    newreportno = 'EMPL000' + str(newreportno_int)
    return newreportno


class employee_details(models.Model):
    Emp_rollno=models.PositiveIntegerField(null=True, blank=True)
    tenant_id=models.PositiveIntegerField(null=True, blank=True)
    financial_period = models.DateField(auto_now=True, null=True, blank=True)
    objects = TenantQuerySet.as_manager()
    first_name = models.CharField(max_length=1024, null=True, blank=True)
    last_name = models.CharField(max_length=1024, null=True, blank=True)
    nationality=models.CharField(max_length=1024, null=True, blank=True)
    materialstatus=models.CharField(max_length=1024, null=True, blank=True)
    dob=models.DateField(null=True, blank=True)
    placeofbirth=models.CharField(max_length=1024, null=True, blank=True)
    gender = models.CharField(max_length=25, null=True, blank=True)
    bloodgroup=models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.first_name


class employee_address(models.Model):
    Emp_rollno=models.ForeignKey(employee_details,  related_name='Emp_no',null=True, blank=True, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=1024, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    adressline1=models.CharField(max_length=1024, null=True, blank=True)
    adressline2=models.CharField(max_length=1024, null=True, blank=True)
    adressline3=models.CharField(max_length=1024, null=True, blank=True)
    landmark = models.CharField(max_length=1024, null=True, blank=True)
    city=models.CharField(max_length=1024, null=True, blank=True)
    state=models.CharField(max_length=1024, null=True, blank=True)
    country = models.CharField(max_length=1024, null=True, blank=True)
    permantadress=models.BooleanField(default=False, null=True, blank=True)
    currentaddress=models.BooleanField(default=False, null=True, blank=True)
    financial_period = models.DateField(auto_now=True)
    tenant_id=models.PositiveIntegerField()
    objects = TenantQuerySet.as_manager()

    def __str__(self):
        return str (self.employedetails)



Performance_level = (('Good', 'Good'), ('Mid-Level', 'Mid-Level'), ('Low', 'Low'))


class tag(models.Model):
    tenant_id=models.PositiveIntegerField(null=True)
    financial_period = models.DateField(auto_now=True)
    objects = FinancialQuerySet.as_manager()
    employee_id = models.ForeignKey(employee_details, related_name='emp_id_for_tag', null=True, blank=True, on_delete=models.PROTECT)
    Reason=models.CharField(max_length=1200)

    def __str__(self):
        return str(self.Reason)



class Marketing_employee_sales(models.Model):
    tenant_id=models.PositiveIntegerField(null=True)
    rollno=models.ForeignKey(employee_details, related_name='rollno', null=True, blank=True, on_delete=models.PROTECT)
    sold_product_invoice_no=models.ForeignKey(bill_detials, related_name='sold_product_invoice', null=True, blank=True, on_delete=models.CASCADE)
    commession = models.FloatField(null=True, blank=True)
    Sales_Performance = models.CharField(max_length=250, choices=Performance_level)
    objects = FinancialQuerySet.as_manager()
    financial_period = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.Sales_Performance)

    
    

class meeting(models.Model):
    tenant_id=models.PositiveIntegerField(null=True)
    objects = FinancialQuerySet.as_manager()
    financial_period = models.DateField(auto_now=True)
    image = models.ImageField(null=True, blank=True)
    employee=models.ForeignKey(employee_details, null=True, blank=True, on_delete=models.CASCADE)
    registered_customers=models.ForeignKey(Customer,  related_name='registered_customer',null=True, blank=True, on_delete=models.PROTECT)
    reasons = models.ForeignKey(tag, related_name='tag', null=True, blank=True, on_delete=models.CASCADE) 

    def __str__(self):
        return str(self.employee)




    
    
    




