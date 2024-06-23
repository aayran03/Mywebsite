# medicines/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine
from .forms import MedicineForm


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

def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'medicines/delete_medicine.html', {'medicine': medicine})