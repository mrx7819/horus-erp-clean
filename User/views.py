from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from .forms import RegistroForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt

User = get_user_model()  # Obtén el modelo de usuario personalizado

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Busca al usuario por email en el modelo personalizado
            user = User.objects.get(email=email)
            # Genera un token de recuperación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            # Enviar el email de recuperación
            send_mail(
                'Recuperación de contraseña',
                f'Usa el siguiente enlace para restablecer tu contraseña: {reset_link}',
                'vi.fraile@duocuc.cl',  # Cambia a tu correo
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Hemos enviado un enlace de recuperación a tu correo.')
            return redirect('login')  # Redirige a la página de login
        except User.DoesNotExist:
            messages.error(request, 'No se encontró un usuario con ese email.')
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        # Decodifica el ID del usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Tu contraseña se ha actualizado con éxito!')
                return redirect('login')  # Redirige al login después de restablecer
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, 'El enlace de restablecimiento no es válido o ha expirado.')
        return redirect('forgot_password')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            print("Formulario válido")  # Debug
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Usar el correo como username
            user.save()
            print(f"Usuario creado: {user.username}")  # Debug
            login(request, user)
            return redirect('login')
        else:
            print(f"Errores en el formulario: {form.errors}")  # Debug
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Cambia esto a la URL que prefieras después del login exitoso
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ver_reporte(request):
    """
    Vista para renderizar la página de reportes con las cards.
    """
    return render(request, 'reportes/ver_reporte.html')

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from Venta.models import Venta, Detalle_Venta
from collections import Counter


def reporte_ventas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    # Crear el documento PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título del reporte
    title = Paragraph("Reporte de Ventas", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Encabezado de tabla
    data = [["Venta ID", "Cliente", "Producto", "Cantidad", "Total ($)"]]
    ventas = Venta.objects.all()

    # Datos de la tabla
    for venta in ventas:
        detalles = Detalle_Venta.objects.filter(venta=venta)
        for detalle in detalles:
            data.append([
                venta.id,
                f"{venta.cliente.nombre} {venta.cliente.apellido}",
                detalle.producto.nombre,
                detalle.cantidad,
                f"${detalle.total_venta:,.2f}"
            ])

    # Crear la tabla
    table = Table(data, colWidths=[60, 120, 120, 60, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)

    # Generar el PDF
    pdf.build(elements)
    return response


def reporte_clientes_compras(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_clientes_compras.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Reporte de Clientes con Más Compras", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    ventas = Venta.objects.all()
    clientes = Counter([venta.cliente for venta in ventas])
    clientes_ordenados = clientes.most_common()

    data = [["Cliente", "Compras Realizadas"]]
    for cliente, cantidad in clientes_ordenados:
        data.append([f"{cliente.nombre} {cliente.apellido}", cantidad])

    table = Table(data, colWidths=[200, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)

    pdf.build(elements)
    return response


from collections import defaultdict

def reporte_productos_vendidos(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos_vendidos.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title = Paragraph("Reporte de Productos Más Vendidos", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Ajustar el cálculo de productos vendidos
    productos = defaultdict(int)
    detalles = Detalle_Venta.objects.all()

    for detalle in detalles:
        productos[detalle.producto] += detalle.cantidad

    # Ordenar los productos por cantidad vendida
    productos_ordenados = sorted(productos.items(), key=lambda x: x[1], reverse=True)

    # Crear la tabla
    data = [["Producto", "Cantidad Vendida"]]
    for producto, cantidad in productos_ordenados:
        data.append([producto.nombre, cantidad])

    # Aplicar estilo a la tabla
    table = Table(data, colWidths=[200, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    elements.append(table)

    # Generar el PDF
    pdf.build(elements)
    return response



def reporte_ganancias_netas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ganancias_netas.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Reporte de Ganancias Netas", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    total_ganancias = 0
    detalles = Detalle_Venta.objects.all()
    data = [["Producto", "Ganancia ($)"]]

    for detalle in detalles:
        ganancia = detalle.cantidad * (detalle.precio_unitario - detalle.producto.precio_compra)
        total_ganancias += ganancia
        data.append([detalle.producto.nombre, f"${ganancia:,.2f}"])

    data.append(["Total Ganancias", f"${total_ganancias:,.2f}"])

    table = Table(data, colWidths=[200, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)

    pdf.build(elements)
    return response

import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
from collections import defaultdict
from Venta.models import Venta, Detalle_Venta

def reporte_ventas_diarias(request):
    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas_diarias.pdf"'

    # Crear el documento PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Generar datos de ventas diarias
    hoy = datetime.now()
    hace_siete_dias = hoy - timedelta(days=7)

    ventas = Venta.objects.filter(fecha_creacion__gte=hace_siete_dias, fecha_creacion__lte=hoy)
    ventas_por_dia = defaultdict(list)

    for venta in ventas:
        ventas_por_dia[venta.fecha_creacion.date()].append(venta)

    # Preparar datos para el gráfico
    fechas_ordenadas = sorted(ventas_por_dia.keys())
    cantidades = [len(ventas_por_dia[fecha]) for fecha in fechas_ordenadas]
    etiquetas_fechas = [fecha.strftime('%d-%b') for fecha in fechas_ordenadas]

    # Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(etiquetas_fechas, cantidades, color='skyblue')
    ax.set_title('Ventas Diarias (Últimos 7 Días)', fontsize=14)
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Cantidad de Ventas', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Guardar gráfico en memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    # Agregar gráfico al PDF
    img = Image(buffer, width=400, height=200)
    elements.append(img)

    # Agregar título descriptivo
    elements.append(Paragraph("Ventas Diarias (Últimos 7 días)", styles['Heading2']))
    elements.append(Paragraph("<br/>", styles['Normal']))

    # Agregar detalles de ventas
    for fecha, ventas_list in ventas_por_dia.items():
        elements.append(Paragraph(f"<b>{fecha}:</b> {len(ventas_list)} ventas", styles['Heading3']))
        
        for venta in ventas_list:
            detalles = Detalle_Venta.objects.filter(venta=venta)
            for detalle in detalles:
                elements.append(Paragraph(
                    f"- {detalle.cantidad} productos de: {detalle.producto.nombre} (Venta ID: {venta.id})", 
                    styles['Normal']
                ))
        elements.append(Paragraph("<br/>", styles['Normal']))

    # Construir el PDF
    pdf.build(elements)
    return response

@login_required
def ver_manual(request):
    """
    Vista para renderizar la página de reportes con las cards.
    """
    return render(request, 'manual/ver_manual.html')