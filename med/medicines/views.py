# medicines/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine
from .forms import MedicineForm
from django.contrib import messages
import csv
from datetime import datetime


def medicine_list(request):
    medicines = Medicine.objects.order_by('expiry_date') 
    return render(request, 'medicines/medicine_list.html', {'medicines': medicines})

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'medicines/add_medicine.html', {'form': form})

def upload(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        
        # Check if CSV file is uploaded
        csv_file = request.FILES.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not a CSV file.')
            else:
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader)  # Skip header row
                    
                    for row in reader:
                        try:
                            # Convert date format from DD/MM/YYYY to YYYY-MM-DD
                            expiry_date = datetime.strptime(row[2], '%d/%m/%Y').strftime('%Y-%m-%d')
                            
                            _, created = Medicine.objects.update_or_create(
                                name=row[0],
                                identification_number=row[1],
                                expiry_date=expiry_date,
                                quantity=row[3],
                            )
                        
                        except Exception as e:
                            messages.error(request, f'Error processing row in CSV: {e}')
                            continue  # Continue to the next row if error occurs
                    
                    messages.success(request, 'Medicines added successfully from CSV.')
                    return redirect('medicine_list')
                
                except Exception as e:
                    messages.error(request, f'Error processing CSV file: {e}')
    else:
        form = MedicineForm()
    return render(request, 'medicines/upload.html', {'form': form})

def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicines/delete_medicine.html', {'medicine': medicine})