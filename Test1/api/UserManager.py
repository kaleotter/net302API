from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, title, first_name, last_name, address_1,  postcode, city, county,  mobile_no, password, address_2, address_3, phone_no, **extra_fields):
        
        if not email:
            raise ValueError("the given email must be set")
        
        if not address_1:
            raise ValueError("Address missing")
        
        if not postcode:
            raise ValueError("Postcode missing")
        
        if not city:
            raise ValueError("city missing")
        
        if not county:
            raise ValueError("county missing")
        
        if not mobile_no:
            raise ValueError("mobile number missing")
        
        email = self.normalize_email(email)
        user = self.model(email=email, title=title, first_name=first_name, last_name=last_name, address_1=address_1, address_2=address_2,
                           address_3=address_3,postcode=postcode, city=city,
                            county=county, phone_no=phone_no, mobile_no=mobile_no, 
                            **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, title, first_name, last_name, address_1,  postcode, city, county,  mobile_no, password=None, address_2=None, address_3=None, phone_no=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, title, first_name, last_name, address_1,  postcode, city, county,  mobile_no, password, address_2, address_3, phone_no, **extra_fields)
    
    def create_superuser(self, email, title, first_name, last_name, address_1, postcode, city, county,  mobile_no, password=None, address_2=None, address_3=None, phone_no=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError ("superuser must have is_superuser=True")
        
        return self._create_user(email, title, first_name, last_name, address_1, postcode, city, county,  mobile_no, password, address_2, address_3, phone_no,  **extra_fields)