from django.shortcuts import render # type: ignore
from decimal import Decimal
from django.db import models # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from Venta.models import Venta, Detalle_Venta
from Inventario.models import Producto
from Cliente.models import Cliente
from django.shortcuts import render, redirect # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.http import JsonResponse # type: ignore
from django.db import transaction # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from django.db.models import F # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from django.db.models import Sum, F, ExpressionWrapper, DecimalField # type: ignore
import requests 
from decimal import Decimal
from django.templatetags.static import static # type: ignore
from django.utils.timezone import now, timedelta # type: ignore
from django.contrib import messages # type: ignore
import json
from django.core.serializers.json import DjangoJSONEncoder
from Inventario.models import Bodega
from Proveedor.models import Pedido
# Create your views here.
@login_required
@csrf_exempt  # Permitir solicitudes AJAX
def eliminar_detalle(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        try:
            # Aquí podrías buscar el detalle por el ID del producto (o cualquier otro criterio)
            detalle = Detalle_Venta.objects.get(producto_id=producto_id)
            detalle.delete()
            return JsonResponse({'success': True})
        except Detalle_Venta.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Detalle no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def get_producto_precio(request, producto_id):
    """
    Retorna el precio de venta de un producto dado su ID.
    """
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'success': True, 'precio_venta': float(producto.precio_venta)})
    except Producto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
    
@login_required
def listarVenta(request):
    # Prefetch los detalles para optimizar la consulta
    ventas = Venta.objects.filter(user=request.user).prefetch_related('detalle_venta_set__producto')

    # Calcular el total de la venta sumando los total_venta de los detalles
    for venta in ventas:
        venta.total_venta_calculado = sum(detalle.total_venta for detalle in venta.detalle_venta_set.all())

    return render(request, 'crud_ventas/listar_venta.html', {'ventas': ventas})






@login_required
def agregarVenta(request):
    if request.method == 'POST':
        print("Se recibió un POST en agregarVenta.")
        print(f"Datos recibidos: cliente_id={request.POST.get('cliente')}, metodo_pago={request.POST.get('metodo_pago')}, estado={request.POST.get('estado')}")

        # Validar los campos requeridos para Venta
        if all([
            request.POST.get('cliente'),
            request.POST.get('metodo_pago'),
            request.POST.get('estado')
        ]):
            try:
                with transaction.atomic():
                    # Crear la Venta
                    venta = Venta.objects.create(
                        cliente_id=request.POST.get('cliente'),
                        metodo_pago=request.POST.get('metodo_pago'),
                        estado=request.POST.get('estado'),
                        user=request.user,
                    )
                    print(f"Venta guardada con ID: {venta.id}")

                    # Manejar los detalles de la venta
                    productos = request.POST.getlist('productos[]')
                    cantidades = request.POST.getlist('cantidades[]')
                    precios = request.POST.getlist('precios[]')
                    descuentos = request.POST.getlist('descuentos[]')

                    for i in range(len(productos)):
                        producto_id = int(productos[i])
                        cantidad_vendida = int(cantidades[i])

                        # Obtener el producto y su bodega
                        producto = get_object_or_404(Producto, pk=producto_id, user=request.user)
                        bodega = producto.bodega

                        # Verificar stock suficiente
                        if producto.cantidad < cantidad_vendida:
                            raise ValueError(f"Stock insuficiente para el producto {producto.nombre}.")

                        # Calcular subtotal y total con descuento
                        precio_unitario = float(precios[i])
                        descuento = float(descuentos[i]) if descuentos[i] else 0.0
                        subtotal = cantidad_vendida * precio_unitario
                        total_final = subtotal * (1 - (descuento / 100))

                        # Crear el detalle de la venta
                        detalle = Detalle_Venta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad_vendida,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            total_venta=max(total_final, 0),
                            user=request.user,
                            fecha_creacion=now(),
                        )
                        print(f"Detalle creado para producto {producto.nombre} con cantidad {cantidad_vendida}")

                        # Actualizar la cantidad del producto y de la bodega directamente en la base de datos
                        Producto.objects.filter(pk=producto.pk).update(cantidad=F('cantidad') - cantidad_vendida)
                        Bodega.objects.filter(pk=bodega.pk).update(
                            cantidad_art=F('cantidad_art') - cantidad_vendida,
                            capacidad=F('capacidad') + cantidad_vendida
                        )
                        print(f"Producto {producto.nombre} y Bodega {bodega.nombre} actualizados.")

                    print("Venta procesada con éxito.")
                    messages.success(request, 'Venta registrada exitosamente.')
                    return redirect('listarVenta')

            except Exception as e:
                print(f"Error: {str(e)}")
                messages.error(request, f"Error al procesar la venta: {str(e)}")
                return render(request, 'crud_ventas/agregar_venta.html', {
                    'error': f"Error al procesar la venta: {str(e)}",
                    'clientes': Cliente.objects.filter(user=request.user),
                    'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
                    'estado_choices': Venta.ESTADO_CHOICES,
                    'productos': Producto.objects.filter(user=request.user),
                })
        else:
            print("Campos obligatorios faltantes.")
            messages.error(request, "Faltan campos obligatorios para registrar la venta.")
            return render(request, 'crud_ventas/agregar_venta.html', {
                'error': 'Faltan campos obligatorios',
                'clientes': Cliente.objects.filter(user=request.user),
                'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
                'estado_choices': Venta.ESTADO_CHOICES,
                'productos': Producto.objects.filter(user=request.user),
            })

    else:
        return render(request, 'crud_ventas/agregar_venta.html', {
            'clientes': Cliente.objects.filter(user=request.user),
            'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
            'estado_choices': Venta.ESTADO_CHOICES,
            'productos': Producto.objects.filter(user=request.user),
        })


@login_required
def modificarVenta(request, idVenta):
    try:
        ventas = Venta.objects.filter(user=request.user)

        if request.method == 'POST':
            print("Datos POST recibidos:", request.POST)

            if (
                request.POST.get('id') and
                request.POST.get('cliente') and
                request.POST.get('metodo_pago') and
                request.POST.get('estado')
            ):
                venta_id = request.POST.get('id')
                venta = Venta.objects.get(pk=venta_id)

                with transaction.atomic():
                    # Actualizar información de la venta
                    venta.cliente_id = request.POST.get('cliente')
                    venta.metodo_pago = request.POST.get('metodo_pago')
                    venta.estado = request.POST.get('estado')
                    venta.save()
                    print(f"Venta {venta.id} actualizada")

                    # Reponer el stock de los productos relacionados con los detalles antiguos
                    for detalle in venta.detalle_venta_set.all():
                        producto = detalle.producto
                        producto.cantidad += detalle.cantidad  # Reponer stock
                        producto.save()
                        print(f"Stock repuesto para producto {producto.nombre}")

                    # Eliminar los detalles antiguos
                    venta.detalle_venta_set.all().delete()
                    print("Detalles antiguos eliminados")

                    # Manejar los nuevos detalles
                    productos = request.POST.getlist('productos[]')
                    cantidades = request.POST.getlist('cantidades[]')
                    precios = request.POST.getlist('precios[]')
                    descuentos = request.POST.getlist('descuentos[]')

                    for i in range(len(productos)):
                        producto_id = productos[i]
                        cantidad_vendida = int(cantidades[i])

                        # Obtener producto y verificar stock suficiente
                        producto = get_object_or_404(Producto, pk=producto_id)
                        if producto.cantidad < cantidad_vendida:
                            raise ValueError(f"Stock insuficiente para el producto {producto.nombre}.")

                        # Calcular subtotal y total con descuento
                        precio_unitario = float(precios[i]) if precios[i] else float(producto.precio_venta)
                        descuento = float(descuentos[i]) if descuentos[i] else 0.0
                        subtotal = cantidad_vendida * precio_unitario
                        total_final = subtotal * (1 - (descuento / 100))

                        # Crear el nuevo detalle de venta
                        Detalle_Venta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad_vendida,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            total_venta=max(total_final, 0),
                            user=request.user,
                        )
                        print(f"Detalle creado para producto {producto.nombre} con cantidad {cantidad_vendida}")

                        # Reducir el stock del producto
                        producto.cantidad -= cantidad_vendida
                        producto.save()

                    messages.success(request, 'Venta modificada exitosamente.')
                    return redirect('listarVenta')
            else:
                print("Error: Faltan campos obligatorios")
                messages.error(request, 'Faltan campos obligatorios.')
                raise ValueError("Campos incompletos.")

        else:
            venta = get_object_or_404(Venta, pk=idVenta) if idVenta != 0 else None
            return render(request, 'crud_ventas/modificar_venta.html', {
                'venta': venta,
                'ventas': ventas,
                'clientes': Cliente.objects.filter(user=request.user),
                'metodo_pago_choices': Venta.METODO_PAGO_CHOICES,
                'estado_choices': Venta.ESTADO_CHOICES,
                'productos': Producto.objects.filter(user=request.user),
            })

    except Venta.DoesNotExist:
        messages.error(request, 'La venta solicitada no existe.')
        return redirect('listarVenta')
    except Exception as e:
        messages.error(request, f'Error al modificar la venta: {e}')
        return redirect('listarVenta')




@login_required
def eliminarVenta(request, idVenta):
    ventas = Venta.objects.all().select_related('cliente')  # Asegúrate de incluir los datos del cliente

    try:
        if request.method == 'POST':
            venta_id = request.POST.get('id')
            if venta_id:
                venta_a_eliminar = Venta.objects.get(pk=venta_id)

                with transaction.atomic():
                    # Reponer stock antes de eliminar la venta
                    for detalle in venta_a_eliminar.detalle_venta_set.all():
                        detalle.producto.cantidad += detalle.cantidad
                        detalle.producto.save(update_fields=["cantidad"])
                        detalle.producto.bodega.cantidad_art += detalle.cantidad
                        detalle.producto.bodega.save(update_fields=["cantidad_art"])

                    # Eliminar la venta
                    venta_a_eliminar.delete()

                messages.success(request, f"Venta ID {venta_id} eliminada exitosamente.")
                return redirect('listarVenta')
            else:
                messages.error(request, "Debe seleccionar una venta para eliminar.")

        venta = Venta.objects.get(pk=idVenta) if idVenta != 0 else None

        # Serializar las ventas a JSON
        ventas_json = json.dumps(
            list(ventas.values('id', 'cliente__nombre', 'cliente__apellido', 'estado', 'metodo_pago', 'fecha_creacion')),
            cls=DjangoJSONEncoder
        )

        return render(request, 'crud_ventas/eliminar_venta.html', {
            'ventas': ventas,
            'venta': venta,
            'ventas_json': ventas_json  # Pasar el JSON serializado al template
        })

    except Venta.DoesNotExist:
        messages.error(request, "La venta seleccionada no existe.")
        return redirect('listarVenta')

    except Exception as e:
        messages.error(request, f"Error al intentar eliminar la venta: {e}")
        return render(request, 'crud_ventas/eliminar_venta.html', {
            'ventas': ventas,
            'venta': None,
            'error': f"Error al intentar eliminar la venta: {e}",
        })





class VentasPorProductoAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Agrupar las ventas por producto
        ventas = Detalle_Venta.objects.values('producto__nombre').annotate(total_ventas=models.Sum('total_venta'))
        
        # Formatear los datos para el gráfico
        labels = [venta['producto__nombre'] for venta in ventas]
        data = [venta['total_ventas'] for venta in ventas]

        return Response({'labels': labels, 'data': data})

class GananciasTotalesAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Calcular ganancias en pesos chilenos
        ganancias_query = Detalle_Venta.objects.annotate(
            ganancia=ExpressionWrapper(
                (F('precio_unitario') - F('producto__precio_compra')) * F('cantidad'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).aggregate(total_ganancias=Sum('ganancia'))

        ganancias_totales_clp = ganancias_query.get('total_ganancias', 0) or Decimal(0)

        # Obtener tasa de cambio para USD
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/CLP')
            response.raise_for_status()
            tasa_cambio = Decimal(response.json().get('rates', {}).get('USD', 1))
        except Exception as e:
            print(f"Error al obtener la tasa de cambio: {e}")
            tasa_cambio = Decimal(1)

        # Calcular ganancias en dólares
        ganancias_totales_usd = ganancias_totales_clp * tasa_cambio

        return Response({
            'ganancias_totales_usd': round(ganancias_totales_usd, 2),
            'ganancias_totales_clp': round(ganancias_totales_clp, 0),
        })


class ProductosVendidosAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Agrupar las ventas por producto y sumar la cantidad vendida
        productos_vendidos = (
            Detalle_Venta.objects.values('producto__nombre')  # Agrupar por nombre del producto
            .annotate(ventas=Sum('cantidad'))  # Sumar la cantidad vendida
            .order_by('-ventas')  # Ordenar por cantidad descendente
        )
        
        # Formatear los datos para el frontend
        data = [
            {'nombre': producto['producto__nombre'], 'ventas': producto['ventas']}
            for producto in productos_vendidos
        ]

        return Response(data)
    
class ProductoEstrellaAPI(APIView):
    def get(self, request, *args, **kwargs):
        producto_estrella = (
            Detalle_Venta.objects
            .values('producto__id', 'producto__nombre', 'producto__img')
            .annotate(total_vendido=Sum('cantidad'))
            .order_by('-total_vendido')
            .first()
        )

        if producto_estrella:
            # Asegúrate de usar solo una vez el prefijo 'static/'
            imagen_url = f"/{producto_estrella['producto__img'].lstrip('/')}" if producto_estrella['producto__img'] else None
            data = {
                'id': producto_estrella['producto__id'],
                'nombre': producto_estrella['producto__nombre'],
                'imagen_url': imagen_url,  # Generar correctamente la URL
                'cantidad_vendida': producto_estrella['total_vendido']
            }
        else:
            data = {'error': 'No hay productos registrados'}

        return Response(data)
    
def obtener_ingresos():
    hoy = now().date()
    ayer = hoy - timedelta(days=1)

    # Ingresos de hoy
    ingresos_hoy = Detalle_Venta.objects.filter(venta__fecha_creacion__date=hoy).aggregate(Sum('total_venta'))['total_venta__sum'] or 0

    # Ingresos de ayer
    ingresos_ayer = Detalle_Venta.objects.filter(venta__fecha_creacion__date=ayer).aggregate(Sum('total_venta'))['total_venta__sum'] or 0

    # Cambio respecto a ayer
    cambio_porcentaje = 0
    if ingresos_ayer > 0:
        cambio_porcentaje = ((ingresos_hoy - ingresos_ayer) / ingresos_ayer) * 100

    return {
        "ingresos_hoy": round(ingresos_hoy, 2),
        "cambio_porcentaje": round(cambio_porcentaje, 2)
    }



def api_ingresos_diarios(request):
    datos = obtener_ingresos()
    return JsonResponse(datos)

class CategoriaMasVendidaAPI(APIView):
    def get(self, request, *args, **kwargs):
        categoria_mas_vendida = (
            Detalle_Venta.objects
            .values('producto__categoria__nombre')  # Agrupar por categoría
            .annotate(total_vendido=Sum('cantidad'))  # Sumar la cantidad vendida
            .order_by('-total_vendido')  # Ordenar por total descendente
            .first()
        )

        if categoria_mas_vendida:
            data = {
                'categoria': categoria_mas_vendida['producto__categoria__nombre'],
                'total_vendido': categoria_mas_vendida['total_vendido']
            }
        else:
            data = {'error': 'No hay datos de ventas disponibles.'}

        return Response(data)

class ClienteMasComprasAPI(APIView):
    def get(self, request, *args, **kwargs):
        cliente_mas_compras = (
            Venta.objects
            .values('cliente__nombre', 'cliente__apellido')  # Agrupar por cliente
            .annotate(total_compras=Sum('detalle_venta__total_venta'))  # Sumar el total de las compras
            .order_by('-total_compras')  # Ordenar por total descendente
            .first()
        )

        if cliente_mas_compras:
            data = {
                'nombre': f"{cliente_mas_compras['cliente__nombre']} {cliente_mas_compras['cliente__apellido']}",
                'total_compras': round(cliente_mas_compras['total_compras'], 2)
            }
        else:
            data = {'error': 'No hay datos de clientes disponibles.'}

        return Response(data)

class EgresosAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Calcular el total de egresos por pedidos
        total_pedidos = Pedido.objects.aggregate(total_egresos=Sum('total'))['total_egresos'] or 0.0
        total_pedidos = Decimal(total_pedidos)  # Convertir a Decimal para evitar conflictos de tipo

        # Calcular el costo total de los productos en inventario
        total_inventario = Producto.objects.aggregate(
            total_costo_inventario=Sum(F('precio_compra') * F('cantidad'), output_field=models.DecimalField())
        )['total_costo_inventario'] or Decimal(0)

        # Sumar ambos valores para obtener los egresos totales
        egresos_totales = total_pedidos + total_inventario

        return Response({
            'egresos_totales': round(egresos_totales, 2),
            'total_pedidos': round(total_pedidos, 2),
            'total_inventario': round(total_inventario, 2),
        })