from django.shortcuts import render, redirect
from.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print (form)
        if form.is_valid():
            # Hash the password before saving
            user = form.save(commit=False)
           # user.password = make_password(form.cleaned_data['password']) # type: ignore
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# Create your views here.
