from django.shortcuts import render,redirect
from .models import Drug
from django.contrib import messages

def doctor_as_dev(request):
    if request.method == "POST":
        generic = request.POST.get("generic")
        indication = request.POST.get("indication")
        contraindication = request.POST.get("contraindication")
        side_effect = request.POST.get("side_effect")

        drugs = Drug.objects.filter(generic=generic)
        for drug in drugs:
            drug.indication = indication
            drug.contraindication = contraindication
            drug.side_effect = side_effect
        
        messages.add_message(request,messages.INFO, f"Properties for {generic} added successfully!")
        return redirect('index')
        

    with open('/home/uch/prescribemate/core/corefiles/generic_names.xlsx','r') as file:
        lines = [line for line in file]
        generics = [line.rstrip('\n') for line in lines]
    context = {
        'generics': generics,
    }
    return render(request,'core/doctor_as_dev.html',context)