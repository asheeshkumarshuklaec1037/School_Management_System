from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from school import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('adminclick',views.adminclick_view),
    path('teacherclick',views.teacherclick_view),
    path('studentclick',views.studentclick_view),

    path('login', views.CustomLoginView.as_view(template_name='school/login.html'), name='login'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='school/index.html'),name='logout'),

    # Admin related urls
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-update', views.update_admin_view,name='admin-update'),

    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),
    path('admin-view-class', views.admin_view_class_view,name='admin-view-class'),
    path('admin-view-student/<str:cl>', views.admin_view_student_view,name='admin-view-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),

    path('admin-attendance', views.admin_attendance_view,name='admin-attendance'),
    path('admin-view-attendance/<str:cl>', views.admin_view_attendance_view,name='admin-view-attendance'),

    path('admin-view-class-total-fee', views.admin_view_class_total_fee,name='admin-view-class-total-fee'),

    path('admin-notice', views.admin_notice_view,name='admin-notice'),
    path('delete-admin-notice/<int:pk>', views.delete_admin_notice_view,name='delete-admin-notice'),

    path('contactus', views.contact_us, name='contactus'),
    path('messages', views.message, name='messages'),    
    path('view-messages/<int:pk>', views.view_messages, name='view-messages'),
    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),

    path('add-display-message', views.add_display_message, name='add-display-message'),
    path('edit-display-message/<int:pk>', views.edit_display_message, name='edit-display-message'),
    path('delete-display-message/<int:pk>', views.delete_display_message,name='delete-display-message'),

    path('add-topper-list', views.add_topper_list, name='add-topper-list'),
    path('update-topper/<int:pk>', views.update_topper,name='update-topper'),
    path('delete-topper/<int:pk>', views.delete_topper,name='delete-topper'),

    path('display-address', views.display_address,name='display-address'),
    path('edit-display-address', views.edit_display_address,name='edit-display-address'),


    # Teacher related urls
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),

    path('teacher-attendance', views.teacher_attendance_view,name='teacher-attendance'),
    path('teacher-take-attendance', views.teacher_take_attendance_view,name='teacher-take-attendance'),
    path('teacher-view-attendance', views.teacher_view_attendance_view,name='teacher-view-attendance'),

    path('teacher-notice', views.teacher_notice_view,name='teacher-notice'),
    path('delete-teacher-notice/<int:pk>', views.delete_teacher_notice_view,name='delete-teacher-notice'),


    # Student related urls
    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),

    path('student-attendance', views.student_attendance_view,name='student-attendance'),

    # About developer url
    path('about-developer', views.about_developer,name='about-developer'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)