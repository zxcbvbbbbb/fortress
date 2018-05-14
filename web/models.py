from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=32,unique=True)
    ip_addrss = models.GenericIPAddressField(unique=True)
    port = models.SmallIntegerField(default=22)
    idc = models.ForeignKey('IDC',on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.name


class HostGroup(models.Model):
    name = models.CharField(max_length=32,unique=True)
    # host = models.ManyToManyField('Host')
    host_to_remote_users = models.ManyToManyField('HostToRemoteUser')

    def __str__(self):
        return self.name

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_actvie = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        self.is_actvie = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    # password = models.CharField(_('password'), max_length=128,help_text=mark_safe('''<a href="password/">修改密码</a>'''))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = UserProfileManager()

    host_to_remote_users = models.ManyToManyField('HostToRemoteUser',blank=True,null=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email



class RemoteUser(models.Model):
    auth_type_choice = ((0,'ssh-password'),(1,'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choice,default=0)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64,blank=True,null=True)

    class Meta:
        unique_together = ('auth_type','username','password')

    def __str__(self):
        return '%s:%s' % (self.username,self.password)

class HostToRemoteUser(models.Model):
    host = models.ForeignKey('Host',on_delete=models.CASCADE)
    remote_users = models.ForeignKey('RemoteUser',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('host','remote_users')

    def __str__(self):
        return '%s %s' % (self.host,self.remote_users)

class IDC(models.Model):
    name = models.CharField(max_length=64,unique=True)

class AuditLog(models.Model):
    user = models.ForeignKey('UserProfile',verbose_name='堡垒机帐号',on_delete=models.CASCADE,blank=True,null=True)
    host_to_remote_user = models.ForeignKey('HostToRemoteUser',on_delete=models.CASCADE,blank=True,null=True)
    login_type_choices = ((0,'login'),(1,'cmd'),(2,'logout'))
    login_type = models.SmallIntegerField(choices=login_type_choices,default=0)
    content = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return '%s %s' % (self.host_to_remote_user,self.content)

class Task(models.Model):
    # task = models.CharField(max_length=32)
    task_type_choices = (('cmd','批量任务'),('file-transfer','文件传输'))
    task_type = models.CharField(choices=task_type_choices,max_length=64) #default='cmd'
    # name = models.CharField(max_length=32)
    content = models.CharField(max_length=255,verbose_name='任务内容')
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)


    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.task_type,self.content)

class TaskLogDetail(models.Model):
    task = models.ForeignKey('Task',on_delete=models.CASCADE)
    host_to_remote_user = models.ForeignKey('HostToRemoteUser',on_delete=models.CASCADE)
    result = models.TextField(verbose_name='任务执行结果') #max_length=32
    status_choices = ((0,'initialized'),(1,'success'),(2,'failed'),(3,'timeout')) #('0','success')
    status = models.SmallIntegerField(choices=status_choices,default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.task,self.result) # self.host_to_remote_user
