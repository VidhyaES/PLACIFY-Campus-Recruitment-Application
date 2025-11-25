from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('company_registration',views.company_registration),
    path('login',views.login),
    path('admin_home',views.admin_home),
    path('admin_view_student',views.admin_view_student),
    path('admin_add_student',views.admin_add_student),
    path('admin_edit_student/<int:id>',views.admin_edit_student),
    path('admin_delete_student/<int:id>',views.admin_delete_student),

    path('admin_view_company_post/<int:id>',views.admin_view_company_post),
    path('admin_view_company',views.admin_view_company),
    path('admin_approve_company/<int:id>',views.admin_approve_company),
    path('admin_reject_company/<int:id>',views.admin_reject_company),
    path('admin_view_applicants/<int:id>',views.admin_view_applicants),

    path('admin_view_complaints',views.admin_view_complaints),
    path('admin_send_reply/<int:id>',views.admin_send_reply),

    path('admin_view_mocktest',views.admin_view_mocktest),
    path('admin_add_mocktest',views.admin_add_mocktest),
    path('admin_edit_mocktest/<int:id>',views.admin_edit_mocktest),
    path('admin_delete_mocktest/<int:id>',views.admin_delete_mocktest),

    path('admin_view_questions/<int:mock_test_id>',views.admin_view_questions),
    path('admin_add_questions',views.admin_add_questions),
    path('admin_edit_questions/<int:id>',views.admin_edit_questions),
    path('admin_delete_questions/<int:id>',views.admin_delete_questions),

    path('admin_view_skill_development_category',views.admin_view_skill_development_category),
    path('admin_add_skill_development_category',views.admin_add_skill_development_category),
    path('admin_edit_skill_development_category/<int:id>',views.admin_edit_skill_development_category),
    path('admin_delete_skill_development_category/<int:id>',views.admin_delete_skill_development_category),
    
    path('admin_view_skill_development/<int:category_id>',views.admin_view_skill_development),
    path('admin_add_skill_development',views.admin_add_skill_development),
    path('admin_edit_skill_development/<int:id>',views.admin_edit_skill_development),
    path('admin_delete_skill_development/<int:id>',views.admin_delete_skill_development),



#company.....

path('company_home',views.company_home),

    path('company_view_post',views.company_view_post),
    path('company_add_post',views.company_add_post),
    path('company_edit_post/<int:id>',views.company_edit_post),
    path('company_delete_post/<int:id>',views.company_delete_post),
    path('view_resume/<int:id>', views.company_view_applicant_resume, name='view_resume'),
    path('company_view_applications/<int:id>',views.company_view_applications),
    path('company_view_applicant_resume/<int:id>',views.company_view_applicant_resume),
    path('company_approve_applicant/<int:id>',views.company_approve_applicant),
    path('company_reject_applicant/<int:id>',views.company_reject_applicant),

    path('company_view_exam_result/<int:id>',views.company_view_exam_result),

    path('company_view_feedback',views.company_view_feedback),

    path('company_view_mocktest/<int:id>',views.company_view_mocktest),
    path('company_add_mocktest',views.company_add_mocktest),
    path('company_edit_mocktest/<int:id>',views.company_edit_mocktest),
    path('company_delete_mocktest/<int:id>',views.company_delete_mocktest),

    path('company_view_questions/<int:mock_test_id>',views.company_view_questions),
    path('company_add_questions',views.company_add_questions),
    path('company_edit_questions/<int:id>',views.company_edit_questions),
    path('company_delete_questions/<int:id>',views.company_delete_questions),


    
#student......
    path('student_home',views.student_home),
    path('student_view_profile',views.student_view_profile),
    path('student_update_profile',views.student_update_profile),

    path('student_view_post',views.student_view_post),
    path('student_submit_resume_and_apply/<int:id>',views.student_submit_resume_and_apply),

    path('student_view_application',views.student_view_application),

    path('student_send_complaint',views.student_send_complaint),
    path('student_view_my_complaints',views.student_view_my_complaints),

    path('student_view_mock_tests/<int:id>', views.student_view_mock_tests),
    path('student_attend_mock_test/<int:test_id>/<question_id>', views.student_attend_mock_test),
    path('submit_answer', views.submit_answer),
    path('student_view_result/<int:test_id>', views.student_view_result),

    path('student_view_skill_development',views.student_view_skill_development),
    
    path('student_view_company',views.student_view_company),
    path('student_view_company_post/<int:id>',views.student_view_company_post),
    path('student_send_feedback/<int:id>',views.student_send_feedback),
    # path('student_view_notification',views.student_view_notification),
    path('student_upload_resume',views.student_upload_resume),
    path('student_view_mocktests_all',views.student_view_mocktest_all),

   
    


]