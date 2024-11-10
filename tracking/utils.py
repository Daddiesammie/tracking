from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import HexColor
from io import BytesIO
import os

def generate_tracking_pdf(product):
    buffer = BytesIO()
    
    # Custom page size with margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Brand colors
    primary_color = HexColor('#312E81')  # Indigo-900
    secondary_color = HexColor('#6366F1')  # Indigo-500
    accent_color = HexColor('#E0E7FF')  # Indigo-100
    
    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=primary_color,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    # Custom heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=primary_color,
        spaceBefore=20,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    # Custom body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#1F2937'),  # Gray-800
        fontName='Helvetica'
    )
    
    elements = []
    
    # Add logo
    # logo_path = os.path.join(settings.STATIC_ROOT, 'images/logo.png')
    # if os.path.exists(logo_path):
    #     logo = Image(logo_path, width=2*inch, height=1*inch)
    #     elements.append(logo)
    
    # Title
    elements.append(Paragraph(f"Shipment Tracking Details", title_style))
    elements.append(Spacer(1, 20))
    
    # Tracking number in highlight box
    tracking_data = [[
        Paragraph(f"Tracking Number: {product.tracking_number}", body_style),
        Paragraph(f"Status: {product.get_current_status_display()}", body_style)
    ]]
    
    tracking_table = Table(tracking_data, colWidths=[doc.width/2.0]*2)
    tracking_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), accent_color),
        ('BOX', (0, 0), (-1, -1), 1, primary_color),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(tracking_table)
    elements.append(Spacer(1, 30))
    
    # Shipment Details
    elements.append(Paragraph("Shipment Details", heading_style))
    
    shipment_data = [
        ['FROM', 'TO'],
        [product.sender_name, product.recipient_name],
        [product.sender_address, product.recipient_address],
    ]
    
    shipment_table = Table(shipment_data, colWidths=[doc.width/2.0]*2)
    shipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#E5E7EB')),  # Gray-200
        ('PADDING', (0, 1), (-1, -1), 12),
    ]))
    elements.append(shipment_table)
    elements.append(Spacer(1, 30))
    
    # Tracking History
    elements.append(Paragraph("Tracking History", heading_style))
    
    for status in product.status_updates.all():
        history_data = [[
            Paragraph(f"<b>{status.get_status_display()}</b>", body_style),
            Paragraph(status.timestamp.strftime('%B %d, %Y %H:%M'), body_style)
        ], [
            Paragraph(f"Location: {status.location}", body_style),
            ''
        ], [
            Paragraph(status.description, body_style),
            ''
        ]]
        
        history_table = Table(history_data, colWidths=[doc.width * 0.7, doc.width * 0.3])
        history_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_color),
            ('BOX', (0, 0), (-1, -1), 0.5, HexColor('#E5E7EB')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('SPAN', (0, 1), (-1, 1)),
            ('SPAN', (0, 2), (-1, 2)),
        ]))
        elements.append(history_table)
        elements.append(Spacer(1, 15))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        textColor=HexColor('#6B7280'),  # Gray-500
        fontSize=8,
        alignment=1
    )
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Thank you for choosing our services", footer_style))
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
