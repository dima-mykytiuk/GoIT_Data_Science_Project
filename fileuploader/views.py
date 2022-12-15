from django.contrib.auth.hashers import check_password
from django.contrib.messages import info
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from fileuploader.forms import UploadFile, LoginForm, SignUpForm
from fileuploader.models import ImageManager, NeuralModel
from fileuploader.keras_model import image_classify
from datetime import datetime, timezone, timedelta
from django.core.files import File

from django.contrib.auth import login, logout, authenticate

import os
# Create your views here.


class IndexView(View):
    template_name = 'pages/index.html'
    form_class = UploadFile
    context = {}
    
    def get(self, request, *args, **kwargs):
        neural_networks = NeuralModel.objects.all()
        if not request.session or not request.session.session_key:
            request.session.save()
        if len(neural_networks) == 0:
            with open("sgd_model.h5", 'rb') as file:
                file_field = File(file)
                NeuralModel.objects.create(model_type='Xception Model', model_name=file_field).save()
            os.remove("sgd_model.h5")
        self.context.update({'title': 'Image Classifier'})
        self.context.update({'form': self.form_class})
        image = ImageManager.objects.filter(session_key=request.session.session_key).last()
        if image:
            self.context.update({'image': image})
            self.context.update({'result': image.model_prediction})
            self.context.update({'accuracy': image.accuracy})
        if self.context.get('image'):
            image = self.context.get('image')
            upload_time = image.uploaded_at
            current_time = datetime.now(timezone.utc)
            difference = current_time - upload_time
            if difference > timedelta(0, 15):
                self.context.update({'image': None})
        return render(request, self.template_name, context=self.context)
    
    def post(self, request, *args, **kwargs):
        if 'actual_picture' not in request.POST:
            file = request.FILES['choose_file']
            model = request.POST['model']
            neural_model = NeuralModel.objects.get(pk=model)
            model_path = neural_model.model_name.path
            if request.user.id:
                document = ImageManager.objects.create(file_name=file,
                                                       model_type=neural_model,
                                                       session_key=request.session.session_key,
                                                       user_id=request.user.id
                                                       )
                document.save()
            else:
                document = ImageManager.objects.create(file_name=file, model_type=neural_model, session_key=request.session.session_key)
                document.save()
            document_path = document.file_name.path
            result = image_classify(document_path, model_path)
            if result != ["Invalid photo"]:
                document.model_prediction = result[0]
                document.accuracy = result[1]
                document.predicted = True
                document.save()
        else:
            image_id = self.context.get('image').id
            image_object = ImageManager.objects.get(pk=image_id)
            actual_info = request.POST['actual_picture']
            image_object.predicted = False
            image_object.info_from_user = actual_info
            image_object.save()
        return redirect('index')


class AboutView(View):
    template_name = 'pages/about.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'Image Classifier'})


class RegistrationView(View):
    form_class = SignUpForm
    template_name = 'pages/registration.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect('login')
        context = {
            'form': form
        }

        return render(request, self.template_name, context=context)


class LoginView(View):
    form_class = LoginForm
    template_name = 'pages/login.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and check_password(password, user.password):
                login(request, user)
                return redirect('index')
            else:
                info(request, 'Username or password is incorrect')

        return render(request, self.template_name, {'form': form})


class LogOutView(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'pages/profile.html'
    model = ImageManager

    def get(self, request, *args, **kwargs):
        images = self.model.objects.filter(user_id=request.user.id).order_by('-uploaded_at')
        return render(request, self.template_name, context={'title': 'Web assistant', 'images': images})
