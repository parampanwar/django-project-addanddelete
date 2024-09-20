from django.shortcuts import render, redirect
from .forms import newform
from .models import User,Hobby  
from django.shortcuts import render, get_object_or_404


def new(request):
    if request.method == 'POST':
        form = newform(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  
            form.save_m2m()
            return redirect('new')
    else:
        form = newform()
    return render(request, "newapp.html", {"form": form})


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_detail.html', {'user': user})



def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'user_detail.html', {'users': users})



# code for editing detail
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = newform(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list or another page
    else:
        form = newform(instance=user)
    return render(request, 'edit_user.html', {'form': form})


# code for deleting user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list') 
    return render(request, 'confirm_delete.html', {'user': user})