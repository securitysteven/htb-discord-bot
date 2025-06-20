from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


def generate_certificate(name, events, credits):
    # In-memory PDF buffer
    buffer = io.BytesIO()

    # Set up PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Draw text
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "Certificate of Attendance")

    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 150, f"Awarded to: {name}")

    event_text = ", ".join(events)
    c.drawCentredString(width / 2, height - 200, f"For attending: {event_text}")

    c.drawCentredString(width / 2, height - 250, f"Total CPE Credits: {credits}")

    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, 100, "Issued by Your Organization")

    # Finalize
    c.showPage()
    c.save()

    # Move to beginning of buffer
    buffer.seek(0)
    return buffer
