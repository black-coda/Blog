from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
#creatiing base user manager

class UserManager(BaseUserManager):
    #creating methods for base user manager
    def create_user(self, email,full_name ,password=None, is_active = True, is_staff = False, is_admin = False):
        if not email and password and full_name:
            raise ValueError('Field required to be filled')
        user = self.model(
            email = self.normalize_email(email),
            full_name =full_name

        )
        user.set_password(password) #also for changing password
        user.staff      = is_staff
        user.admin      = is_admin
        user.active     = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff=True
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None ):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff=True,
            is_admin=True
        )
        user.save(using=self._db)
        return user

#Creating my own custom user
class User(AbstractBaseUser):
    email           =   models.EmailField(max_length=255, unique=True)
    full_name       =   models.CharField(max_length=234,blank=True, null=True)
    active          =   models.BooleanField(default=True)   #can user login
    staff           =   models.BooleanField(default=False)  #is user a staff
    admin           =   models.BooleanField(default=False)  #SUPERUSER
    timestamp       =   models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  =   'email' #change email to comp
    #email and password are required by default

    REQUIRED_FIELDS =   ['full_name',]  #A list of the field names that will be prompted for when creating a user via the createsuperuser management command.

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    objects = UserManager()



class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.author.email

class PublishedManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class AuthorPost(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    CATEGORY_CHOICES = (
    ('Personal blogs', 'Personal blogs'),
    ('Business/corporate blogs', 'Business/corporate blogs'),
    ('Personal brand/professional blogs', 'Personal brand/professional blogs'),
    ('Fashion blogs', 'Fashion blogs'),
    ('Lifestyle blogs', 'Lifestyle blogs'),
    ('Travel blogs', 'Travel blogs'),
    ('Food blogs', 'Food blogs'),
    ('Affiliate/review blogs', 'Affiliate/review blogs'),
    ('News blogs', 'News blogs'),
    ('Multimedia blogs', 'Multimedia blogs'),
    ('others', 'Others')
)

    title       =   models.CharField(max_length=400, unique=True,)
    author      =   models.ForeignKey(Author, on_delete=models.CASCADE)
    article     =   models.TextField(max_length=1500000)
    image_cover =   models.ImageField(upload_to='images_cover/', null = True, blank = True)
    category    =   models.CharField(max_length=700, choices=CATEGORY_CHOICES)
    publish     =   models.DateTimeField(default=timezone.now)
    created_on  =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True) 
    status      =   models.CharField(max_length=10, choices = STATUS_CHOICES, default = 'draft' )
    
    objects     =   models.Manager()
    published   =   PublishedManger()

    class Meta:
        ordering = ['-publish',]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:PostDetail", args=[self.pk])

class Comment(models.Model):
    post      = models.ForeignKey(AuthorPost, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=40)
    email     = models.EmailField(max_length=255)
    body      = models.TextField(max_length=1000)
    active    = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on',]

    def approvalOfComment(self):
        self.active = True
        self.save


def auther_user_create_signal(sender, instance, created, **kwargs):
    print(instance, sender, created)
    if created:
        Author.objects.create(author=instance)

post_save.connect(auther_user_create_signal, sender=User)