from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import ContactMessage


def home(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not subject or not message:

            messages.error(
                request,
                "Veuillez remplir tous les champs du formulaire."
            )

        else:

            try:
                validate_email(email)

            except ValidationError:

                messages.error(
                    request,
                    "Veuillez entrer une adresse email valide."
                )

            else:

                # ==============================
                # ENREGISTRER DANS LA BASE
                # ==============================

                contact_message = ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                )

                # ==============================
                # ENVOYER PAR EMAIL
                # ==============================

                full_message = (
                    f"Nom : {name}\n"
                    f"Email : {email}\n\n"
                    f"Message :\n{message}"
                )

                try:

                    email_message = EmailMessage(
                        subject=f"Portfolio - {subject}",
                        body=full_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[settings.CONTACT_EMAIL],
                        reply_to=[email],
                    )

                    email_message.send(fail_silently=False)

                    messages.success(
                        request,
                        "Votre message a été envoyé avec succès. Merci de m'avoir contacté."
                    )

                    return redirect(
                        reverse("home") + "#contact"
                    )

                except Exception:

                    messages.warning(
                        request,
                        "Votre message a été enregistré, mais l'envoi de l'email a échoué."
                    )

                    return redirect(
                        reverse("home") + "#contact"
                    )

    return render(request, "core/home.html")