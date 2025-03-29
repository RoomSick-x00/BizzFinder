#iska actual backend k kam hota h.. 
# models ko hadnle karna 
# nd unki req ko handhle karna

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    #taki method se baki ki model m nayi class bani h usko accept kare
    def create_user(self, phone_number, password = None, **extra_fields):
        if not phone_number:
           raise ValueError("Phone number is required") 
        
        #normalize the email.. chote letter m kar dena 
        extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set(password)
        user.save(using = self.db)
        
        return user
    
    #taki method se baki ki model m nayi class bani h usko accept kare
    def create_superuser(self, phone_number, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.user(phone_number, password, extra_fields)