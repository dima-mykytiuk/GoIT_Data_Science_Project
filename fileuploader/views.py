from django.shortcuts import render, redirect

from django.views import View
from fileuploader.forms import UploadFile
from fileuploader.models import ImageManager, NeuralModel
from fileuploader.keras_model import image_classify
from datetime import datetime, timezone, timedelta

# Create your views here.


class IndexView(View):
    template_name = 'pages/index.html'
    form_class = UploadFile
    context = {}
    
    def get(self, request, *args, **kwargs):
        self.context.update({'title': 'Image Classifier'})
        self.context.update({'form': self.form_class})
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
            document = ImageManager.objects.create(file_name=file, model_type=neural_model)
            document.save()
            document_path = document.file_name.path
            result = image_classify(document_path, model_path)
            if result != ["Invalid photo"]:
                document.model_prediction = result[0]
                document.predicted = True
                document.save()
            self.context.update({'image': document})
            self.context.update({'result': result})
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
    