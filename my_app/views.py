from django.shortcuts import render,HttpResponse
from .models import *
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request,'public/index.html')

def company_registration(request):
    if 'submit' in request.POST:
    
        username = request.POST['username']
        password = request.POST['password']
        company_name = request.POST['company_name']
        contact = request.POST['contact']
        email = request.POST['email']
        place = request.POST['place']
        pin = request.POST['pin']
        post = request.POST['post']
        city = request.POST['city']
        district = request.POST['district']

        q1=Login(username=username,password=password,user_type='pending')
        q1.save()

        q2=Company(name=company_name,contact=contact,email=email,place=place,pin=pin,post=post,city=city,district=district,status='pending',LOGIN_id=q1.pk)
        q2.save()
        return HttpResponse(f"<script>alert('company registration successfull.. please wait for admin approval');window.location='/login'</script>")
    return render(request,'public/company_registration.html')

def login(request):
    if 'submit' in request.POST:
    
        username = request.POST['username']
        password = request.POST['password']
        if Login.objects.filter(username=username,password=password).exists():
            res = Login.objects.get(username=username,password=password)
            request.session['login_id']=res.pk
            login_id=request.session['login_id']

            if res.user_type =='admin':
                request.session['log']="in"
                return HttpResponse(f"<script>alert('welcome Admin');window.location='/admin_home'</script>")

            elif res.user_type =='company':
                if Company.objects.filter(LOGIN_id=login_id).exists():
                    res2=Company.objects.get(LOGIN_id=login_id)
                    if res2:
                        request.session['log']="in"
                        request.session['company_id']=res2.pk
                        
                        return HttpResponse(f"<script>alert('welcome user');window.location='company_home'</script>")
                    else:
                        return HttpResponse(f"<script>alert('Invalid company ');window.location='login'</script>")
                else:
                        return HttpResponse(f"<script>alert('this company ID  does not exist');window.location='login'</script>")

            elif res.user_type =='student':
                if Student.objects.filter(LOGIN_id=login_id).exists():
                    res2=Student.objects.get(LOGIN_id=login_id)
                    if res2:
                        request.session['log']="in"
                        request.session['student_id']=res2.pk
                        
                        return HttpResponse(f"<script>alert('welcome user');window.location='student_home'</script>")
                    else:
                        return HttpResponse(f"<script>alert('Invalid  student ');window.location='login'</script>")
                else:
                        return HttpResponse(f"<script>alert('this student ID  does not exist');window.location='login'</script>")



            elif res.user_type =='blocked':
                return HttpResponse(f"<script>alert('you are blocked by admin');window.location='/login'</script>")

            elif res.user_type =='pending':
                return HttpResponse(f"<script>alert('you are not approved by admin....please wait for approval');window.location='/login'</script>")
            
            else:
                return HttpResponse(f"<script>alert('invalid user ');window.location='login'</script>")

        else:
            return HttpResponse(f"<script>alert('invalid username or password');window.location='login'</script>")
    return render(request,'public/login.html')



#admin.......#admin.......#admin.......#admin.......#admin.......#admin.......#admin.......#admin.......
def admin_home(request):
    return render(request,'admin/admin_home.html')

def admin_add_student(request):
    if 'submit' in request.POST:
    
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        email = request.POST['email']
        place = request.POST['place']
        pin = request.POST['pin']
        post = request.POST['post']
        city = request.POST['city']
        district = request.POST['district']
        photo=request.FILES['photo']

        date=datetime.now().time().strftime("%Y%m%d-%H%M%S")+".jpg"
        fs = FileSystemStorage() 
        fp = fs.save(date, photo)

        q1=Login(username=username,password=password,user_type='student')
        q1.save()

        q2=Student(first_name=first_name,last_name=last_name,dob=dob,gender=gender,contact=contact,email=email,place=place,pin=pin,post=post,city=city,district=district,photo=fs.url(fp),LOGIN_id=q1.pk)
        q2.save()
        return HttpResponse(f"<script>alert('student added successfully');window.location='/admin_view_student'</script>")
    return render(request,'admin/add_student.html')

def admin_view_student(request):
    data=Student.objects.all()
    return render(request,'admin/view_student.html',{'data':data})

def admin_edit_student(request, id):
    data = Student.objects.get(id=id)

    if 'submit' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        email = request.POST['email']
        place = request.POST['place']
        pin = request.POST['pin']
        post = request.POST['post']
        city = request.POST['city']
        district = request.POST['district']
        photo = request.FILES.get('photo') 

        data.first_name = first_name
        data.last_name = last_name
        data.dob = dob
        data.gender = gender
        data.contact = contact
        data.email=email
        data.place = place
        data.pin = pin
        data.post = post
        data.city = city
        data.district = district

        if photo:
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fp = fs.save(date, photo)
            data.photo = fs.url(fp) 


        data.save()


        return HttpResponse(f"<script>alert('Student edited successfully');window.location='/admin_view_student'</script>")

    return render(request, 'admin/edit_student.html', {'data': data})

def admin_delete_student(request,id):
    data=Student.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('Student deleted successfully');window.location='/admin_view_student'</script>")

def admin_view_company(request):
    data=Company.objects.all()
    return render(request,'admin/view_company.html',{'data':data})

def admin_approve_company(request,id):
    data1=Company.objects.get(LOGIN_id=id)
    data2=Login.objects.get(id=id)
    data1.status='approved'
    data1.save()

    data2.user_type='company'
    data2.save()
    return HttpResponse(f"<script>alert('company approved successfully');window.location='/admin_view_company'</script>")

def admin_reject_company(request,id):
    data1=Company.objects.get(LOGIN_id=id)
    data2=Login.objects.get(id=id)
    data1.status='rejected'
    data1.save()

    data2.user_type='rejected'
    data2.save()
    return HttpResponse(f"<script>alert('company rejected successfully');window.location='/admin_view_company'</script>")

def admin_view_company_post(request,id):
    data=Post.objects.filter(COMPANY_id=id)
    return render(request,'admin/view_company_post.html',{'data':data})

def admin_view_applicants(request,id):
    data=Application.objects.filter(POST_id=id)
    return render(request,'admin/view_applicants.html',{'data':data})

def admin_view_complaints(request):
    data=Complaint.objects.all()
    return render(request,'admin/view_complaints.html',{'data':data})

def admin_send_reply(request,id):
    data=Complaint.objects.get(id=id)
    if 'submit' in request.POST:
        reply=request.POST['reply']
        data.reply=reply
        data.save()
        return HttpResponse(f"<script>alert('reply send successfully');window.location='/admin_view_complaints'</script>")
    return render(request,'admin/send_reply.html',{'data':data})

def admin_view_mocktest(request):
    data=Mock_test.objects.all()    
    return render(request,'admin/view_mocktest.html',{'data':data})


def admin_add_mocktest(request):
    if 'submit' in request.POST:
        title=request.POST['title']
        instruction=request.POST['instruction']
        duration=request.POST['duration']

        q1=Mock_test(title=title,instruction=instruction,duration=duration)
        q1.save()
        return HttpResponse(f"<script>alert('new mock test added successfully');window.location='/admin_view_mocktest'</script>")

    return render(request,'admin/add_mocktest.html')

def admin_edit_mocktest(request,id):
    data=Mock_test.objects.get(id=id)
    if 'submit' in request.POST:
        title=request.POST['title']
        instruction=request.POST['instruction']
        duration=request.POST['duration']

        data.title=title
        data.instruction=instruction
        data.duration=duration
        data.save()

        return HttpResponse(f"<script>alert(' mock test edited successfully');window.location='/admin_view_mocktest'</script>")

    return render(request,'admin/edit_mocktest.html',{'data':data})

def admin_delete_mocktest(request,id):
    data=Mock_test.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert(' mock test deleted successfully');window.location='/admin_view_mocktest'</script>")

def admin_view_questions(request,mock_test_id):
    request.session['mock_test_id']=mock_test_id
    data=Question.objects.filter(MOCK_TEST_id=mock_test_id)    
    return render(request,'admin/view_questions.html',{'data':data})

def admin_add_questions(request):
    mock_test_id=request.session['mock_test_id']
    if 'submit' in request.POST:
        question=request.POST['question']   
        option_1=request.POST['option_1']   
        option_2=request.POST['option_2'] 
        option_3=request.POST['option_3'] 
        option_4=request.POST['option_4'] 
        correct_answer=request.POST['correct_answer']
        score=request.POST['score']

        q1=Question(question=question,option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,correct_answer=correct_answer,score=score,status='pending',MOCK_TEST_id=mock_test_id)
        q1.save()
        return HttpResponse(f"<script>alert(' new question added successfully');window.location='/admin_view_mocktest'</script>")
    return render(request,'admin/add_questions.html')

def admin_edit_questions(request,id):
    data=Question.objects.get(id=id)
    if 'submit' in request.POST:
        question=request.POST['question']   
        option_1=request.POST['option_1']   
        option_2=request.POST['option_2'] 
        option_3=request.POST['option_3'] 
        option_4=request.POST['option_4'] 
        correct_answer=request.POST['correct_answer']
        score=request.POST['score']

        data.question=question
        data.option_1=option_1
        data.option_2=option_2
        data.option_3=option_3
        data.option_4=option_4
        data.correct_answer=correct_answer
        data.score=score

        data.save()
        return HttpResponse(f"<script>alert('mock questions edit  successfully');window.location='/admin_view_mocktest'</script>")
        
    return render(request,'admin/edit_questions.html',{'data':data})

def admin_delete_questions(request,id):
    data=Question.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert(' mock questions deleted  successfully');window.location='/admin_view_mocktest'</script>")

def admin_view_skill_development_category(request):
    data=Skill_development_category.objects.all()    
    return render(request,'admin/view_skill_development_category.html',{'data':data})

def admin_add_skill_development_category(request):
    if 'submit' in request.POST:
        category=request.POST['category']  
        description=request.POST['description'] 

        q1=Skill_development_category(category=category,description=description)
        q1.save()
        return HttpResponse(f"<script>alert('new skill category added  successfully');window.location='/admin_view_skill_development_category'</script>")
    return render(request,'admin/add_skill_development_category.html')

def admin_edit_skill_development_category(request,id):
    data=Skill_development_category.objects.get(id=id)
    if 'submit' in request.POST:
        category=request.POST['category']  
        description=request.POST['description']

        data.category=category
        data.description=description
        data.save()
        
        return HttpResponse(f"<script>alert(' skill category edited  successfully');window.location='/admin_view_skill_development_category'</script>")
    return render(request,'admin/edit_skill_development_category.html',{'data':data})


def admin_delete_skill_development_category(request,id):
    data=Skill_development_category.objects.get(id=id)

    data.delete()
        
    return HttpResponse(f"<script>alert(' skill category deleted  successfully');window.location='/admin_view_skill_development_category'</script>")

def admin_view_skill_development(request,category_id):
    request.session['category_id']=category_id
    data=Skill_development.objects.filter(SKILL_DEVELOPMENT_CATEGORY_id=category_id)    
    return render(request,'admin/view_skill_development.html',{'data':data})

def admin_add_skill_development(request):
    category_id=request.session['category_id']
    if 'submit' in request.POST:
        video=request.FILES['video']  
        details=request.POST['details'] 
        links=request.POST['urls']

        date=datetime.now().time().strftime("%Y%m%d-%H%M%S")+".mp4"
        fs = FileSystemStorage() 
        fp = fs.save(date, video)

        q1=Skill_development(video=fs.url(fp),details=details,links=links,SKILL_DEVELOPMENT_CATEGORY_id=category_id)
        q1.save()
        return HttpResponse(f"<script>alert('new skill development program added  successfully');window.location='/admin_view_skill_development_category'</script>")
    return render(request,'admin/add_skill_development.html')

def admin_edit_skill_development(request,id):
    data=Skill_development.objects.get(id=id)
    if 'submit' in request.POST:
        video=request.FILES.get('video')
        details=request.POST['details'] 
        links=request.POST['urls']

        data.details=details
        data.links=links

        if video:
            date=datetime.now().time().strftime("%Y%m%d-%H%M%S")+".mp4"
            fs = FileSystemStorage() 
            fp = fs.save(date, video)
            data.video=fs.url(fp)

        data.save()
        
        return HttpResponse(f"<script>alert(' skill development program edited  successfully');window.location='/admin_view_skill_development_category'</script>")
    return render(request,'admin/edit_skill_development.html',{'data':data})


def admin_delete_skill_development(request,id):
    data=Skill_development.objects.get(id=id)

    data.delete()
        
    return HttpResponse(f"<script>alert(' skill development program deleted  successfully');window.location='/admin_view_skill_development_category'</script>")


#company.....#company.....#company.....#company.....#company.....#company.....#company.....#company.....
import json
def company_home(request):
    # Get company_id from the session
    company_id = request.session.get('company_id')

    # Fetch the count of posts for the company
    posts_count = Post.objects.filter(COMPANY__id=company_id).count()

    # Fetch the count of applicants for each post
    applicants_count = Application.objects.filter(COMPANY__id=company_id).count()

    context = {
        'posts_count': posts_count,
        'applicants_count': applicants_count,
    }

    return render(request, 'company/home.html', context)


def company_view_post(request):
    company_id=request.session['company_id']
    data = Post.objects.filter(COMPANY_id=company_id)
    return render(request,'company/view_post.html',{'data':data})
    
def company_add_post(request):
    company_id=request.session['company_id']
    if 'submit' in request.POST:
        job_vacancy = request.POST['job_vacancy']
        # description = request.POST['description']
        exam = request.POST['exam']
        
        q1=Post(job_vacancy=job_vacancy,exam=exam,status='active',COMPANY_id=company_id)
        q1.save()
        return HttpResponse(f"<script>alert('post added successfully');window.location='/company_view_post'</script>")
    return render(request,'company/add_post.html')

def company_edit_post(request,id):
    data=Post.objects.get(id=id)
    if 'submit' in request.POST:
        job_vacancy = request.POST['job_vacancy']
        exam = request.POST['exam']
        status = request.POST['status']

        data.job_vacancy=job_vacancy
        data.exam=exam
        # data.description = request.POST['description']
        data.status=status
        data.save()
        return HttpResponse(f"<script>alert('post updated successfully');window.location='/company_view_post'</script>")
    return render(request,'company/update_post.html',{'data':data})

def company_delete_post(request,id):
    data=Post.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert('post deleted successfully');window.location='/company_view_post'</script>")

def company_view_applications(request,id):
    request.session['post_id']=id
    data=Application.objects.filter(POST_id=id)
    return render(request,'company/view_applications.html',{'data':data})

def company_view_applicant_resume(request,id):
    try:
        data = Resume.objects.get(id=id)
        return render(request,'company/view_applicant_resume.html',{'data':data})
    except Resume.DoesNotExist:
        return HttpResponse("<script>alert('Resume not found');window.location='/company_view_post'</script>")

def company_approve_applicant(request,id):
    post_id=request.session['post_id']
    data2=Application.objects.get(id=id)
    data2.status='approved'
    data2.save()
    return HttpResponse(f"<script>alert('applicant approved successfully');window.location='/company_view_applications/{post_id}'</script>")

def company_reject_applicant(request,id):
    post_id=request.session['post_id']
    data2=Application.objects.get(id=id)
    data2.status='rejected'
    data2.save()
    return HttpResponse(f"<script>alert('applicant rejected successfully');window.location='/company_view_applications/{post_id}'</script>")

# def company_view_exam_result(request,id):
#     data=Student_answer.objects.filter(STUDENT_id=id)
#     total_score = 
#     return render(request,'company/view_result.html',{'data':data})
def company_view_exam_result(request, id):
    # Get the student answers for this student
    student_answers = Student_answer.objects.filter(STUDENT_id=id)
    
    total_score = 0
    
    # Loop through each answer the student gave
    for answer in student_answers:
        # Check if the answer is correct
        if answer.is_correct:
            # Add the score for the corresponding question to the total score
            total_score += answer.QUESTION.score
    
    # Render the result page with the student data and total score
    return render(request, 'company/view_result.html', {'data': student_answers, 'total_score': total_score})


def company_view_feedback(request):
    data=Feedback.objects.filter(id=request.session['company_id'])
    return render(request,'company/view_feedbacks.html',{'data':data})

def company_view_mocktest(request,id):
    request.session['post_id']=id
    print(request.session['post_id'],'===================')
    data=Mock_test.objects.filter(id=id) 
    return render(request,'company/view_mocktest.html',{'data':data})

def company_add_mocktest(request):
    post_id=request.session['post_id']
    print(post_id,'---------------------------')

    if 'submit' in request.POST:
        title=request.POST['title']
        instruction=request.POST['instruction']
        duration=request.POST['duration']

        q1=Mock_test(title=title,instruction=instruction,duration=duration,id=post_id)
        q1.save()
        del request.session['post_id']
        return HttpResponse(f"<script>alert('new mock test added successfully');window.location='/company_view_mocktest/{post_id}'</script>")

    return render(request,'company/add_mocktest.html')

def company_edit_mocktest(request,id):
    data=Mock_test.objects.get(id=id)
    if 'submit' in request.POST:
        title=request.POST['title']
        instruction=request.POST['instruction']
        duration=request.POST['duration']

        data.title=title
        data.instruction=instruction
        data.duration=duration
        data.save()

        return HttpResponse(f"<script>alert(' mock test edited successfully');window.location='/company_view_mocktest'</script>")

    return render(request,'company/edit_mocktest.html',{'data':data})

def company_delete_mocktest(request,id):
    data=Mock_test.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert(' mock test deleted successfully');window.location='/company_view_mocktest'</script>")

def company_view_questions(request,mock_test_id):
    request.session['mock_test_id']=mock_test_id
    data=Question.objects.filter(MOCK_TEST_id=mock_test_id)    
    return render(request,'company/view_questions.html',{'data':data})

def company_add_questions(request):
    mock_test_id=request.session['mock_test_id']
    if 'submit' in request.POST:
        question=request.POST['question']   
        option_1=request.POST['option_1']   
        option_2=request.POST['option_2'] 
        option_3=request.POST['option_3'] 
        option_4=request.POST['option_4'] 
        correct_answer=request.POST['correct_answer']
        

        q1=Question(question=question,option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,correct_answer=correct_answer,MOCK_TEST_id=mock_test_id)
        q1.save()
        return HttpResponse(f"<script>alert(' new question added successfully');window.location='/company_view_questions/{mock_test_id}'</script>")
    return render(request,'company/add_questions.html')

def company_edit_questions(request,id):
    mock_test_id=request.session['mock_test_id']
    data=Question.objects.get(id=id)
    if 'submit' in request.POST:
        question=request.POST['question']   
        option_1=request.POST['option_1']   
        option_2=request.POST['option_2'] 
        option_3=request.POST['option_3'] 
        option_4=request.POST['option_4'] 
        correct_answer=request.POST['correct_answer']
        

        data.question=question
        data.option_1=option_1
        data.option_2=option_2
        data.option_3=option_3
        data.option_4=option_4
        data.correct_answer=correct_answer

        data.save()
        return HttpResponse(f"<script>alert('mock questions edit  successfully');window.location='/company_view_questions/{mock_test_id}'</script>")
        
    return render(request,'company/edit_questions.html',{'data':data})

def company_delete_questions(request,id):
    mock_test_id=request.session['mock_test_id']
    data=Question.objects.get(id=id)
    data.delete()
    return HttpResponse(f"<script>alert(' mock questions deleted  successfully');window.location='/company_view_questions/{mock_test_id}'</script>")



def student_home(request):
    # Count the available mock tests
    mock_tests_count = Mock_test.objects.all().count()

    # Count the available jobs (posts)
    jobs_count = Post.objects.all().count()

    # Count the available programs (skill development categories)
    programs_count = Skill_development_category.objects.all().count()

    # Pass the counts to the template
    context = {
        'mock_tests_count': mock_tests_count,
        'jobs_count': jobs_count,
        'programs_count': programs_count,
    }

    return render(request, 'student/home.html', context)


def student_view_profile(request):
    data=Student.objects.get(id=request.session['student_id'])
    return render(request,'student/view_profile.html',{'data':data})

def student_update_profile(request):
    data=Student.objects.get(id=request.session['student_id'])

    if 'submit' in request.POST:
        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.dob = request.POST['dob']
        data.gender = request.POST['gender']
        data.contact = request.POST['contact']
        data.email = request.POST['email']
        data.place = request.POST['place']
        data.pin = request.POST['pin']
        data.post = request.POST['post']
        data.city = request.POST['city']
        data.district = request.POST['district']
        photo=request.FILES.get('photo')

        if photo:
            date=datetime.now().time().strftime("%Y%m%d-%H%M%S")+".jpg"
            fs = FileSystemStorage() 
            fp = fs.save(date, photo)
            image_url = f"/static/media/{fp}"

            data.photo=fs.url(fp)
            data.save()
        data.save()

        
        return HttpResponse(f"<script>alert('profile updated');window.location='/student_view_profile'</script>")
    return render(request,'student/update_profile.html',{'data':data})

# def student_view_post(request):
#     data=Post.objects.filter(status='active')
#     return render(request,'student/view_post.html',{'data':data})
def student_view_post(request):
    student_id = request.session['student_id']
    
    # Fetch job posts
    job_posts = Post.objects.all()

    # Create a dictionary to hold whether a student has already applied for a job
    applications = Application.objects.filter(STUDENT_id=student_id)
    applied_posts = {application.POST_id for application in applications}

    return render(request, 'student/view_post.html', {
        'data': job_posts,
        'applied_posts': applied_posts
    })

# def student_apply_post(request,id):
#     q0=Post.objects.get(id=id)

#     q1=Application(status='applied',POST_id=id,COMPANY_id=q0.COMPANY_id,STUDENT_id=request.session['student_id'])
#     q1.save()
#     return HttpResponse(f"<script>alert('applied for this job post successfully');window.location='/student_view_post'</script>")


# def student_submit_resume_and_apply(request,id):
#     if 'submit' in request.POST:

#         # Retrieving form data
#         objective = request.POST['objective']
#         skills = request.POST['skills']
#         experience = request.POST['experience']
#         education = request.POST['education']
#         certifications = request.POST.get('certifications', '')
#         projects = request.POST.get('projects', '')
#         achievements = request.POST.get('achievements', '')
#         languages = request.POST.get('languages', '')
#         hobbies = request.POST.get('hobbies', '')
#         portfolio_link = request.POST.get('portfolio_link', '')
#         linkedin = request.POST.get('linkedin', '')
#         github = request.POST.get('github', '')
#         photo  = request.FILES.get('photo', '')
#         date   = datetime.now().time().strftime("%Y%m%d-%H%M%S")+".jpg"
#         fs = FileSystemStorage()
#         fp = fs.save(date, photo)
#         image_url = f"/static/media/{fp}"

#         resume = Resume(STUDENT_id=request.session['student_id'],objective=objective,skills=skills,experience=experience,education=education,certifications=certifications,projects=projects,achievements=achievements,languages=languages,hobbies=hobbies,portfolio_link=portfolio_link,linkedin=linkedin,github=github,photo=image_url)
#         resume.save()

#         q0=Post.objects.get(id=id)

#         q1=Application(status='applied',POST_id=id,COMPANY_id=q0.COMPANY_id,STUDENT_id=request.session['student_id'],RESUME_id=resume.pk)
#         q1.save()

#         return HttpResponse(f"<script>alert('Resume submitted and job applied successfully');window.location='/student_view_post'</script>")

#     return render(request, 'student/resume.html')

def student_submit_resume_and_apply(request, id):
    student_id = request.session['student_id']
    
    # Check if the student has already applied for this job post
    existing_application = Application.objects.filter(STUDENT_id=student_id, POST_id=id).exists()
    
    if existing_application:
        return HttpResponse(f"<script>alert('You have already applied for this job.');window.location='/student_view_post'</script>")
    
    if 'submit' in request.POST:
        # Retrieving form data
        objective = request.POST['objective']
        skills = request.POST['skills']
        experience = request.POST['experience']
        education = request.POST['education']
        certifications = request.POST.get('certifications', '')
        projects = request.POST.get('projects', '')
        achievements = request.POST.get('achievements', '')
        languages = request.POST.get('languages', '')
        hobbies = request.POST.get('hobbies', '')
        portfolio_link = request.POST.get('portfolio_link', '')
        linkedin = request.POST.get('linkedin', '')
        github = request.POST.get('github', '')
        photo = request.FILES.get('photo', '')
        date = datetime.now().time().strftime("%Y%m%d-%H%M%S") + ".jpg"
        fs = FileSystemStorage()
        fp = fs.save(date, photo)
        image_url = f"/static/media/{fp}"

        resume = Resume(STUDENT_id=student_id, objective=objective, skills=skills, experience=experience, education=education, certifications=certifications, projects=projects, achievements=achievements, languages=languages, hobbies=hobbies, portfolio_link=portfolio_link, linkedin=linkedin, github=github, photo=image_url)
        resume.save()

        post = Post.objects.get(id=id)

        application = Application(status='applied', POST_id=id, COMPANY_id=post.COMPANY_id, STUDENT_id=student_id,id=resume.pk)
        application.save()

        return HttpResponse(f"<script>alert('Resume submitted and job applied successfully');window.location='/student_view_post'</script>")

    return render(request, 'student/resume.html')



# def student_view_application(request):
#     data=Application.objects.filter(STUDENT_id=request.session['student_id'])
#     return render(request,'student/view_applications.html',{'data':data})
def student_view_application(request):
    data = Application.objects.filter(STUDENT_id=request.session['student_id'])
    for application in data:
        # Check if the student has already attempted the exam for this job post
        mock_test_attempted = Student_answer.objects.filter(
            STUDENT_id=request.session['student_id'],
            MOCK_TEST__id=application.POST.id
        ).exists()

        # Add this info to each application
        application.mock_test_attempted = mock_test_attempted

    return render(request, 'student/view_applications.html', {'data': data})


def student_send_complaint(request):
    data=Complaint.objects.filter(STUDENT_id=request.session['student_id'])
    if 'submit' in request.POST:
        complaint=request.POST['complaint']

        q=Complaint(complaint=complaint,reply='pending',STUDENT_id=request.session['student_id'])
        q.save()
        return HttpResponse(f"<script>alert('complaint submited successfully..please wait for admin to reply');window.location='/student_send_complaint'</script>")
    return render(request,'student/send_complaint.html',{'data':data})

def student_view_my_complaints(request):
    data=Complaint.objects.filter(STUDENT_id=request.session['student_id'])
    return render(request,'student/view_my_complaints.html',{'data':data})
# def student_view_mock_tests(request):
#     mock_tests = Mock_test.objects.all()
#     return render(request, 'student/view_mock_tests.html', {'mock_tests': mock_tests})

# from django.shortcuts import get_object_or_404

# from django.shortcuts import get_object_or_404

# def student_attend_mock_test(request, test_id):
#     mock_test = get_object_or_404(Mock_test, id=test_id)
#     questions = Question.objects.filter(MOCK_TEST=mock_test)
    
#     if request.method == "POST":
#         # Process the answers from the form submission
#         total_score = 0
#         for question in questions:
#             selected_answer = request.POST.get(f'question_{question.id}')
#             is_correct = selected_answer == question.correct_answer
#             result = "Correct" if is_correct else "Incorrect"
#             time_taken = int(request.POST.get(f'time_taken_{question.id}', 0))
            
#             # Save the student's answer
#             Student_answer.objects.create(
#                 STUDENT_id=request.session['student_id'],  
#                 MOCK_TEST_id=mock_test.id,
#                 QUESTION_id=question.id,
#                 selected_answer=selected_answer,
#                 is_correct=is_correct,
#                 time_taken=time_taken,
#                 result=result
#             )
#             if is_correct:
#                 total_score += question.score
        
#         # Save the final score or result
#         return render(request, 'student/view_result.html', {'score': total_score, 'mock_test': mock_test})

#     return render(request, 'student/attend_mock_test.html', {'mock_test': mock_test, 'questions': questions})


# def student_view_result(request, test_id):
#     student_answers = Student_answer.objects.filter(STUDENT_id=request.session['student_id'], MOCK_TEST_id=test_id)
#     total_score = sum([answer.score for answer in student_answers if answer.is_correct])
    
#     return render(request, 'student/view_result.html', {
#         'student_answers': student_answers,
#         'total_score': total_score
#     })
# views.py





# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse


# # Display mock tests to the student
# def student_view_mock_tests(request):
#     mock_tests = Mock_test.objects.all()
#     return render(request, 'student/view_mock_tests.html', {'mock_tests': mock_tests})

# # Attend mock test (first question)
# # def student_attend_mock_test(request, test_id, question_id):
# #     mock_test = get_object_or_404(Mock_test, id=test_id)
# #     question = get_object_or_404(Question, MOCK_TEST=mock_test, id=question_id)
    
# #     # Find the next question
# #     next_question = Question.objects.filter(MOCK_TEST=mock_test, id__gt=question.id).first()
# #     next_question_id = next_question.id if next_question else None
    
# #     if request.method == "POST":
# #         selected_answer = request.POST.get('answer')
# #         is_correct = selected_answer == question.correct_answer
# #         Student_answer.objects.create(
# #             STUDENT_id=request.session['student_id'],  
# #             MOCK_TEST_id=test_id,
# #             QUESTION_id=question.id,
# #             selected_answer=selected_answer,
# #             is_correct=is_correct,
# #             time_taken=60,  # Assume a fixed time for this example
# #             result="Correct" if is_correct else "Incorrect"
# #         )

# #         # Check if there is a next question
# #         if next_question:
# #             return redirect(f'/student_attend_mock_test/{test_id}/{next_question.id}')
# #         else:
# #             return redirect('/test_results')  # Redirect to results page when test is complete
    
# #     return render(request, 'student/attend_mock_test.html', {
# #         'mock_test': mock_test, 
# #         'question': question,
# #         'next_question_id': next_question_id
# #     })

# from django.shortcuts import render
# from django.utils import timezone
# import uuid

# def student_attend_mock_test(request, test_id, question_id):
#     mock_test = get_object_or_404(Mock_test, id=test_id)
#     question = get_object_or_404(Question, MOCK_TEST_id=mock_test, id=question_id)
    
#     # Set a unique test attempt ID in the session (e.g., using a timestamp or UUID)
#     if 'current_attempt' not in request.session:
#         request.session['current_attempt'] = uuid.uuid4().hex  # or use timezone.now() for timestamp-based ID
    
#     # Find the next question
#     next_question = Question.objects.filter(MOCK_TEST_id=mock_test, id__gt=question.id).first()
#     next_question_id = next_question.id if next_question else None
    
#     if request.method == "POST":
#         selected_answer = request.POST.get('answer')
#         is_correct = selected_answer == question.correct_answer
#         Student_answer.objects.create(
#             STUDENT_id=request.session['student_id'],  
#             MOCK_TEST_id=test_id,
#             QUESTION_id=question.id,
#             selected_answer=selected_answer,
#             is_correct=is_correct,
#             time_taken=60,  # Assume a fixed time for this example
#             result="Correct" if is_correct else "Incorrect",
#             attempt=request.session['current_attempt']  # Store the current attempt
#         )

#         # Check if there is a next question
#         if next_question:
#             return redirect(f'/student_attend_mock_test/{test_id}/{next_question.id}')
#         else:
#             return redirect('/test_results')  # Redirect to results page when test is complete
    
#     return render(request, 'student/attend_mock_test.html', {
#         'mock_test': mock_test, 
#         'question': question,
#         'next_question_id': next_question_id
#     })

# # Submit the answer and get the next question or show result
# def submit_answer(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         question_id = data.get('question_id')
#         answer = data.get('answer')
#         mock_test_id = data.get('mock_test_id')

#         question = Question.objects.get(id=question_id)
#         is_correct = answer == question.correct_answer

#         Student_answer.objects.create(
#             STUDENT_id=request.session['student_id'],
#             MOCK_TEST_id=mock_test_id,
#             QUESTION_id=question.id,
#             selected_answer=answer,
#             is_correct=is_correct,
#             time_taken=60,  # You could dynamically capture the time
#             result="Correct" if is_correct else "Incorrect"
#         )

#         next_question = Question.objects.filter(MOCK_TEST_id=mock_test_id, id__gt=question.id).first()
#         if next_question:
#             return JsonResponse({'next_question': next_question.id})
#         else:
#             return JsonResponse({'next_question': None})

#     return JsonResponse({'error': 'Invalid request'}, status=400)

# # View test results
# # def student_view_result(request, test_id):
# #     student_answers = Student_answer.objects.filter(STUDENT_id=request.session['student_id'], MOCK_TEST_id=test_id)
    
# #     # Calculate total score by accessing the score from the associated Question model
# #     total_score = sum([answer.QUESTION.score for answer in student_answers if answer.is_correct])
    
# #     return render(request, 'student/view_result.html', {
# #         'student_answers': student_answers,
# #         'total_score': total_score
# #     })

# from django.shortcuts import render
# from .models import Student_answer

# # def student_view_result(request, test_id):
# #     # Fetch the current session or attempt ID (for example, using request.session['test_attempt_id'])
# #     current_attempt = request.session.get('current_attempt')  # This could be a timestamp or a unique session ID

# #     # Filter the student's answers by the current attempt and mock test
# #     student_answers = Student_answer.objects.filter(
# #         STUDENT_id=request.session['student_id'], 
# #         MOCK_TEST_id=test_id,
# #         attempt=current_attempt
# #     )
    
# #     # Calculate total score by accessing the score from the associated Question model
# #     total_score = sum([answer.QUESTION.score for answer in student_answers if answer.is_correct])
    
# #     return render(request, 'student/view_result.html', {
# #         'student_answers': student_answers,
# #         'total_score': total_score
# #     })
# from uuid import UUID

# def student_view_result(request, test_id):
#     current_attempt = request.session.get('current_attempt')
    
#     # Convert the session value to a UUID object
#     if current_attempt:
#         current_attempt = UUID(current_attempt)  # Convert string to UUID
#         print(current_attempt,'uuuuuiiiiii')
    
#     # Now fetch the answers using the UUID value
#     student_answers = Student_answer.objects.filter(
#         STUDENT_id=request.session['student_id'],
#         MOCK_TEST_id=test_id,
#         attempt=current_attempt
#     )
    
#     total_score = sum([answer.QUESTION.score for answer in student_answers if answer.is_correct])
    
#     return render(request, 'student/view_result.html', {
#         'student_answers': student_answers,
#         'total_score': total_score
#     })



#new day
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from uuid import uuid4
from .models import Mock_test, Question, Student_answer

# Display mock tests to the student
def student_view_mock_tests(request,id):
    mock_tests = Mock_test.objects.filter(id=id)
    return render(request, 'student/view_mock_tests.html', {'mock_tests': mock_tests})

def student_view_mocktest_all(request):
    data=Mock_test.objects.all()    
    return render(request,'student/view_mock_tests.html', {'mock_tests': data})

# Attend mock test (first question)
def student_attend_mock_test(request, test_id, question_id):
    mock_test = get_object_or_404(Mock_test, id=test_id)
    question = get_object_or_404(Question, MOCK_TEST=mock_test, id=question_id)
    
    # Set a unique test attempt ID in the session (using UUID as string)
    if 'current_attempt' not in request.session:
        request.session['current_attempt'] = uuid4().hex  # Store UUID as string
    
    # Find the next question
    next_question = Question.objects.filter(MOCK_TEST=mock_test, id__gt=question.id).first()
    next_question_id = next_question.id if next_question else None
    
    if request.method == "POST":
        selected_answer = request.POST.get('answer')
        is_correct = selected_answer == question.correct_answer
        Student_answer.objects.create(
            STUDENT_id=request.session['student_id'],  
            MOCK_TEST_id=test_id,
            QUESTION_id=question.id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_taken=60,  # Assume a fixed time for this example
            result="Correct" if is_correct else "Incorrect",
            attempt=request.session['current_attempt']  # Store the current attempt as string
        )

        # Check if there is a next question
        if next_question:
            return redirect(f'/student_attend_mock_test/{test_id}/{next_question.id}')
        else:
            # Delete the session key after the test is complete
            # del request.session['current_attempt']
            return redirect('/test_results')  # Redirect to results page when test is complete
    
    return render(request, 'student/attend_mock_test.html', {
        'mock_test': mock_test, 
        'question': question,
        'next_question_id': next_question_id
    })


# Submit the answer and get the next question or show result
def submit_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer = data.get('answer')
        mock_test_id = data.get('mock_test_id')

        question = Question.objects.get(id=question_id)
        is_correct = answer == question.correct_answer

        Student_answer.objects.create(
            STUDENT_id=request.session['student_id'],
            MOCK_TEST_id=mock_test_id,
            QUESTION_id=question.id,
            selected_answer=answer,
            is_correct=is_correct,
            time_taken=60,  # You could dynamically capture the time
            result="Correct" if is_correct else "Incorrect",
            attempt=request.session['current_attempt']  # Store the current attempt as string
        )

        next_question = Question.objects.filter(MOCK_TEST_id=mock_test_id, id__gt=question.id).first()
        if next_question:
            return JsonResponse({'next_question': next_question.id})
        else:
            # del request.session['current_attempt']
            return JsonResponse({'next_question': None})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# View test results
def student_view_result(request, test_id):
    # Fetch the current attempt before it's deleted (if it's still available)
    current_attempt = request.session.get('current_attempt')
    print(current_attempt, 'attempt id in view result')

    if not current_attempt:
        # If the session key has been deleted, handle accordingly (maybe redirect or show a message)
        return redirect('/some_error_page')  # Or show some message
    
    # Use the string value directly (no need to convert to UUID)
    student_answers = Student_answer.objects.filter(
        STUDENT_id=request.session['student_id'],
        MOCK_TEST_id=test_id,
        attempt=current_attempt  # Match by string (no UUID conversion needed)
    )
    
    # Calculate total score
    total_score = sum([answer.QUESTION.score for answer in student_answers if answer.is_correct])
    del request.session['current_attempt']
    
    return render(request, 'student/view_result.html', {
        'student_answers': student_answers,
        'total_score': total_score
    })


from django.shortcuts import render
from .models import Skill_development_category, Skill_development

def student_view_skill_development(request):
    # Get all categories
    categories = Skill_development_category.objects.all()
    
    # Create a list to store categories with their videos
    category_videos = []

    for category in categories:
        # Get videos under each category
        videos = Skill_development.objects.filter(SKILL_DEVELOPMENT_CATEGORY=category)
        category_videos.append({
            'category': category,
            'videos': videos
        })
    
    # Pass data to the template
    return render(request, 'student/view_skill_development.html', {'category_videos': category_videos})

# def student_view_company(request):
#     data=Company.objects.all()
#     return render(request,'student/view_company.html',{'data':data})

def student_view_company(request):
    # search_query = request.GET.get('search', '')  # Get the search query from the GET parameters
    
    if 'submit' in request.POST:
        search_query=request.POST['search']
        # Filter companies by name, case-insensitive, partial match
        data = Company.objects.filter(name__icontains=search_query)
    else:
        # Return all companies if no search query is provided
        data = Company.objects.all()

    return render(request, 'student/view_company.html', {'data': data})


def student_view_company_post(request,id):
    request.session['company_post_id']=id
    data=Post.objects.filter(COMPANY_id=id,status='active')
    return render(request,'student/view_company_post.html',{'data':data})

def student_send_feedback(request,id):

    if 'submit' in request.POST:
        feedback=request.POST['feedback']
        q=Feedback(feedback=feedback,STUDENT_id=request.session['student_id'],COMPANY_id=id)
        q.save()
        return HttpResponse(f"<script>alert('Feedback send successfully');window.location='/student_view_company'</script>")
    return render(request,'student/send_feedback.html')

import json
from .knn import predict



# def student_view_notification(request):
#     data=Job_notification.objects.all()
#     return render(request,'student/view_notification.html',{'data':data})





def read_pdf(file_path):
    import PyPDF2
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        txt=""
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text()
            txt=txt+text+" "
        return txt

# def upldcv(request):

#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         # from interview.sampleee import pdf_reader
#     cv=request.FILES['file']
#     fn=FileSystemStorage()
#     fs=fn.save(cv.name,cv)
#     lid=request.POST['lid']
#     save_image_path = r'C:\Users\hp\Desktop\mock final\mockinterview\mockinterview\media/' + fs
#     resume_text = read_pdf(save_image_path)
#     # print(resume_text)
#     # print("****************8")
#     res = predict(resume_text)
#     print(res,"=================================================")
#     # ob=upload()
#     ob.USER=Student.objects.get(LOGIN__id=lid)
#     ob.cv=fs
#     ob.date=datetime.today()
#     ob.save()
#     data = {"task": "success","res":res}
#     r = json.dumps(data)
#     return HttpResponse(r)


def student_upload_resume(request):

    if 'submit' in request.POST:
        cv=request.FILES['resume']
        fn=FileSystemStorage()
        fs=fn.save(cv.name,cv)
        lid=request.session['login_id']
        save_image_path = r'C:\Users\HP\Downloads\placify-demo\placify-demo\static\media/' + fs
        resume_text = read_pdf(save_image_path)
        print(resume_text)
        print("****************8")

        res = predict(resume_text)
        print(res,"=================================================")
        jj = Post.objects.none()  # Start with an empty QuerySet
        for r in res:
            jj = jj | Post.objects.filter(job_vacancy__icontains=r)
        
        return render(request,'student/upload_resume.html',{"data":res,"data2":jj})
    return render(request,'student/upload_resume.html')


