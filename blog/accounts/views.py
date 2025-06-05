from django.shortcuts import render , redirect
from django.contrib import messages
from . import form as fm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from . import form as fm
from django.contrib.auth.decorators import login_required
# Create your views here.



def register_user(request):
    if request.method == 'POST':
        form = fm.RegisterUserForm(request.POST)
        print("Form data:", request.POST)  # Debugging line to check form data
        print("Form is valid:", form.is_valid())  # Debugging line to check if form is valid
        if form.is_valid():
            var = form.save(commit=False)
            var.username = var.email  # Set username from email
            var.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.warning(request, 'Registration failed. Please correct the errors below.')
    else:
        form = fm.RegisterUserForm()
    
    # Always define context before rendering
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            # User is authenticated and active
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')  # Redirect to the dashboard or any other page
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Redirect back to the login page
        
    return render(request, 'accounts/login.html')

login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to the login page after logout

login_required
def change_password(request):
    if request.method == 'POST':
        form = fm.UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')  
        else:
            messages.warning(request, 'Please correct the errors below.')
            return redirect('change-password')
    else:
        form = fm.UserPasswordChangeForm(request.user)
        context = {'form': form }
    return render(request, 'accounts/change_password.html', context)

login_required
def update_profile(request):
    if request.method == 'POST':
        form = fm.UpdateUserProfileForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')  
        else:
            messages.warning(request, 'Please correct the errors below.')
            return redirect('update-profile')
        
    else:
        form = fm.UpdateUserProfileForm(instance=request.user)
        context = { 'form': form }
    return render(request, 'accounts/update_profile.html', context)