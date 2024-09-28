from django.shortcuts import render, redirect
from .forms import newform
from .models import User,Hobby,ExcelFile  
from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.http import response
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
import os
import io


#imports for generating pdf
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle 
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


#for excel export
def export_to_excel(request):
    objs = User.objects.all()
    data = []
    for obj in objs:
        hobbies = ', '.join([hobby.name for hobby in obj.choices.all()])
        data.append({
            'id':obj.id,
            'name': obj.name,
            'age': obj.age,
            'gender': obj.get_gender_display(),  
            'country': obj.country.name, 
            'email': obj.email,
            'hobbies': hobbies  
        })
        df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output,  engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="user_details_{timestamp}.xlsx"'
    return response

#Importing excel file

def upload_xlsx(request):
    if request.method == 'POST':
        file = request.FILES.get('files') 
        if file:
            obj = ExcelFile.objects.create(file=file)
            path = os.path.join(settings.MEDIA_ROOT, str(obj.file)) 
            df = pd.read_excel(path)
            for index, row in df.iterrows():
                user = User.objects.create(
                    name=row['name'],
                    age=row['age'],
                    gender=row['gender'],
                    country=row['country'],
                    email=row['email'],
                )
                user.save()
                if 'hobbies' in row and pd.notna(row['hobbies']):
                    hobbies = row['hobbies'].split(',') 
                    for hobby_name in hobbies:
                        hobby, created = Hobby.objects.get_or_create(name=hobby_name.strip())
                        user.choices.add(hobby)
                user.save()

            print("Data successfully imported from Excel.")
        else:
            print("No file uploaded.")
    
    return render(request, 'upload_xlsx.html')


#code to export data as PDF
def venue_pdf(request):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    table_data = [['ID', 'Name', 'Age', 'Gender', 'Country', 'Email', 'Hobbies']]
    objs = User.objects.all()
    for obj in objs:
        hobbies = ', '.join([hobby.name for hobby in obj.choices.all()])
        table_data.append([
            obj.id,
            obj.name,
            obj.age,
            obj.gender,  
            obj.country, 
            obj.email,
            hobbies
        ])
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
        ('FONTSIZE', (0, 0), (-1, -1), 12),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  
    ]))
    elements.append(table)
    pdf.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="user_details_{timestamp}.pdf"'
    return response


#code for searching 
def search_view(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(
            Q(name__contains=query) | Q(email__exact=query)
        )
    else:
        results = User.objects.all()
    return render(request, 'user_detail.html', {'users': results, 'query': query})
    