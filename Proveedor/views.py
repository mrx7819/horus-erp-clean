from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages
from .models import *
from Proveedor.models import Giro, CategoriaGiro
from Ubicacion.models import Region, Provincia, Comuna
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from Inventario.models import Producto, Bodega
from django.db import transaction

def upload_logo(request):
    if request.method == 'POST' and request.FILES.get('logo'):
        logo = request.FILES['logo']
        
        # Validación del tipo de archivo (solo imágenes)
        if not logo.content_type.startswith('image/'):
            return JsonResponse({'success': False, 'error': 'Solo se permiten imágenes.'})
        
        file_path = os.path.join('provider_logos', logo.name)
        default_storage.save(file_path, ContentFile(logo.read()))
        return JsonResponse({'success': True, 'logo_url': default_storage.url(file_path)})
    
    return JsonResponse({'success': False})


def filtrar_comunas(request):
    comuna_codigo = request.GET.get('comuna_codigo')
    if comuna_codigo:
        comuna = get_object_or_404(Comuna, codigo_comuna=comuna_codigo)
        provincia = comuna.provincia
        region = provincia.region
        return JsonResponse({
            'success': True,
            'region': {
                'codigo': region.codigo_region,
                'nombre': region.nombre
            }
        })
    return JsonResponse({'success': False})

def get_regiones(request):
    regiones = Region.objects.all()
    data = [{'id': r.codigo_region, 'nombre': r.nombre} for r in regiones]
    return JsonResponse(data, safe=False)

def get_provincias_por_region(request, region_id):
    provincias = Provincia.objects.filter(region__codigo_region=region_id)
    data = [{'id': p.codigo_provincia, 'nombre': p.nombre} for p in provincias]
    return JsonResponse(data, safe=False)

def get_comunas_por_provincia(request, provincia_id):
    comunas = Comuna.objects.filter(provincia__codigo_provincia=provincia_id)
    data = [{'id': c.codigo_comuna, 'nombre': c.nombre} for c in comunas]
    return JsonResponse(data, safe=False)

@login_required
def listarProveedor(request):
    # Filtrar proveedores por el usuario que ha iniciado sesión
    proveedores = Proveedor.objects.filter(user=request.user)
    return render(request, 'crud_proveedores/listar_proveedor.html', {'proveedores': proveedores})


@login_required
def agregarProveedor(request):
    if request.method == 'POST':
        if (
            request.POST.get('rut') and 
            request.POST.get('nombre') and 
            request.POST.get('direccion') and 
            request.POST.get('telefono') and 
            request.POST.get('email') and 
            request.POST.get('comuna') and
            request.POST.get('provincia') and
            request.POST.get('region') and
            request.POST.get('giro')
        ):
            proveedor = Proveedor()
            proveedor.rut = request.POST.get('rut')
            proveedor.nombre = request.POST.get('nombre')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.email = request.POST.get('email')
            proveedor.comuna_id = request.POST.get('comuna')
            proveedor.provincia_id = request.POST.get('provincia')
            proveedor.region_id = request.POST.get('region')
            proveedor.giro_id = request.POST.get('giro')

            # Logo opcional
            if request.FILES.get('logo'):
                proveedor.logo = request.FILES.get('logo')

            proveedor.user = request.user
            proveedor.save()
            return redirect('listarProveedor')
        else:
            # Si no se completaron todos los campos requeridos, mostrar mensaje de error
            return render(request, 'crud_proveedores/agregar_proveedor.html')
    else:
        # Pasamos las comunas, regiones y giros disponibles al formulario
        comunas = Comuna.objects.all()
        provincias = Provincia.objects.all()
        regiones = Region.objects.all()
        giros = Giro.objects.all()
        return render(request, 'crud_proveedores/agregar_proveedor.html', {
            'comunas': comunas,
            'regiones': regiones,
            'provincias': provincias,
            'giros': giros
        })




@login_required
def modificarProveedor(request, idProveedor):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('rut') and 
                request.POST.get('nombre') and 
                request.POST.get('direccion') and 
                request.POST.get('telefono') and 
                request.POST.get('email') and 
                request.POST.get('comuna') and
                request.POST.get('provincia') and
                request.POST.get('region') and
                request.POST.get('giro')
            ):
                proveedor_id_old = request.POST.get('id')
                proveedor_old = Proveedor.objects.get(id=proveedor_id_old)

                proveedor = Proveedor()
                proveedor.id = request.POST.get('id')
                proveedor.rut = request.POST.get('rut')
                proveedor.nombre = request.POST.get('nombre')
                proveedor.direccion = request.POST.get('direccion')
                proveedor.telefono = request.POST.get('telefono')
                proveedor.email = request.POST.get('email')
                proveedor.comuna_id = request.POST.get('comuna')
                proveedor.provincia_id = request.POST.get('provincia')
                proveedor.region_id = request.POST.get('region')
                proveedor.giro_id = request.POST.get('giro')
                proveedor.fecha_creacion = proveedor_old.fecha_creacion  # Conservamos la fecha original

                if request.FILES.get('logo'):
                    proveedor.logo = request.FILES.get('logo')  # Actualizamos el logo si es necesario

                proveedor.user = request.user
                proveedor.save()

                messages.success(request, 'Proveedor modificado exitosamente.')
                return redirect('listarProveedor')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                comunas = Comuna.objects.all()
                provincias = Provincia.objects.all()
                regiones = Region.objects.all()
                giros = Giro.objects.all()
                proveedor = Proveedor.objects.get(id=idProveedor)
                datos = {
                    'proveedores': Proveedor.objects.all(),
                    'proveedor': proveedor,
                    'comunas': comunas,
                    'provincias': provincias,
                    'regiones': regiones,
                    'giros': giros,
                    'error': 'Faltan campos obligatorios'
                }
                return render(request, 'crud_proveedores/modificar_proveedor.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos del proveedor
            comunas = Comuna.objects.all()
            provincias = Provincia.objects.all()
            regiones = Region.objects.all()
            giros = Giro.objects.all()
            proveedor = Proveedor.objects.get(id=idProveedor)
            datos = {
                'proveedores': Proveedor.objects.all(),
                'proveedor': proveedor,
                'comunas': comunas,
                'provincias': provincias,
                'regiones': regiones,
                'giros': giros
            }
            return render(request, 'crud_proveedores/modificar_proveedor.html', datos)

    except Proveedor.DoesNotExist:
        # En caso de que no exista el proveedor, manejar el error y devolver la vista con proveedor nulo
        comunas = Comuna.objects.all()
        provincias = Provincia.objects.all()
        regiones = Region.objects.all()
        giros = Giro.objects.all()
        datos = {
            'proveedores': Proveedor.objects.all(),
            'proveedor': None,
            'comunas': comunas,
            'provincias': provincias,
            'regiones': regiones,
            'giros': giros,
            'error': 'El proveedor solicitado no existe.'
        }
        return render(request, 'crud_proveedores/modificar_proveedor.html', datos)

@login_required
def eliminarProveedor(request, idProveedor):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                proveedor = Proveedor.objects.get(id=id_a_borrar)
                
                # Eliminar productos relacionados
                productos_relacionados = Producto.objects.filter(proveedor=proveedor)
                productos_relacionados.delete()
                
                # Eliminar el proveedor
                proveedor.delete()
                
                return redirect('listarProveedor')

        proveedores = Proveedor.objects.all()
        proveedor = Proveedor.objects.get(id=idProveedor)
        datos = {'proveedores': proveedores, 'proveedor': proveedor}
        return render(request, "crud_proveedores/eliminar_proveedor.html", datos)

    except Proveedor.DoesNotExist:
        proveedores = Proveedor.objects.all()
        proveedor = None
        datos = {'proveedores': proveedores, 'proveedor': proveedor}
        return render(request, "crud_proveedores/eliminar_proveedor.html", datos)



@login_required
def listarGiro(request):
    # Filtrar giros por el usuario que ha iniciado sesión (si es necesario)
    giros = Giro.objects.all()  # Si no hay un campo de usuario, puedes listar todos los giros
    return render(request, 'crud_giros/listar_giro.html', {'giros': giros})


def buscar_proveedores(request):
    query = request.GET.get('query', '')
    proveedores = Proveedor.objects.filter(nombre__icontains=query) | Proveedor.objects.filter(rut__icontains=query)
    
    results = []
    for p in proveedores:
        results.append({
            'id': p.id,
            'rut': p.rut,
            'nombre': p.nombre,
            'direccion': p.direccion,
            'telefono': p.telefono,
            'email': p.email,
            'giro_id': p.giro.id,  # Solo incluir el ID del giro
            'giro_nombre': p.giro.nombre if p.giro else None  # Incluir el nombre del giro si existe
        })
    
    return JsonResponse(results, safe=False)


def get_giros(request):
    giros = Giro.objects.all().values('id','codigo', 'nombre')  # Obtén los giros desde la base de datos
    return JsonResponse(list(giros), safe=False)  # Devuelve los giros como JSON

############################################################################ Pedidos ############################################################################
@login_required
def get_product_price(request, product_id):
    try:
        producto = get_object_or_404(Producto, id=product_id, user=request.user)
        return JsonResponse({'success': True, 'precio': float(producto.precio_compra)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
@login_required
def listarPedido(request):
    # Prefetch los detalles para optimizar la consulta
    pedidos = Pedido.objects.filter(user=request.user).prefetch_related('detalles__producto')

    # Calcular el total del pedido sumando los subtotales de los detalles
    for pedido in pedidos:
        pedido.total_calculado = sum(detalle.subtotal for detalle in pedido.detalles.all())

    return render(request, 'crud_pedidos/listar_pedido.html', {'pedidos': pedidos})


@login_required
def agregarPedido(request, proveedor_id=None):
    try:
        # Obtener el proveedor seleccionado si se proporciona el `proveedor_id`
        proveedor_seleccionado = None
        if proveedor_id:
            proveedor_seleccionado = get_object_or_404(Proveedor, id=proveedor_id, user=request.user)

        if request.method == 'POST':
            print("Se recibió un POST en agregarPedido.")
            print(f"Datos recibidos: proveedor_id={request.POST.get('proveedor')}, estado={request.POST.get('estado')}")

            # Validar los campos requeridos para el Pedido
            if all([
                request.POST.get('proveedor'),
                request.POST.get('estado')
            ]):
                try:
                    with transaction.atomic():
                        # Crear el Pedido
                        pedido = Pedido.objects.create(
                            proveedor_id=request.POST.get('proveedor'),
                            estado=request.POST.get('estado'),
                            observaciones=request.POST.get('observaciones', ''),
                            created_by=request.user,
                            updated_by=request.user,
                            user=request.user,
                        )
                        print(f"Pedido guardado con ID: {pedido.id}")

                        # Manejar los detalles del pedido
                        productos = request.POST.getlist('productos[]')
                        cantidades = request.POST.getlist('cantidades[]')
                        precios = request.POST.getlist('precios[]')
                        direcciones_entrega = request.POST.getlist('direcciones_entrega[]')

                        for i in range(len(productos)):
                            producto_id = int(productos[i])
                            cantidad_pedida = int(cantidades[i])
                            precio_unitario = float(precios[i])
                            direccion_entrega_id = int(direcciones_entrega[i])

                            # Obtener el producto
                            producto = get_object_or_404(Producto, id=producto_id)

                            # Obtener la bodega (como dirección de entrega)
                            direccion_entrega = get_object_or_404(Bodega, id=direccion_entrega_id)

                            # Actualizar la cantidad del producto
                            producto.cantidad += cantidad_pedida
                            producto.save()
                            print(f"Producto '{producto.nombre}' actualizado: cantidad {producto.cantidad}")

                            # Actualizar la capacidad de la bodega
                            if direccion_entrega.capacidad >= cantidad_pedida:
                                direccion_entrega.capacidad -= cantidad_pedida
                                direccion_entrega.cantidad_art = (direccion_entrega.cantidad_art or 0) + cantidad_pedida
                                direccion_entrega.save()
                                print(f"Bodega '{direccion_entrega.nombre}' actualizada: capacidad restante {direccion_entrega.capacidad}")
                            else:
                                raise ValueError(f"La bodega '{direccion_entrega.nombre}' no tiene suficiente capacidad para este pedido.")

                            # Crear el detalle del pedido
                            detalle = Detalle_Pedido.objects.create(
                                pedido=pedido,
                                producto=producto,
                                cantidad=cantidad_pedida,
                                precio_unitario=precio_unitario,
                                direccion_entrega=direccion_entrega,
                                user=request.user,
                            )
                            print(f"Detalle creado: {detalle}")

                        # Calcular el total del pedido
                        pedido.calcular_total()
                        print(f"Total del pedido calculado: {pedido.total}")

                        messages.success(request, 'Pedido creado exitosamente.')
                        return redirect('listarPedido')

                except Exception as e:
                    print(f"Error: {str(e)}")
                    messages.error(request, f"Error al procesar el pedido: {str(e)}")
                    return render(request, 'crud_pedidos/agregar_pedido.html', {
                        'error': f"Error al procesar el pedido: {str(e)}",
                        'proveedores': Proveedor.objects.filter(user=request.user),
                        'productos': Producto.objects.filter(user=request.user),
                        'bodegas': Bodega.objects.filter(user=request.user),
                        'estado_choices': Pedido.ESTADO_CHOICES,
                        'proveedor_seleccionado': proveedor_seleccionado,
                    })

            else:
                print("Campos obligatorios faltantes.")
                messages.error(request, "Faltan campos obligatorios para crear el pedido.")
                return render(request, 'crud_pedidos/agregar_pedido.html', {
                    'error': 'Faltan campos obligatorios',
                    'proveedores': Proveedor.objects.filter(user=request.user),
                    'productos': Producto.objects.filter(user=request.user),
                    'bodegas': Bodega.objects.filter(user=request.user),
                    'estado_choices': Pedido.ESTADO_CHOICES,
                    'proveedor_seleccionado': proveedor_seleccionado,
                })

        else:
            # Si se proporciona `proveedor_id`, filtrar productos por el proveedor seleccionado
            productos = Producto.objects.filter(proveedor=proveedor_seleccionado, user=request.user) if proveedor_seleccionado else Producto.objects.filter(user=request.user)
            return render(request, 'crud_pedidos/agregar_pedido.html', {
                'proveedores': Proveedor.objects.filter(user=request.user),
                'productos': productos,
                'bodegas': Bodega.objects.filter(user=request.user),
                'estado_choices': Pedido.ESTADO_CHOICES,
                'proveedor_seleccionado': proveedor_seleccionado,
            })
    except Proveedor.DoesNotExist:
        messages.error(request, 'El proveedor seleccionado no existe.')
        return redirect('listarProveedor')




from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Proveedor
from .serializers import ProveedorSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def create(self, request, *args, **kwargs):
        # Si el cuerpo de la solicitud es una lista
        if isinstance(request.data, list):
            # Procesa la lista
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Procesa un solo objeto
            serializer = self.get_serializer(data=request.data)

        # Valida los datos
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
