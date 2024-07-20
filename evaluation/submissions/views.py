from datetime import date
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .decorators import student_required, supervisor_required
from .models import StudentSubmissionLog, StudentSubmission, Batch, Course
from .forms import StudentSubmissionForm


@require_http_methods(["GET"])
def submissions_landing(request):
    return render(request, "submissions/landing.html", {})


@login_required(login_url="/login")
@require_http_methods(["GET"])
def submissions_dashboard(request):
    # hold batch / course info that still need submissions
    courses_count = 0
    submissions_needed = {}
    submissions_made = {}
    submissions_past = set()

    if hasattr(request.user, "student_profile"):
        # get all evaluation batches that have NOT ended yet (student review table)
        batches = Batch.objects.filter(review_period_end__gte=date.today()).order_by("-review_period_end")
        # for each batch's courses, check logs to see if the student submitted an evaluation
        for batch in batches:
            batch_key = str(batch)
            submissions_needed[batch_key] = []
            submissions_made[batch_key] = []
            for course in batch.courses.all():
                # look up the course by PK and check student has not already submitted an evaluation for it
                log = StudentSubmissionLog.objects.filter(course=course, author=request.user.student_profile).first()
                if not log:
                    # add to list for display in dashboard table
                    submissions_needed[batch_key].append(course)
                    courses_count += 1
                else:
                    submissions_made[batch_key].append(course)
    elif hasattr(request.user, "supervisor_profile"):
        # get all student submissions
        submissions_past = StudentSubmission.objects.all()
    context = {
        "courses_count": courses_count,
        "submissions_needed": submissions_needed,
        "submissions_made": submissions_made,
        "submissions_past": submissions_past,
    }
    return render(request, "submissions/dashboard.html", context)


@login_required(login_url="/login")
@supervisor_required()
@require_http_methods(["GET"])
def submission_student_detail(request, pk):
    sub = get_object_or_404(StudentSubmission, pk=pk)
    context = {
        "submission": sub,
    }
    return render(request, "submissions/detail.html", context)


@login_required(login_url="/login")
@student_required()
@requires_csrf_token
@require_http_methods(["GET", "POST"])
def submission_student_create(request, course_id):
    # look up the course by PK and check:
    # check the course passed along is valid
    course = get_object_or_404(Course, pk=course_id)
    context = {
        "course": course,
        "form": StudentSubmissionForm(initial={"course":course_id}, url_course_id=course_id),
    }
    # check student has not already submitted an evaluation for it
    log = StudentSubmissionLog.objects.filter(course=course, author=request.user.student_profile).first()
    # check that student is enrolled in said course
    if log or request.user not in course.students:
        next = request.GET.get(reverse("dashboard"))
        return HttpResponseRedirect(next)

    if request.method == "POST":
        form = StudentSubmissionForm(request.POST, url_course_id=course_id)
        context["form"] = form
        if form.is_valid():
            # save the student submission
            form.save()
            # create a submission log record
            StudentSubmissionLog.objects.create(course=course, author=request.user.student_profile)
            # send student back to dashboard
            context = {
                "new_submission": True
            }
            next = request.GET.get('next', reverse('dashboard'))
            return HttpResponseRedirect(next, context)

    return render(request, "submissions/create.html", context)

