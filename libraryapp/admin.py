from django.contrib import admin
from .models import Student, Book,BookCopy, BorrowRequest, BorrowedBook, BookRequest, Review, Payment
# Register your models here.

admin.site.register(Student)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(BorrowRequest)
admin.site.register(BorrowedBook)
admin.site.register(BookRequest)
admin.site.register(Review)
admin.site.register(Payment)