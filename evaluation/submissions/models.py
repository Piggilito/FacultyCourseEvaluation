from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING, CASCADE


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    middle_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to="profile/", blank=True)

    def __str__(self):
        return self.username

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return '/images/default_profile.png'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="student_profile")
    submissions = models.ForeignKey("StudentSubmission", on_delete=DO_NOTHING, related_name="submission_student", blank=True, null=True)
    year = models.PositiveIntegerField()
    enrolled_degree = models.CharField(max_length=100)
    student_id = models.CharField(max_length=30, unique=True)
    enrolled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="instructor_profile")
    employed = models.BooleanField(default=False)
    years_employed = models.PositiveIntegerField()

    def __str__(self):
        return str(self.user)


class SupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="supervisor_profile")
    #submissions = models.ForeignKey("SupervisorSubmission", on_delete=DO_NOTHING, related_name="submission_supervisor")

    def __str__(self):
        return str(self.user)


class Batch(models.Model):
    title = models.CharField(max_length=140)
    review_period_start = models.DateTimeField()
    review_period_end = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Batches"

    def __str__(self):
        return str(self.title)


class Course(models.Model):
    course_id = models.CharField(max_length=15)
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(InstructorProfile, on_delete=DO_NOTHING, related_name="instructor_courses", blank=True)
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=DO_NOTHING, related_name="supervisor_courses", blank=True)
    students = models.ManyToManyField(StudentProfile, related_name="courses", blank=True)
    batch = models.ManyToManyField(Batch, related_name="courses",  blank=True)

    def __str__(self):
        return f"{self.title} ({self.course_id})"


# Disable updating/deleting of model records (secondary failsafe check to DB-level rules)
class NoUpdateDeleteQuerySet(models.QuerySet):
    # update calls should pass
    def update(self, *args, **kwargs):
        pass

    # delete calls should pass
    def delete(self, *args, **kwargs):
        pass


class StudentSubmissionLog(models.Model):
    author = models.ForeignKey(StudentProfile, on_delete=DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)

    # manager for queries
    objects = NoUpdateDeleteQuerySet()

    def __str__(self):
        return f"{self.created_on} - {self.course}"


class SupervisorSubmissionLog(models.Model):
    author = models.ForeignKey(StudentProfile, on_delete=DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)

    # manager for queries
    objects = NoUpdateDeleteQuerySet()

    def __str__(self):
        return f"{self.created_on} - {self.course}"


class StudentSubmission(models.Model):
    course = models.ForeignKey(Course, on_delete=DO_NOTHING)
    # response form fields go next...
    # A. Commitment Section
    rate_commit_1 = models.PositiveSmallIntegerField()
    rate_commit_2 = models.PositiveSmallIntegerField()
    rate_commit_3 = models.PositiveSmallIntegerField()
    rate_commit_4 = models.PositiveSmallIntegerField()
    rate_commit_5 = models.PositiveSmallIntegerField()

    # B. Knowledge Section
    rate_knowledge_1 = models.PositiveSmallIntegerField()
    rate_knowledge_2 = models.PositiveSmallIntegerField()
    rate_knowledge_3 = models.PositiveSmallIntegerField()
    rate_knowledge_4 = models.PositiveSmallIntegerField()
    rate_knowledge_5 = models.PositiveSmallIntegerField()

    # C. Teaching for Independent Learning
    rate_teaching_1 = models.PositiveSmallIntegerField()
    rate_teaching_2 = models.PositiveSmallIntegerField()
    rate_teaching_3 = models.PositiveSmallIntegerField()
    rate_teaching_4 = models.PositiveSmallIntegerField()
    rate_teaching_5 = models.PositiveSmallIntegerField()

    # D. Management of Learning
    rate_management_1 = models.PositiveSmallIntegerField()
    rate_management_2 = models.PositiveSmallIntegerField()
    rate_management_3 = models.PositiveSmallIntegerField()
    rate_management_4 = models.PositiveSmallIntegerField()
    rate_management_5 = models.PositiveSmallIntegerField()
    
    # open-ended questions
    openended_other = models.TextField()
    openended_strong = models.TextField()
    openended_weak = models.TextField()

    # manager for queries
    objects = NoUpdateDeleteQuerySet()

    def __str__(self):
        return f"Student Eval - {self.pk}"


class SupervisorSubmission(models.Model):
    course = models.ForeignKey(Course, on_delete=DO_NOTHING)
    # response form fields go next...
    rating = models.PositiveSmallIntegerField()
    feedback = models.TextField()

    # manager for queries
    objects = NoUpdateDeleteQuerySet()

    def __str__(self):
        return f"Supervisor Eval - {self.pk}"

