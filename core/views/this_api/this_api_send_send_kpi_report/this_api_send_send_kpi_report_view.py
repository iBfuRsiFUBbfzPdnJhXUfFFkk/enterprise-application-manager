import datetime
from time import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now

from core.models.sprint import Sprint
from core.settings.common.email import EMAIL_FROM
from core.utilities.base_render import base_render
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


def this_api_send_send_kpi_report_view(request):
    start_time: float = time()
    sprint = Sprint.current_sprint()
    sprint_kpis = KeyPerformanceIndicatorSprint.objects.filter(sprint=sprint)
    from_email = EMAIL_FROM

    for kpi in sprint_kpis:
        subject = f"Your Sprint {sprint.name} KPI Report"
        if kpi.person_developer.user_account is None:
            continue
        recipient_email = kpi.person_developer.user_account.email

        html_content = render_to_string(
            "email/kpi_email.html",
            {
                "sprint": sprint,
                "sprint_start_date": sprint.date_start,
                "sprint_end_date": sprint.date_end,
                "stat": kpi,
            },
        )

        email = EmailMultiAlternatives(subject, "", from_email, [recipient_email], [from_email])
        email.attach_alternative(html_content, "text/html")
        email.send()
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {},
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )

def should_send_email_today(sprint):
    """
    Checks if an email should be sent today based on the sprint schedule:
    - Thurs of 1st week
    - Mon, Wed, Thurs of 2nd week
    - Tue, Wed, Thurs, Fri of 3rd week
    - Mon, Tue after sprint ends
    """
    today = now().date()
    sprint_start = sprint.start_date
    sprint_end = sprint.end_date
    monday_after_end = sprint_end + datetime.timedelta(days=(7 - sprint_end.weekday()))

    # Adjusted days to correctly align with a **Sunday** start sprint
    first_week = {sprint_start + datetime.timedelta(days=6)}  # Thursday (Day 7)
    second_week = {sprint_start + datetime.timedelta(days=i) for i in [8, 10, 11]}  # Mon (9), Wed (11), Thurs (12)
    third_week = {sprint_start + datetime.timedelta(days=i) for i in [15, 16, 17, 18]}  # Tue (16), Wed (17), Thurs (18), Fri (19)
    week_after = {monday_after_end - datetime.timedelta(days=1), monday_after_end}  # Mon (23), Tue (24)

    email_days = first_week | second_week | third_week | week_after
    if today in email_days:
        print(f"✅ Today ({today}) is an email day!")
        return True
    else:
        print(f"❌ Today ({today}) is NOT an email day.")
        return False