from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('about/', views.about, name="about"),
    path('logout/', views.logout, name="logout"),
    path('adminhome/', views.adminhome, name="adminhome"),
    path('adminhome/register_students/', views.register_students, name="register_students"),
    path('success/',views.success_page, name="success_page"),
    path('adminhome/add_staff/', views.add_staff, name="add_staff"),
    path('staff_success_page/',views.staff_success_page, name="staff_success_page"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('student/', views.studenthome, name="student"),
    path('adminhome/add_books/', views.add_books, name='add_books'),
    path('book_success_page/',views.book_success_page, name="book_success_page"),
    path('adminhome/search_books/', views.search_books, name='search_books'),
    path('toggle_book_status/', views.toggle_book_status, name='toggle_book_status'),
    path('adminhome/book_list/', views.book_list, name="book_list"),

    path('adminhome/add_prgm/', views.add_program, name='add_program'),
    path('adminhome/add_dept/', views.add_department, name='add_department'),
    path('adminhome/add_des/', views.add_designation, name='add_designation'),
    path('program/', views.program_list, name='program_list'),
    path('department/', views.department_list, name='department_list'),
    path('designation/', views.designation_list, name='designation_list'),
    
    path('adminhome/search_students/', views.search_students, name='search_students'),


    # path('student/send_request/', views.send_request, name='send_request'),
    path('student/user_search_books/', views.user_search_books, name="user_search_books"),
    path('student/send_borrow_request/', views.send_borrow_request, name="send_borrow_request"),
    # path('adminhome/view_borrow_requests/', views.view_borrow_requests, name='view_borrow_requests'),
    # path('adminhome/approve_borrow_request/<int:request_id>/', views.approve_borrow_request, name='approve_borrow_request'),
    path('adminhome/borrow_requests/', views.admin_borrow_requests, name='admin_borrow_requests'),
    path('adminhome/approve_request/<int:request_id>/', views.admin_approve_request, name='admin_approve_request'),
    path('student/view_borrow_status/', views.view_borrow_status, name='view_borrow_status'),
    path('student/request_book/', views.request_book, name="request_book"),
    path('adminhome/admin_view_requests/', views.admin_view_requests, name="admin_view_requests"),
    path('adminhome/view_borrowed_books/', views.view_borrowed_books, name='view_borrowed_books'),

    path('student/new_book_request/', views.new_book_success, name="new_book_success"),
    path('adminhome/view_book_requests/', views.view_book_requests, name='view_book_requests'),
    path('adminhome/book_approve_request/<int:request_id>/', views.book_approve_request, name='book_approve_request'),
    path('adminhome/book_reject_request/<int:request_id>/', views.book_reject_request, name='book_reject_request'),
    path('adminhome/book_approval_success/', views.book_approval_success, name='book_approval_success'),
    path('adminhome/book_rejection_success/', views.book_rejection_success, name='book_rejection_success'),
    path('student/view_request_status/', views.view_request_status, name='view_request_status'),

    path('student/<int:student_id>/', views.student_borrowed_books, name='student_borrowed_books'),
    path('adminhome/view_borrowed_books_user', views.view_borrowed_books_user, name='view_borrowed_books_user'),
    
    path('student/save_review/', views.save_review, name='save_review'),
    path('adminhome/review_list/', views.review_list, name='review_list'),
    path('adminhome/return_book/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    path('student/pay_fine/<int:borrowed_book_id>/', views.pay_fine, name='pay_fine'),
    path('payment_handler/', views.payment_handler, name='payment_handler'),
    path('payment-success/<str:payment_id>/', views.payment_success, name='payment_success'),

    # path('student/recommend_books/', views.recommend_books, name='recommend_books'),
    
    path('student/fine_details/', views.view_fine_details, name='view_fine_details'),

    # path('adminhome/report/', views.borrowed_books_report, name='borrowed_books_report'),
    path('adminhome/generate-pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('student/view_borrowed_books_report/', views.view_borrowed_books_report, name='borrowed_books_report'),

]

  