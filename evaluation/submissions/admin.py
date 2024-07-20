from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin

from .models import User, StudentProfile, InstructorProfile, SupervisorProfile, Batch, Course, StudentSubmission, StudentSubmissionLog, SupervisorSubmission, SupervisorSubmissionLog


class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_student')
    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'profile_picture')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_student', 'is_instructor', 'is_supervisor')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'first_name', 'middle_name', 'last_name', 'password1', 'password2')}),)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_student', 'is_instructor', 'is_supervisor',)
    search_fields = ('username', 'first_name', 'middle_name', 'last_name', 'email',)
    ordering = ('last_name', 'first_name')
    filter_horizontal = ('groups', 'user_permissions',)

class StudentProfileAdmin(admin.ModelAdmin):
    pass

class SupervisorProfileAdmin(admin.ModelAdmin):
    pass

class InstructorProfileAdmin(admin.ModelAdmin):
    pass

class BatchAdmin(admin.ModelAdmin):
    pass

class CourseAdmin(admin.ModelAdmin):
    pass

class SupervisorSubmissionAdmin(admin.ModelAdmin):
    pass

class StudentSubmissionAdmin(admin.ModelAdmin):
    pass

class StudentSubmissionLogAdmin(admin.ModelAdmin):
    pass

class SupervisorSubmissionLogAdmin(admin.ModelAdmin):
    pass

# unregister default auth Admin models
admin.site.unregister(models.Group)

# register all of our models to Admin
admin.site.register(User, UserAdmin)
admin.site.register(StudentSubmission, StudentSubmissionAdmin)
admin.site.register(SupervisorSubmission, SupervisorSubmissionAdmin)
admin.site.register(StudentSubmissionLog, StudentSubmissionLogAdmin)
admin.site.register(SupervisorSubmissionLog, SupervisorSubmissionLogAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(Batch, BatchAdmin)

admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(InstructorProfile, InstructorProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
