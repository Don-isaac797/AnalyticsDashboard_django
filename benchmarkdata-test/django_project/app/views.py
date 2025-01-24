import requests
import json
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views import View
from .forms import ContactForm, ContactFormSet, FilesForm



# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField:
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class GetParametersMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", None)
        context["size"] = self.request.GET.get("size", None)
        return context


class DefaultFormsetView(GetParametersMixin, FormView):
    template_name = "app/formset.html"
    form_class = ContactFormSet


class DefaultFormView(GetParametersMixin, FormView):
    template_name = "app/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(GetParametersMixin, FormView):
    template_name = "app/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(GetParametersMixin, FormView):
    template_name = "app/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(GetParametersMixin, FormView):
    template_name = "app/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(GetParametersMixin, FormView):
    template_name = "app/form_with_files.html"
    form_class = FilesForm

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "app/pagination.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append(f"Line {i + 1}")
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "app/misc.html"


'''

class AnalyticsView(View):
    template_name = "app/analytics.html"

    def get(self, request):
        # Define the JWT token
        jwt_token = "your_secure_token"
        
        # Define the headers with the JWT token
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        # Define the data to be sent in the POST request
        data = [       
                {
                    'analytics_id': item.get('analytics_id'),
                    'user_id': item.get('user_id'),
                    'log_image': item.get('log_image'),
                    'log_video': item.get('log_video'),
                    'create_date': item.get('create_date'),
                    'message': item.get('message'),
                    'camera_id': item.get('camera_id'),
                    'camera_location': item.get('camera_location'),
                    'action': item.get('action'),
                    'status': item.get('status'), 
                }
                for item in analytics_data
            ]
            
        
        # Make the POST request to the Flask API with the headers and data
        response = requests.post('http://127.0.0.1:5000/analytics-viewall', headers=headers, data=json.dumps(data))
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                analytics_data = response.json()
                print(f"Analytics Data: {analytics_data}")
            except ValueError:
                analytics_data = []
                print("Error: Unable to parse JSON response")
        else:
            analytics_data = []
            print(f"Error: Received unexpected status code {response.status_code}")
            print(f"Response Content: {response.content}")

        return render(request, self.template_name, {'analytics_data': analytics_data})

'''

class AnalyticsView(View):
    template_name = "app/analytics.html"

    def get(self, request):
        # Define the JWT token
        jwt_token = "your_secure_token"
        
        # Define the headers with the JWT token
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        # Define the data to be sent in the POST request
        data = {
            "token": jwt_token,
            "row_count": 100  # Replace with actual data if needed
        }
        
        # Make the POST request to the Flask API with the headers and data
        response = requests.get('http://127.0.0.1:5000/analytics-viewall', headers=headers, data=json.dumps(data))
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                response_json = response.json()
                analytics_data = response_json.get('data', [])
                print(f"Analytics Data: {analytics_data}")
            except ValueError:
                analytics_data = []
                print("Error: Unable to parse JSON response")
        else:
            analytics_data = []
            print(f"Error: Received unexpected status code {response.status_code}")
            print(f"Response Content: {response.content}")

        return render(request, self.template_name, {'analytics_data': analytics_data})
    
'''# CAMERAS VIEW
class CamerasView(View):
    template_name = "app/cameras.html"

    def get(self, request):
        # Define the JWT token
        jwt_token = "your_secure_token"
        
        # Define the headers with the JWT token
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        # Define the data to be sent in the POST request
        data = {
            "token": jwt_token,
            "row_count": 100  # Replace with actual data if needed
        }
        
        # Make the POST request to the Flask API with the headers and data
        response = requests.post('http://127.0.0.1:5000/camera-viewall', headers=headers, data=json.dumps(data))
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                response_json = response.json()
                cameras_data = response_json.get('data', [])
                print(f"Cameras Data: {cameras_data}")
            except ValueError:
                cameras_data = []
                print("Error: Unable to parse JSON response")
        else:
            analytics_data = []
            print(f"Error: Received unexpected status code {response.status_code}")
            print(f"Response Content: {response.content}")

        return render(request, self.template_name, {'cameras_data': cameras_data})    
'''
'''
#new version
def analytics_view(request):
    response = requests.get('http://127.0.0.1:5000/analytics-viewall')
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        try:
            analytics_data = response.json()

        except ValueError:
            analytics_data = []
            print("Error: Unable to parse JSON response")    
    else:
        analytics_data = []
        print(f"Error: Received unexpected status code {response.status_code}")

    processed_data = [
        {
            'analytics_id': item.get('analytics_id'),
            'log_image': item.get('log_image'),
            'log_video': item.get('log_video'),
            'create_date': item.get('create_date'),
            'message': item.get('message'),
            'camera_id': item.get('camera_id'),
            'camera_location': item.get('camera_location'),
            'action': item.get('action'),
            'time_to_action': item.get('time_to_action'),
            'status': item.get('status'),
            'user_id': item.get('user_id'),
        }
        for item in analytics_data
    ]

    return render(request, 'app/analytics.html', {'analytics_data': processed_data})
''' 

'''
class AnalyticsView(View):
    template_name = "app/analytics.html"

    def get(self, request):
        # Define the JWT token
        JWT_SECRET_KEY = "your_secure_token"
        
        # Define the headers with the JWT token
        headers = {
            "Authorization": f"Bearer {JWT_SECRET_KEY}"
        }
        
        # Make the POST request to the Flask API with the headers
        response = requests.get('http://127.0.0.1:5000/analytics-viewall', headers=headers)
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            try:
                analytics_data = response.json()
            except ValueError:
                analytics_data = []
                print("Error: Unable to parse JSON response")
        else:
            analytics_data = []
            print(f"Error: Received unexpected status code {response.status_code}")

        return render(request, self.template_name, {'analytics_data': analytics_data})
'''