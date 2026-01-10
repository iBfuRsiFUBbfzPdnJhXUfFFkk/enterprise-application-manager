from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.user_profile_form import UserProfileForm
from core.models.user_passkey import UserPasskey
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
            messages.success(request, 'Your profile has been updated successfully!')
            # Redirect to the same page to show updated data and success message
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    # Get user's passkeys for security settings section
    passkeys = UserPasskey.objects.filter(user=user).order_by('-created_at')

    context = {
        'form': form,
        'user': user,
        'passkeys': passkeys,
    }

    return base_render(
        request=request,
        template_name='authenticated/profile/profile.html',
        context=context
    )
