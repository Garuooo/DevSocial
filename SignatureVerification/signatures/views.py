from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import Signature, Verify, Note
from .forms import SignatureForm, VerifyForm, NoteForm
import tensorflow as tf
import os
import tensorflow as tf
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
siamese_model = tf.keras.models.load_model(
    os.path.join(os.getcwd(), "siamesemodel_updated2.tf"))


@login_required(login_url="login")
def signatures(request):
    signatures = Signature.objects.filter(owner=request.user.profile)
    context = {"signatures": signatures}
    return render(request, 'signatures/signatures.html', context)


@login_required(login_url="login")
def signature(request, pk):
    signature = Signature.objects.get(id=pk)
    if signature.owner != request.user.profile:
        messages.error(request, "Your are the owner of this account")
        return redirect("profiles")
    tags = signature.tags.all()
    context = {"pk": pk, "signature": signature, "tags": tags}
    return render(request, 'signatures/signature.html', context)


def preprocess(image):
    # read image from file path
    path = str(settings.MEDIA_ROOT) + "/" + image.name
    decoded_file = tf.io.read_file(path)
    img = tf.io.decode_image(decoded_file)
    img = tf.image.resize(img, size=(100, 100))
    img = tf.cast(img, tf.float32)/255.0
    img = tf.expand_dims(img, axis=0)
    return img


@login_required
def create_signature(request):
    value = "create"
    form = SignatureForm()
    if request.method == 'POST':
        signature = SignatureForm(request.POST, request.FILES)
        if signature.is_valid():
            signature = signature.save()
            signature.owner = request.user.profile
            signature.save()
            return redirect('signatures')
    context = {'form': form, "value": value}
    return render(request, 'signatures/signature_form.html', context)


@login_required
def update_signature(request, pk):
    value = "signature"
    try:
        singature_instance = Signature.objects.get(id=pk)
    except:
        return HttpResponse("Invalid Signature")

    if request.user.profile != singature_instance.owner:
        messages.error("You are not the owner of this signature")
        return redirect("profiles")

    form = SignatureForm(instance=singature_instance)

    if request.method == "POST":
        new_signature = SignatureForm(
            request.POST, request.FILES, instance=singature_instance)
        if new_signature.is_valid():
            new_signature.save()
            return redirect('signatures')

    context = {'form': form, "value": value}
    return render(request, 'signatures/signature_form.html', context)


@login_required(login_url="login")
def delete_signature(request, pk):
    try:
        singature_instance = Signature.objects.get(id=pk)
    except:
        return HttpResponse("Invalid signature")

    if request.user.profile != singature_instance.owner:
        messages.error("You are not the owner of this signature")
        return redirect("profiles")

    if request.method == 'POST':
        singature_instance.delete()
        return redirect('signatures')

    return render(request, 'signatures/delete_signature.html')


@login_required(login_url="login")
def verify_two_signatures(request):
    form = VerifyForm()
    if request.method == "POST":
        try:
            form = VerifyForm(request.POST, request.FILES)
            verify = form.save(commit=False)
            verify.owner = request.user.profile
            verify.save()
        except:
            messages.error(request, "Invalid request")
            return redirect("verify_two_signatures")

        first_signature = preprocess(verify.first_signature)
        second_signature = preprocess(verify.second_signature)
        prediction = siamese_model.predict((first_signature, second_signature))
        print(prediction)
        if prediction >= 0.5:
            prediction = "Valid"
        else:
            prediction = "Invalid"
        verify.prediction = prediction
        verify.save()
        context = {"prediction": prediction}
        return render(request, "signatures/verification_result.html", context)
    return render(request, "signatures/verify_two_signatures.html", context={"form": form})


@login_required(login_url='login')
def create_note(request, pk):
    profile = request.user.profile
    try:
        signature = Signature.objects.get(id=pk)
    except:
        messages.error(request, 'Signature Not Found')
        return redirect("signatures")
    if signature.owner != profile:
        messages.error("You are not the owner")
        return redirect("signatures")
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = profile
            note.signature = signature
            note.save()
            return redirect("signatures")
    context = {"form": form}
    return render(request, "signatures/note.html", context)


@login_required(login_url='login')
def update_note(request, pk):
    profile = request.user.profile
    try:
        signature = Signature.objects.get(id=pk)
    except:
        messages.error(request, 'Signature Not Found')
        return redirect("signatures")
    if signature.owner != profile:
        messages.error("You are not the owner")
        return redirect("signatures")
    note = signature.note
    form = NoteForm(request.POST, instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
        return redirect("signature", signature.id)
    context = {"form": form}
    return render(request, "signatures/note.html", context)


@login_required(login_url='login')
def delete_note(request, pk):
    profile = request.user.profile
    try:
        signature = Signature.objects.get(id=pk)
    except:
        messages.error(request, 'Signature Not Found')
        return redirect("signatures")
    if signature.owner != profile:
        messages.error("You are not the owner")
        return redirect("signatures")
    note = signature.note
    if request.method == "POST":
        note.delete()
        return redirect("signature", signature.id)
    context = {}
    return render(request, "signatures/delete_note.html")
