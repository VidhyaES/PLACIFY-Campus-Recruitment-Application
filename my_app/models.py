from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50)

class Company(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    contact=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    place=models.CharField(max_length=50)
    pin=models.CharField(max_length=50)
    post=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    status=models.CharField(max_length=50)

class Student(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    dob=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    pin=models.CharField(max_length=50)
    post=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    photo=models.CharField(max_length=1500)


class Post(models.Model):
    COMPANY=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='posted_company')
    job_vacancy=models.CharField(max_length=150)
    exam=models.CharField(max_length=150)
    status=models.CharField(max_length=150)

class Application(models.Model):
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)
    COMPANY=models.ForeignKey(Company,on_delete=models.CASCADE)
    status=models.CharField(max_length=150)

class Resume(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    photo = models.TextField(max_length=2000) 
    objective = models.TextField(max_length=1000) 
    skills = models.CharField(max_length=500)  
    experience = models.TextField(max_length=1000) 
    education = models.TextField(max_length=1000) 
    certifications = models.TextField(max_length=1000, blank=True)
    projects = models.TextField(max_length=1000, blank=True) 
    achievements = models.TextField(max_length=1000, blank=True) 
    languages = models.CharField(max_length=100, blank=True) 
    hobbies = models.CharField(max_length=300, blank=True) 
    portfolio_link = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)  
    github = models.URLField(max_length=200, blank=True)

class Complaint(models.Model):
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    complaint=models.CharField(max_length=700)
    reply=models.CharField(max_length=700)

class Feedback(models.Model):
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    feedback=models.CharField(max_length=700)
    

class Qualification(models.Model):
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    qualification=models.CharField(max_length=700)
    institution=models.CharField(max_length=150)
    course=models.CharField(max_length=150)
    batch=models.CharField(max_length=150)
    

class Certification(models.Model):
    STUDENT=models.ForeignKey(Student,on_delete=models.CASCADE)
    certification=models.CharField(max_length=700)
    issued_organisation=models.CharField(max_length=200)
    batch=models.CharField(max_length=150)

class Skill_development_category(models.Model):
    category=models.CharField(max_length=1700)
    description=models.CharField(max_length=200)

class Skill_development(models.Model):
    SKILL_DEVELOPMENT_CATEGORY=models.ForeignKey(Skill_development_category,on_delete=models.CASCADE)
    video=models.CharField(max_length=1500)
    details=models.CharField(max_length=1500)
    links=models.CharField(max_length=1500)
    

class Mock_test(models.Model):
    title = models.CharField(max_length=200)
    instruction = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
   

class Question(models.Model):
    MOCK_TEST=models.ForeignKey(Mock_test,on_delete=models.CASCADE)
    question=models.CharField(max_length=200)
    option_1=models.CharField(max_length=100)
    option_2=models.CharField(max_length=100)
    option_3=models.CharField(max_length=100)
    option_4=models.CharField(max_length=100)
    correct_answer=models.CharField(max_length=100)
    score=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class Student_answer(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    MOCK_TEST = models.ForeignKey(Mock_test, on_delete=models.CASCADE) 
    QUESTION = models.ForeignKey(Question, on_delete=models.CASCADE) 
    selected_answer = models.CharField(max_length=1500)
    is_correct = models.BooleanField(default=False) 
    time_taken = models.CharField(max_length=1500) 
    result = models.CharField(max_length=1500) 
    attempt = models.CharField(max_length=1500)



    
