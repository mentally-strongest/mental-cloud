from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import FileUploadForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('home')
    else:
        form = FileUploadForm()
    return render(request, 'app/file_upload.html', {'form': form})


@login_required
def home(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'app/home.html', {'files': files})


@login_required
def change_privacy(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)

    if request.method == 'POST':
        file.is_public = not file.is_public

        if file.is_public and not file.shared_link:
            file.generate_shared_link()

        elif not file.is_public:
            file.delete_shared_link()

        file.save()
        return redirect('home')

    return render(request, 'app/change_privacy.html', {'file': file})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, user=request.user)
    file.delete()
    return redirect('home')



