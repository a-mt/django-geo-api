from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Commune, CodePostal
from .forms import CommuneForm

def home(request):
    return render(request, "geo/index.html", {})

def commune_create(request):
    if request.method == 'POST':

        # Save changes
        form = CommuneForm(request.POST)

        if form.is_valid():
            instance = form.save()
            instance.setCodesPostaux(set(form.cleaned_data['codesPostaux']), checkExisting=False)
            messages.success(request, 'La ville a bien été enregistrée.')

            return redirect('geo:commune_edit', code=instance.code)
    else:

        # Display form
        form = CommuneForm()

    return render(request, "geo/commune_form.html", {
        'form'    : form,
        'instance': False
    })

def commune_edit(request, code):
    instance = Commune.objects.get(code=code)

    if request.method == 'POST':

        # Delete
        if request.POST.get('delete'):
            instance.delete()
            messages.success(request, 'La ville "%s" a bien été supprimée.' % instance.nom)

            return redirect('geo:homepage')

        # Save changes
        else:
            form = CommuneForm(request.POST, instance=instance)
            if form.is_valid():
                instance = form.save()
                instance.setCodesPostaux(set(form.cleaned_data['codesPostaux']))
                messages.success(request, 'La ville a bien été enregistrée.')

                return redirect('geo:commune_edit', code=instance.code)
    else:

        # Display form
        form = CommuneForm(instance=instance)

    return render(request, "geo/commune_form.html", {
        'form'    : form,
        'instance': instance
    })