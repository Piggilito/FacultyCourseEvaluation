from django import forms
from django.core.exceptions import ValidationError

from .models import StudentSubmission


class StudentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentSubmission
        fields = [
            'course',
            'rate_commit_1',
            'rate_commit_2',
            'rate_commit_3',
            'rate_commit_4',
            'rate_commit_5',
            'rate_knowledge_1',
            'rate_knowledge_2',
            'rate_knowledge_3',
            'rate_knowledge_4',
            'rate_knowledge_5',
            'rate_teaching_1',
            'rate_teaching_2',
            'rate_teaching_3',
            'rate_teaching_4',
            'rate_teaching_5',
            'rate_management_1',
            'rate_management_2',
            'rate_management_3',
            'rate_management_4',
            'rate_management_5',
            'openended_other',
            'openended_strong',
            'openended_weak',
        ]

    def __init__(self, *args, **kwargs):
        self.url_course_id = kwargs.pop('url_course_id')  # pop it from kwargs before parent init call

        super(StudentSubmissionForm, self).__init__(*args, **kwargs)

    def clean_course(self):
        data = self.cleaned_data["course"]
        # check that url course ID == form course ID
        if self.url_course_id is not data.id:
            raise ValidationError("URL Course ID differs from Form Course ID!")
        return data

