from datetime import datetime, timedelta
from django.db import IntegrityError, models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db import transaction

from django.utils import timezone

# Create your models here.


class Department(models.Model):
    d_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.department

class Program(models.Model):
    p_id = models.AutoField(primary_key=True)
    program = models.CharField(max_length=50, unique=True)
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

class Designation(models.Model):
    des_id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=50, unique=True)



class Student(models.Model):
    name = models.CharField("Student Name", max_length=100)
    email = models.EmailField("Email id", unique=True)
    password = models.CharField("Password", max_length=10, default=get_random_string(length=12))  # Store hashed passwords in a real application 
    p_id = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', blank=True, null=True)


class Staff(models.Model):
    name = models.CharField("Staff Name", max_length=100)
    email = models.EmailField("Email id", unique=True)
    password = models.CharField("Password", max_length=10, default=get_random_string(length=12))  # Store hashed passwords in a real application
    d_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    des_id = models.ForeignKey(Designation, on_delete=models.CASCADE, blank=True, null=True)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff', blank=True, null=True)

class Book(models.Model):
    accno = models.CharField(max_length=10, primary_key=True, unique=True)
    callno = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_of_published = models.PositiveIntegerField()
    isbn = models.CharField(max_length=12, unique=True)
    publisher = models.CharField(max_length=50)
    pages = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    available_books = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.accno:
            self.accno = self.generate_accno()
        if not self.callno:
            self.callno = self.generate_callno()

        book_copies = [
            BookCopy(copy_id=f'{self.accno}-Copy{str(i).zfill(2)}', book=self)
            for i in range(1, self.quantity + 1)
        ]    
                
        with transaction.atomic():
            try:
                # Save the Book instance
                super(Book, self).save(*args, **kwargs)
                # Use bulk_create to insert multiple instances in a single query
                BookCopy.objects.bulk_create(book_copies)
            except IntegrityError:
                # Handle the case where a copy_id is not unique
                # You can log the error or handle it based on your requirement
                pass

    # def save(self, *args, **kwargs):
    #     if not self.accno:
    #         self.accno = self.generate_accno()
    #     if not self.callno:
    #         self.callno = self.generate_callno()
    #     super(Book, self).save(*args, **kwargs)

    #     for i in range(1, self.quantity + 1):
    #         book_copy_id = f'{self.accno}-Copy{str(i).zfill(2)}'
    #         book_copy = BookCopy(copy_id=book_copy_id)
    #         book_copy.book = self  # Set the book instance
    #         book_copy.save()

        # for i in range(1, self.quantity + 1):
        #     book_copy_id = f'{self.accno}-Copy{str(i).zfill(2)}'
        #     BookCopy.objects.create(book=self, copy_id=book_copy_id)

    def generate_callno(self):
        last_book = Book.objects.order_by('-callno').first()
        if last_book:
            last_index = int(last_book.callno.split('-')[-1])
            new_index = last_index + 1
        else:
            new_index = 1
        return f"{new_index:04d}-{self.author.split()[0][0]}"

    def generate_accno(self):
        last_book = Book.objects.order_by('-accno').first()
        if last_book:
            last_index = int(last_book.accno.split('Acc')[-1])
            new_index = last_index + 1
        else:
            new_index = 1
        return f"Acc{new_index:03d}"

    def __str__(self):
        return f"{self.callno} - {self.title}"

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    copy_id = models.CharField(max_length=10, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.copy_id    

class BorrowRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=10)  # 'borrow' or 'reserve'
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
class BorrowedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True) 
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def return_book(self):
        if self.return_date:
            return False  # Book already returned
        else:
            self.return_date = timezone.now().date()  # Set return date to current date
            self.book.available_books += 1  # Increment available_books count
            self.book.save()  # Save the updated book
            self.calculate_fine()  # Calculate fine if overdue
            self.save()  # Save the return_date for the borrowed book
            return True  # Book successfully returned  

    def calculate_fine(self):
        if self.return_date and self.return_date < timezone.now().date():
            days_overdue = (timezone.now().date() - self.return_date).days
            print(days_overdue)
            self.fine_amount = days_overdue * 3.00
            print(self.fine_amount)
            self.save()


class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.book.title} by {self.student.name}"   

class BookRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=50, default='Unknown Publisher')
    category = models.CharField(max_length=100, default='Uncategorized')
    edition = models.CharField(max_length=50, default='Unknown')
    no_of_copies = models.PositiveIntegerField(default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author} requested by {self.student.name}"   

class Review(models.Model):
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)       


class ReturnedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    borrowed_book = models.ForeignKey('BorrowedBook', on_delete=models.CASCADE,blank=True, null=True)
    return_date = models.DateField()
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} - Returned by {self.student.name}"    
    
class Payment(models.Model):
    borrowed_book = models.ForeignKey(BorrowedBook, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    