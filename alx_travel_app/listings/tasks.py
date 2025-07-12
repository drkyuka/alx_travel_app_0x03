"""tasks.py
Celery tasks for the ALX Travel App.
This module contains tasks related to booking confirmations.
"""

from celery import shared_task
from .models import Booking


@shared_task
def send_booking_confirmation_email(booking: Booking):
    """
    Sends a booking confirmation email to the user.

    Args:
        booking (Booking): The booking instance containing user and listing details.
    """
    subject = "Booking Confirmation"
    message = (
        f"Dear {booking.booked_by.name},\n\n"
        f"Your booking for {booking.listing.title} has been confirmed.\n"
        f"Booking ID: {booking.booking_id}\n"
        f"Check-in Date: {booking.check_in_date}\n"
        f"Check-out Date: {booking.check_out_date}\n\n"
        f"Thank you for choosing us!\n\nBest regards,\nThe Travel App Team"
    )

    # Assuming send_email is a utility function to send emails
    send_email(booking.host.email, booking.booked_by.email, subject, message)


def send_email(from_email, to_email, subject, message):
    """
    Utility function to send an email.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email.
    """
    # Here you would implement the actual email sending logic, e.g., using SMTP or a third-party service
    print(
        f"Sending email from {from_email} to {to_email} with subject '{subject}' and message:\n{message}"
    )
