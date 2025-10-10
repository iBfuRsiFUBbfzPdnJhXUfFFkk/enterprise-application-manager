from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.user_profile_form import UserProfileForm
from core.utilities.base_render import base_render


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    User profile page where users can view and update their information.
    """
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirect to the same page to show updated data
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return base_render(
        request=request,
        template_name='authenticated/profile/profile.html',
        context=context
    )
