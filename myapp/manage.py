#iska actual backend k kam hota h.. 
# models ko hadnle karna 
# nd unki req ko handhle karna

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required") 
        
        if 'email' in extra_fields:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Fixed: Correct method to set password
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(phone_number, password, **extra_fields)  # Fixed: Correct method call