from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200)
    city = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    district=models.TextField(null=True, blank=True)
 
    def __str__(self):
        return (self.user.username)
        
class Education(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    grade = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return (self.college_name)


class Experience(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return (self.company_name)


class Skill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20)

    def __str__(self):
        return (self.skill_name)


class Certificate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    certificate_url = models.URLField(blank=True)

    def __str__(self):
        return (self.certificate_name)


class Achievement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    achievement_date = models.DateField()

    def __str__(self):
        return (self.title)

class Interest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest_name = models.CharField(max_length=100)
    interest_level = models.CharField(max_length=20)

    def __str__(self):
        return (self.interest_name) 

class Language(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language_name = models.CharField(max_length=100)
    language_level = models.CharField(max_length=20)

    def __str__(self):
        return (self.language_name) 

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return (self.user.username)

class Job(models.Model):
    company = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100)

    def __str__(self):
        return (self.job_title)