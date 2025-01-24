import boto3
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import FileUploadForm
import mimetypes


@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_instance = File(
            original_name=uploaded_file.name,
            user=request.user,
        )
        file_instance.save()
        file_instance.file = uploaded_file
        file_instance.save()
        return redirect('home')
    return redirect('home')

@login_required
def home(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'app/home.html', {'files': files})


@login_required
def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    owner = file.user == request.user

    if not owner and not file.is_public:
        return render(request, 'app/file_not_found.html', {'message': 'This file is private or does not exist.'})

    return render(request, 'app/view_file.html', {'file': file, 'owner': owner})


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


@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    if file.user != request.user and not file.is_public:
        raise Http404('You do not have permission to download this file.')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_key = file.file.name
    file_name = file.original_name

    content_type, _ = mimetypes.guess_type(file_name)
    if not content_type:
        content_type = 'application/octet-stream'

    s3_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file_content = s3_object['Body'].read()

    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response