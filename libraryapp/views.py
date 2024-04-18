from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookRequestForm, ProgramForm, DesignationForm, DepartmentForm
from .models import ReturnedBook, Student, Staff, Book, BorrowRequest, BorrowedBook, BookRequest, Program, Department, Designation, Payment
from django.db.models import Q
# from .forms import StudentRegistrationForm
import csv
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta, timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def index(request):
    borrowed_books = BorrowedBook.objects.all()

    # Iterate through each borrowed book and calculate fine
    for borrowed_book in borrowed_books:
        borrowed_book.calculate_fine()
    return render(request,'index.html')  

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def register_students(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if csv_file:
            print(f"Received CSV file: {csv_file.name}")

            # Process CSV file
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

            for row in csv_data:
                name, email = row
                password = get_random_string(length=12)

                user = User.objects.create_user(username=name, email=email, password=password)

                student = Student(name=name, email=email, password=password, user=user)  
                try:
                    student.save()
                    print(f"Saved student: {student.name}")
                except Exception as e:
                    print(f"Error saving student: {str(e)}")

                # Send email to the student (check for any errors here as well)
                subject = 'Your new password'
                message = f'Hello {student.name},\n\nYour account has been created with the following login credentials:\n\nEmail: {student.email}\nPassword: {password}\n\nPlease login to the system to access your account.\n\n http://127.0.0.1:8000/login/ \n\n Please keep this information safe.'
                from_email = 'aleenaannshaji@gmail.com'  # Update with your library's email
                recipient_list = [student.email]
                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print(f"Email sent to: {student.email}")
                except Exception as e:
                    print(f"Error sending email: {str(e)}")

            return redirect('success_page')  # Create a success_page template

    return render(request, 'register_students.html')

def success_page(request):
    return render(request, 'success_page.html')

def add_staff(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if csv_file:
            print(f"Received CSV file: {csv_file.name}")

            # Process CSV file
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

            for row in csv_data:
                name, email = row
                password = get_random_string(length=12)

                user = User.objects.create_user(username=name, email=email, password=password)

                staff = Staff(name=name, email=email, password=password, user=user)
                try:
                    staff.save()
                    print(f"Saved staff: {staff.name}")
                except Exception as e:
                    print(f"Error saving staff: {str(e)}")

                # Send email to the student (check for any errors here as well)
                subject = 'Your new password'
                message = f'Hello {staff.name},\n\nYour account has been created with the following login credentials:\n\nEmail: {staff.email}\nPassword: {password}\n\nPlease login to the system to access your account.\n\n http://127.0.0.1:8000/login/ \n\n Please keep this information safe.'
                from_email = 'aleenaannshaji@gmail.com'  # Update with your library's email
                recipient_list = [staff.email]
                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    print(f"Email sent to: {staff.email}")
                except Exception as e:
                    print(f"Error sending email: {str(e)}")

            return redirect('staff_success_page')  # Create a success_page template

    return render(request, 'add_staff.html')

def staff_success_page(request):
    return render(request, 'staff_success_page.html')

def adminhome(request):
    return render(request, 'adminhome.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the entered email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

        # Authenticate the user
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            # Redirect to respective dashboard based on user type (student, staff, admin)
            if authenticated_user.is_superuser:
                return redirect('adminhome')
            elif hasattr(authenticated_user, 'student'):
                return redirect('student')
            elif hasattr(authenticated_user, 'staff'):
                return redirect('staff')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


def studenthome(request):
    return render(request, 'studenthome.html')

def logout(request):
    auth_logout(request)
    return redirect('index')


def add_books(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            print(f"Received CSV file: {csv_file.name}")
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in csv_data:
                accno, callno, title, author, year_of_published, isbn, publisher, pages, category, available_books, quantity = row
                book = Book(
                    accno=accno,
                    callno=callno,
                    title=title,
                    author=author,
                    year_of_published=int(year_of_published),
                    isbn=isbn,
                    publisher=publisher,
                    pages=int(pages),
                    category=category,
                    available_books=int(available_books),
                    quantity=int(quantity)
                )
                try:
                    book.save()
                    print(f"Saved book: {book.title}")
                except Exception as e:
                    print(f"Error saving book: {str(e)}")
            return redirect('book_success_page')  # Create a success_page template
    return render(request, 'add_books.html')


def book_success_page(request):
    return render(request, 'book_success_page.html')

def search_books(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(Q(accno__icontains=query) | Q(title__icontains=query) | Q(category__icontains=query))
        return render(request, 'search_book.html', {'books': books})
    else:
        return render(request, 'search_book.html', {'books': []})
    
def user_search_books(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(category__icontains=query))
        return render(request, 'student_booksearch.html', {'books': books})
    else:
        return render(request, 'student_booksearch.html', {'books': []})
 


def toggle_book_status(request):
    if request.method == 'GET':
        accno = request.GET.get('accno')
        status = request.GET.get('status')
        try:
            book = Book.objects.get(accno=accno)
            book.is_active = (status == 'active')
            book.save()
            return JsonResponse({'success': True})
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Book not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})    

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def send_borrow_request(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        accno = request.POST.get('accno')
        action = request.POST.get('action')
        book = Book.objects.get(accno=accno)

        if book.is_active:
            if action == 'borrow' and book.available_books > 0:
                # Get the underlying Student instance from the SimpleLazyObject
                student_instance = request.user.student if hasattr(request.user, 'student') else None
                
                if student_instance:
                    BorrowRequest.objects.create(student=student_instance, book=book, action='borrow')
                    messages.success(request, 'Borrow request sent successfully.')
                else:
                    messages.warning(request, 'User is not associated with a Student instance.')
            elif action == 'reserve':
                # Get the underlying Student instance from the SimpleLazyObject
                student_instance = request.user.student if hasattr(request.user, 'student') else None
                
                if student_instance:
                    BorrowRequest.objects.create(student=student_instance, book=book, action='reserve')
                    messages.success(request, 'Reservation request sent successfully.')
                else:
                    messages.warning(request, 'User is not associated with a Student instance.')
            else:
                messages.warning(request, 'Invalid action or no available books.')
        else:
            messages.warning(request, 'This book is not available for borrowing or reservation.')

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request.'})

def admin_borrow_requests(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    borrow_requests = BorrowRequest.objects.all()

    return render(request, 'admin_borrow_requests.html', {'borrow_requests': borrow_requests})



# 22/02/2024 
# def admin_approve_request(request, request_id):
#     if not request.user.is_superuser or request.method != 'POST':
#         return HttpResponseForbidden("You don't have permission to access this page.")
    
#     borrow_request = get_object_or_404(BorrowRequest, pk=request_id)
#     action = request.POST.get('action')
    
#     if action == 'approve':
#         # Record the borrowed book
#         borrowed_book = BorrowedBook.objects.create(student=borrow_request.student, book=borrow_request.book)
        
#         # Update the available_books count in the Book model
#         if borrow_request.book.available_books > 0:
#             borrow_request.book.available_books -= 1
#             borrow_request.book.save()
#         else:
#             return HttpResponseBadRequest("No available books to borrow.")
        
#         # Calculate return date after 15 days
#         borrowed_book.borrow_date = datetime.now().date()
#         borrowed_book.return_date = borrowed_book.borrow_date + timedelta(days=15)
#         borrowed_book.save()

#         borrow_request.is_approved = True
#         borrow_request.save()
        
#         # Calculate fine if overdue
#         borrowed_book.calculate_fine()
        
#         messages.success(request, f'Request approved successfully. Book must be returned by: {str(borrowed_book.return_date)}.')
    
#     elif action == 'reject':
#         borrow_request.is_approved = False
#         borrow_request.save()
#         messages.success(request, 'Request rejected successfully.')
    
#     borrow_request.delete()
    
#     return HttpResponseRedirect(reverse('admin_borrow_requests'))



#  20/03/2024


# def admin_approve_request(request, request_id):
#     if not request.user.is_superuser or request.method != 'POST':
#         return HttpResponseForbidden("You don't have permission to access this page.")

#     borrow_request = get_object_or_404(BorrowRequest, pk=request_id)

#     action = request.POST.get('action')

#     if action == 'approve':
#         # Record the borrowed book
#         borrowed_book = BorrowedBook.objects.create(student=borrow_request.student, book=borrow_request.book)
#         # Update the available_books count in the Book model

#         if borrow_request.book.available_books > 0:
#             borrow_request.book.available_books -= 1
#             borrow_request.book.save()
#             borrow_request.is_approved = True
#             borrow_request.save()
#             borrow_request.book.refresh_from_db()
#         else:
#             return HttpResponseBadRequest("No available books to borrow.")

#         # borrow_request.book.available_books -= 1    // already commented code
#         # borrow_request.book.save()
#         # borrow_request.is_approved = True
#         # borrow_request.save()     already commented code //
        
#         # Calculate return date after 15 days
#         borrowed_book.borrow_date = datetime.now().date()
#         borrowed_book.return_date = borrowed_book.borrow_date + timedelta(days=15)
#         borrowed_book.save()

#         # Calculate fine if overdue
#         borrowed_book.calculate_fine()

#         messages.success(request, f'Request approved successfully. Book must be returned by: {str(borrowed_book.return_date)}. Fine amount: {borrowed_book.fine_amount}')
#     elif action == 'reject':
#         borrow_request.is_approved = False
#         borrow_request.save()
#         messages.success(request, 'Request rejected successfully.')

#     borrow_request.delete()    

#     return HttpResponseRedirect(reverse('admin_borrow_requests'))


def admin_approve_request(request, request_id):
    if not request.user.is_superuser or request.method != 'POST':
        return HttpResponseForbidden("You don't have permission to access this page.")

    borrow_request = get_object_or_404(BorrowRequest, pk=request_id)
    action = request.POST.get('action')

    if action == 'approve':
        # Record the borrowed book
        borrowed_book = BorrowedBook.objects.create(student=borrow_request.student, book=borrow_request.book)
        
        # Update the available_books count in the Book model
        if borrow_request.book.available_books > 0:
            borrow_request.book.available_books -= 1
            borrow_request.book.save()
            borrow_request.is_approved = True
            borrow_request.save()
            borrow_request.book.refresh_from_db()
        else:
            return HttpResponseBadRequest("No available books to borrow.")

        # Calculate return date after 15 days
        borrowed_book.borrow_date = datetime.now().date()
        borrowed_book.return_date = borrowed_book.borrow_date + timedelta(days=15)
        borrowed_book.save()

        # Calculate fine if overdue
        borrowed_book.calculate_fine()

        messages.success(request, f'Request approved successfully. Book must be returned by: {str(borrowed_book.return_date)}. Fine amount: {borrowed_book.fine_amount}')
    elif action == 'reject':
        borrow_request.is_approved = False
        borrow_request.save()
        messages.success(request, 'Request rejected successfully.')

    borrow_request.delete()    

    return HttpResponseRedirect(reverse('admin_borrow_requests'))

def return_book(request, borrowed_book_id):
    borrowed_book = BorrowedBook.objects.get(pk=borrowed_book_id)

    if borrowed_book.return_book():
        # Record the returned book in the ReturnedBook model
        ReturnedBook.objects.create(
            student=borrowed_book.student,
            borrowed_book=borrowed_book.book,
            return_date=borrowed_book.return_date,
            fine_amount=borrowed_book.fine_amount
        )
        borrowed_book.delete()

        return redirect('view_borrowed_books')  # Redirect to the borrowed books list page
    else:
        # Handle the case where the book has already been returned
        return render(request, 'return_book_error.html', {'message': 'This book has already been returned.'})
    
    
def view_borrow_status(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        return HttpResponseForbidden("You don't have permission to access this page.")

    student = request.user.student
    borrowed_books = BorrowedBook.objects.filter(student=student)

    return render(request, 'borrow_status.html', {'borrowed_books': borrowed_books})



# #last# def request_book(request):
#     if request.method == 'POST':
#         form = BookRequestForm(request.POST)
#         if form.is_valid():
#             book_request = form.save(commit=False)
            
#             # Ensure that the user is authenticated and is a student
#             if request.user.is_authenticated and hasattr(request.user, 'student'):
#                 book_request.student = request.user.student
#                 book_request.save()
#                 messages.success(request, 'Book request submitted successfully.')
#                 return redirect('new_book_success')
#             else:
#                 # Handle the case where the user is not authenticated or not a student
#                 messages.error(request, 'You must be logged in as a student to request a book.')
#     else:
#         form = BookRequestForm()

#     return render(request, 'request_book.html', {'form': form})

def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.student = request.user.student  # Assuming you have a user profile model with a 'student' field
            book_request.save()
            messages.success(request, 'Book request submitted successfully. Waiting for approval.')
            return redirect('new_book_success')  # Redirect to the home page or any other desired page
    else:
        form = BookRequestForm()

    return render(request, 'request_book.html', {'form': form})

def new_book_success(request):
    return render(request, 'new_book_success.html')

def view_book_requests(request):
    if not request.user.is_superuser:
        return redirect('index')  # Redirect to home or another page if the user is not a superuser

    book_requests = BookRequest.objects.all()

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        book_request = BookRequest.objects.get(id=request_id)

        if action == 'approve':
            book_request.is_approved = True
            book_request.save()
            messages.success(request, f'Request for "{book_request.title}" approved successfully.')
        elif action == 'reject':
            book_request.delete()
            messages.success(request, f'Request for "{book_request.title}" rejected successfully.')

        return redirect('view_book_requests')

    return render(request, 'newbook_request.html', {'book_requests': book_requests})



def book_approve_request(request, request_id):
    if not request.user.is_superuser:
        return redirect('index')  # Redirect to home or another page if the user is not a superuser

    book_request = get_object_or_404(BookRequest, id=request_id)
    book_request.is_approved = True
    book_request.save()

    messages.success(request, f'Request for "{book_request.title}" approved successfully.')
    return redirect('book_approval_success')

def book_reject_request(request, request_id):
    if not request.user.is_superuser:
        return redirect('index')  # Redirect to home or another page if the user is not a superuser

    book_request = get_object_or_404(BookRequest, id=request_id)
    book_request.delete()

    messages.success(request, f'Request for "{book_request.title}" rejected successfully.')
    return redirect('book_rejection_success')

def book_approval_success(request):
    return render(request, 'book_approval_success.html')

def book_rejection_success(request):
    return render(request, 'book_rejection_success.html')

def view_request_status(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not logged in

    student_requests = BookRequest.objects.filter(student=request.user.student)

    return render(request, 'view_request_status.html', {'student_requests': student_requests})


# def request_book(request):
#     if request.method == 'POST':
#         form = BookRequestForm(request.POST)
#         if form.is_valid():
#             book_request = form.save(commit=False)
#             book_request.student = request.user
#             book_request.save()
#             messages.success(request, 'Book request submitted successfully.')
#             return redirect('request_book')
#     else:
#         form = BookRequestForm()

#     return render(request, 'request_book.html', {'form': form})



# def view_borrowed_books(request):    #For admin to see all the borrowed books
#     borrowed_books = BorrowedBook.objects.all()
#     return render(request, 'view_borrowed_books.html', {'borrowed_books': borrowed_books})

def view_borrowed_books(request):
    query = request.GET.get('q')
    borrowed_books = []

    if query:
        # Use Q objects for a case-insensitive search
        borrowed_books = BorrowedBook.objects.filter(
            Q(book__title__icontains=query) | Q(book__category__icontains=query)
        )

    return render(request, 'view_borrowed_books.html', {'borrowed_books': borrowed_books, 'query': query})


def admin_view_requests(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admins to the home page

    book_requests = BookRequest.objects.all()

    return render(request, 'newbook_request.html', {'book_requests': book_requests})


# def book_approve_request(request, request_id):
#     if not request.user.is_superuser:
#         return redirect('home')

#     book_request = get_object_or_404(BookRequest, id=request_id)
#     book_request.is_approved = True
#     book_request.save()
#     messages.success(request, f'Request "{book_request.title}" has been approved.')
#     return redirect('admin_view_requests')

# def book_reject_request(request, request_id):
#     if not request.user.is_superuser:
#         return redirect('home')

#     book_request = get_object_or_404(BookRequest, id=request_id)
#     messages.success(request, f'Request "{book_request.title}" has been rejected.')
#     return redirect('admin_view_requests')


def add_program(request):
    error_message = None
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program_name = form.cleaned_data['program']
            d_id = form.cleaned_data['d_id']  # Update to 'd_id'

            # Check if a program with the same name and department already exists
            if Program.objects.filter(program=program_name, d_id=d_id).exists():
                error_message = 'A program with this name in the selected department already exists.'
            else:
                form.save()
            return redirect('program_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form, 'error_message': error_message})


def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department_name = form.cleaned_data['department']
            if Department.objects.filter(department=department_name).exists():
                error_message = 'Department with this name already exists.'
            else:
                form.save()
                return redirect('department_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = DepartmentForm()
        error_message = None

    return render(request, 'add_department.html', {'form': form, 'error_message': error_message})


def add_designation(request):
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            designation_name = form.cleaned_data['designation']
            if Designation.objects.filter(designation=designation_name).exists():
                error_message = 'Designation with this name already exists.'
            else:
                form.save()
                return redirect('designation_list')
        else:
            error_message = 'Form is invalid. Please check your input.'
    else:
        form = DesignationForm()
        error_message= None
    return render(request, 'add_designation.html', {'form': form, 'error_message': error_message})


def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def designation_list(request):
    designations = Designation.objects.all()
    return render(request, 'designation_list.html', {'designations': designations})


def search_students(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'

    students = []
    if query:
        # Search students by ID or name
        students = Student.objects.filter(Q(id__icontains=query) | Q(name__icontains=query))

    return render(request, 'member_list.html', {'students': students, 'query': query})


def about(request):
    return render(request, 'about.html')


def student_borrowed_books(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    borrowed_books = BorrowedBook.objects.filter(student=student)
    return render(request, 'student_borrowed_books.html', {'student': student, 'borrowed_books': borrowed_books})

def view_borrowed_books_user(request):
    query = request.GET.get('q')
    borrowed_books = []

    if query:
        # Assuming you have a Book model with a 'title' field
        borrowed_books = BorrowedBook.objects.filter(book__title__icontains=query)

    return render(request, 'view_borrowed_books_user.html', {'borrowed_books': borrowed_books, 'query': query})


from .models import Review

# def save_review(request):
#     if request.method == 'POST':
#         borrowed_book_id = request.POST.get('borrowed_book_id')
#         description = request.POST.get('description')
        
#         if borrowed_book_id and description:
#             # Create a new review object
#             review = Review.objects.create(
#                 borrowed_book_id=borrowed_book_id,
#                 description=description
#             )
#             # Optionally, you can add any additional processing or validation here
            
#             # Redirect the user to a success page or back to the previous page
#             return redirect('success_page')  # Change 'success_page' to the appropriate URL name
#         else:
#             # If any required data is missing, return a bad request response
#             return HttpResponseBadRequest("Missing required data")
#     else:
#         # If the request method is not POST, return a bad request response
#         return HttpResponseBadRequest("Invalid request method")

# def save_review(request):
#     if request.method == 'POST':
#         borrowed_book_id = request.POST.get('borrowed_book_id')
#         description = request.POST.get('description')

#         borrowed_book = BorrowedBook.objects.get(id=borrowed_book_id)
#         review = Review.objects.create(borrowed_book=borrowed_book, description=description)

#         return redirect('borrow_status')  # Replace 'borrow_status' with the URL name of your borrow status page
#     else:
#         return redirect('borrow_status')  # Handle GET requests or invalid requests

def save_review(request):
    if request.method == 'POST':
        borrowed_book_id = request.POST.get('borrowed_book_id')
        description = request.POST.get('description')

        # Get the BorrowedBook object
        borrowed_book = BorrowedBook.objects.get(id=borrowed_book_id)

        # Create a new Review object
        review = Review.objects.create(borrowed_book=borrowed_book, description=description)

        messages.success(request, 'Review added successfully.')

    return redirect('view_borrow_status')


def review_list(request):
    reviews = Review.objects.select_related('borrowed_book__student', 'borrowed_book__book').all()
    return render(request, 'review_list.html', {'reviews': reviews})


#20/03/2024
# def return_book(request, borrowed_book_id):   
#     borrowed_book = BorrowedBook.objects.get(pk=borrowed_book_id)

#     if borrowed_book.return_book():
#         # Record the returned book in the ReturnedBook model
#         ReturnedBook.objects.create(
#             student=borrowed_book.student,
#             borrowed_book=borrowed_book.book,
#             return_date=borrowed_book.return_date,
#             fine_amount=borrowed_book.fine_amount
#         )
#         borrowed_book.delete()

#         return redirect('view_borrowed_books')  # Redirect to the borrowed books list page
#     else:
#         # Handle the case where the book has already been returned
#         return render(request, 'return_book_error.html', {'message': 'This book has already been returned.'})

from django.conf import settings
import razorpay
from django.template.response import TemplateResponse

def pay_fine(request, borrowed_book_id):   #05/04/2024
    borrowed_book = BorrowedBook.objects.get(pk=borrowed_book_id)
    if request.method == 'POST':
        amount_paisa = int(borrowed_book.fine_amount * 100)  # Convert to paisa

        # client = razorpay.Client(auth=('rzp_test_a8SpiQASAPrLki', 'VZpK4EfTTuqEUQjMSgRkeVLw'))
        # payment = client.order.create(data={ 'amount':amount_paisa, 'currency': 'INR', 'payment_capture': 1 })
       
        # payment.payment_id = payment['id'] #new
        # payment.save()

        context = {
            'borrowed_book': borrowed_book,
            'amount_paisa': amount_paisa,  # Pass the multiplied amount to the template
            
            # 'payid' : payment['id']
        }
        return TemplateResponse(request, 'pay_fine.html', context)
    else:
        context = {'borrowed_book': borrowed_book}
        return TemplateResponse(request, 'pay_fine.html', context)

    
def payment_success(request, payment_id):    #05/04/2024
    # payment = Payment.objects.get(payment_id=payment_id)
    # payment.payment_status = 'success'  # Update payment status
    # payment.save()
    return redirect('student')



def payment_handler(request):
    # Handle the payment success response from Razorpay
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        booking_id = request.POST.get('booking_id')  # Assuming the booking ID is sent in the request
        payment = Payment.objects.create(payment_id=razorpay_payment_id,
                                                 borrowed_book_id=booking_id,
                                                 payment_status='success',
                                                 amount=0,  # Set the amount as needed
                                                 payment_date=timezone.now())
                # Redirect to a success page or perform any other action
        return redirect('payment_success', payment_id=payment.payment_id)
               

    # Redirect to a failure page or perform any other action if payment is not successful
    return redirect('payment_failure')



# import os
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier

# def recommend_books(request):
#     # Step 1: Get the path to the CSV files
#     csv_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'csv')
#     books_file_path = os.path.join(csv_directory, 'books.csv')
#     borrowers_file_path = os.path.join(csv_directory, 'borrowers.csv')
#     historys_file_path = os.path.join(csv_directory, 'historys.csv')

#     # Step 2: Load and preprocess the data
#     books_df = pd.read_csv(books_file_path)
#     borrowers_df = pd.read_csv(borrowers_file_path)
#     history_df = pd.read_csv(historys_file_path)

#     # Merge dataframes appropriately
#     merged_df = pd.merge(history_df, borrowers_df, on='borrower_id')
#     merged_df = pd.merge(merged_df, books_df, on='book_id')

#     # Step 3: Train/Test Split
#     X = merged_df[['borrower_id', 'book_id']]  # Features
#     y = merged_df['category']  # Target

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Step 4: Train Decision Tree Model
#     decision_tree_model = DecisionTreeClassifier()
#     decision_tree_model.fit(X_train, y_train)

#     # Retrieve logged-in user's ID (assuming stored in session or request context)
#     user_id = request.user.id  # Adjust this based on your actual authentication setup

#     # Retrieve student based on user ID
#     student = User.objects.get(id=user_id)

#     # Assuming there's a field named 'borrower_id' in the Student model
#     borrower_id = student.student.id

#     # Step 5: Predict borrower's preference using Decision Tree and use it as input to RandomForest for recommendation
#     borrower_history = merged_df[merged_df['borrower_id'] == borrower_id]
#     predicted_preference = decision_tree_model.predict(borrower_history[['borrower_id', 'book_id']])

#     # Use the predicted preference as input to the RandomForest model for book recommendation
#     random_forest_model = RandomForestClassifier()
#     random_forest_model.fit(X_train, y_train)
#     recommended_books = books_df[books_df['category'] == predicted_preference[0]]

#     # Convert recommended books data to dictionary
#     recommended_books_data = recommended_books[['title', 'author', 'category']].to_dict(orient='records')

#     # Render the HTML template with recommended books data
#     return render(request, 'recommend_books.html', {'recommended_books': recommended_books_data})





# def view_fine_details(request):   #view whole student's fine details
#     # Fetch fine details from the BorrowedBook model
#     fine_details = BorrowedBook.objects.filter(return_date__lt=timezone.now().date())

#     for book in fine_details:
#         if book.return_date:
#             days_overdue = (timezone.now().date() - book.return_date).days
#             book.days_overdue = days_overdue
#             book.save()
    
#     # Render the HTML template with fine details
#     return render(request, 'fine_details.html', {'fine_details': fine_details})


from django.utils import timezone
def view_fine_details(request):
    # Get the logged-in student
    student = request.user.student
    
    # Fetch fine details for the logged-in student from the BorrowedBook model
    fine_details = BorrowedBook.objects.filter(student=student, return_date__lt=timezone.now().date())

    for book in fine_details:
        if book.return_date:
            days_overdue = (timezone.now().date() - book.return_date).days
            book.days_overdue = days_overdue
            book.save()
    
    # Render the HTML template with fine details
    return render(request, 'fine_details.html', {'fine_details': fine_details})




from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import BorrowedBook
from io import BytesIO

def generate_pdf_report(request):
    # Fetch borrowed books data
    borrowed_books = BorrowedBook.objects.all()

    # Create a buffer for the PDF
    buffer = BytesIO()

    # Create a new PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Set report title
    report_title = "Borrowed Books Report"

    # Create a list to hold PDF elements
    elements = []

    # Add LIBRARY MANAGEMENT SYSTEM heading to PDF
    style = getSampleStyleSheet()["Title"]
    style.alignment = 1  # Center alignment
    elements.append(Paragraph("LIBRARY MANAGEMENT SYSTEM", style))

    # Add report title to PDF
    style = getSampleStyleSheet()["Heading1"]
    elements.append(Paragraph(report_title, style))

    # Create a table for the report
    data = [['Student', 'Book', 'Category', 'Author', 'Borrow Date', 'Return Date']]
    for borrowed_book in borrowed_books:
        data.append([
            borrowed_book.student.name if borrowed_book.student else '',  # Assuming student has a 'name' field
            borrowed_book.book.title if borrowed_book.book else '',    # Assuming book has a 'title' field
            borrowed_book.book.category if borrowed_book.book else '',    # Assuming book has a 'category' field
            borrowed_book.book.author if borrowed_book.book else '',    # Assuming book has an 'author' field
            str(borrowed_book.borrow_date),
            str(borrowed_book.return_date)
        ])

    # Get the width of the page
    width, height = letter

    # Define table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table
    table = Table(data)
    table.setStyle(style)

    # Add table to PDF elements
    elements.append(table)

    # Build PDF document
    pdf_title = "Admin_Borrowed_Books_Report.pdf"
    pdf.build(elements)

    # Close the PDF document
    buffer.seek(0)

    # Create a HTTP response with PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_title}"'

    # Write PDF data to the response
    response.write(buffer.getvalue())
    buffer.close()

    return response



from reportlab.lib.enums import TA_CENTER 


def generate_borrowed_books_report(student):
    # Fetch borrowed books data for the specified student
    borrowed_books = BorrowedBook.objects.filter(student=student)

    # Create a buffer for the PDF
    buffer = BytesIO()

    # Create a new PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Set report title
    report_title = f"{student.name}'s Borrowed Books Report"

    # Create a list to hold PDF elements
    elements = []

    # Add LIBRARY MANAGEMENT SYSTEM heading to PDF
    style = getSampleStyleSheet()["Title"]
    style.alignment = 1  # Center alignment
    elements.append(Paragraph("LIBRARY MANAGEMENT SYSTEM", style))

    # Add report title to PDF
    style = getSampleStyleSheet()["Heading1"]
    elements.append(Paragraph(report_title, style))


    # Create a table for the report
    data = [['Title', 'Author', 'Category', 'Borrow Date', 'Return Date', 'Fine Amount']]
    for borrowed_book in borrowed_books:
        data.append([
            borrowed_book.book.title if borrowed_book.book else '',
            borrowed_book.book.author if borrowed_book.book else '',
            borrowed_book.book.category if borrowed_book.book else '',
            str(borrowed_book.borrow_date),
            str(borrowed_book.return_date),
            str(borrowed_book.fine_amount)
        ])

    width, height=letter    

    # Define table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table
    table = Table(data) # Set width of each column
    table.setStyle(style)

    # Add table to PDF elements
    elements.append(table)

    # Build PDF document
    pdf_title = f"{student.name}_Borrowed_Books_Report.pdf"
    pdf.build(elements)

    # Close the PDF document
    buffer.seek(0)

    return buffer


def view_borrowed_books_report(request):
    student = request.user.student  # Assuming you have a UserProfile linked to the User model
    if student:
        buffer = generate_borrowed_books_report(student)
        pdf_title = "Students_Borrowed_Books_Report.pdf"

        # Create a HTTP response with PDF mime type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_title}"'
        # Write PDF data to the response
        response.write(buffer.getvalue())
        buffer.close()
        return response
    else:
        return HttpResponse("You are not authorized to view this page.")
