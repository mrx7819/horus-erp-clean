from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.

@login_required
def listarCliente(request):
    # Obtiene todos los clientes relacionados al usuario actual
    clientes = Cliente.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Obtiene el término de búsqueda desde el formulario
        palabra = request.POST.get('keyword')
        
        if palabra:  # Si hay una palabra de búsqueda
            # Filtrar clientes basándose en coincidencias parciales en múltiples campos
            resultado_busqueda = clientes.filter(
                Q(rut__icontains=palabra) |
                Q(nombre__icontains=palabra) |
                Q(apellido__icontains=palabra) |
                Q(direccion__icontains=palabra) |
                Q(telefono__icontains=palabra) |
                Q(email__icontains=palabra)
            )
            # Enviar resultados filtrados a la plantilla
            return render(request, 'crud_clientes/listar_cliente.html', {'clientes': resultado_busqueda})
    
    # Si no hay POST o palabra, envía la lista completa de clientes
    return render(request, 'crud_clientes/listar_cliente.html', {'clientes': clientes})

# views.py

import datetime

@login_required
def agregarCliente(request):
    if request.method == 'POST':
        if (
            request.POST.get('rut') and
            request.POST.get('nombre') and
            request.POST.get('apellido') and
            request.POST.get('telefono') and
            request.POST.get('email') and
            request.POST.get('fecha_nacimiento') and
            request.POST.get('genero') and
            request.POST.get('interaccion_fecha') and
            request.POST.get('interaccion_descripcion') and
            request.POST.get('interaccion_tipo')
        ):
            try:
                # Crear el cliente
                cliente = Cliente()
                cliente.rut = request.POST.get('rut')
                cliente.nombre = request.POST.get('nombre')
                cliente.apellido = request.POST.get('apellido')
                cliente.direccion = request.POST.get('direccion')  # Puede ser opcional
                cliente.telefono = request.POST.get('telefono')
                cliente.email = request.POST.get('email')
                cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                cliente.genero = request.POST.get('genero')
                cliente.user = request.user  # Relacionamos el cliente con el usuario logueado
                
                # Validar y guardar cliente
                cliente.full_clean()
                cliente.save()

                # Crear la interacción asociada
                interaccion = InteraccionCliente()
                interaccion.cliente = cliente
                interaccion.fecha = request.POST.get('interaccion_fecha')
                interaccion.descripcion = request.POST.get('interaccion_descripcion')
                interaccion.tipo_interaccion = request.POST.get('interaccion_tipo')

                # Validar y guardar interacción
                interaccion.full_clean()
                interaccion.save()

                messages.success(request, 'Cliente e interacción agregados exitosamente.')
                return redirect('listarCliente')  # Cambiar por el nombre de la URL que lista los clientes
            except ValidationError as e:
                messages.error(request, f'Error de validación: {e.message_dict}')
            except Exception as e:
                messages.error(request, f'Error al crear el cliente o la interacción: {str(e)}')
            return render(request, 'crud_clientes/agregar_cliente.html')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
            return render(request, 'crud_clientes/agregar_cliente.html')
    else:
        # Renderizamos el formulario
        return render(request, 'crud_clientes/agregar_cliente.html')



@login_required
def modificarCliente(request, idCliente):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('id') and
                request.POST.get('rut') and
                request.POST.get('nombre') and
                request.POST.get('apellido') and
                request.POST.get('telefono') and
                request.POST.get('email') and
                request.POST.get('fecha_nacimiento') and
                request.POST.get('genero')
            ):
                # Recuperamos el cliente original antes de actualizarlo
                cliente_id_old = request.POST.get('id')
                cliente_old = Cliente.objects.get(id=cliente_id_old)

                # Creamos una nueva instancia del cliente con los datos actualizados
                cliente = Cliente()
                cliente.id = request.POST.get('id')
                cliente.rut = request.POST.get('rut')
                cliente.nombre = request.POST.get('nombre')
                cliente.apellido = request.POST.get('apellido')
                cliente.direccion = request.POST.get('direccion')  # Puede ser opcional
                cliente.telefono = request.POST.get('telefono')
                cliente.email = request.POST.get('email')
                cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
                cliente.genero = request.POST.get('genero')
                cliente.fecha_creacion = cliente_old.fecha_creacion  # Mantenemos la fecha original
                cliente.user = request.user
                cliente.save()

                # Modificar o crear una nueva interacción
                if (
                    request.POST.get('interaccion_id') and
                    request.POST.get('interaccion_fecha') and
                    request.POST.get('interaccion_tipo') and
                    request.POST.get('interaccion_descripcion')
                ):
                    interaccion_id = request.POST.get('interaccion_id')
                    interaccion_fecha = request.POST.get('interaccion_fecha')
                    interaccion_tipo = request.POST.get('interaccion_tipo')
                    interaccion_descripcion = request.POST.get('interaccion_descripcion')

                    if interaccion_id != "0":  # Modificar interacción existente
                        try:
                            interaccion = InteraccionCliente.objects.get(id=interaccion_id, cliente=cliente)
                            interaccion.fecha = interaccion_fecha
                            interaccion.tipo_interaccion = interaccion_tipo
                            interaccion.descripcion = interaccion_descripcion
                            interaccion.save()
                        except InteraccionCliente.DoesNotExist:
                            messages.error(request, 'La interacción que intenta modificar no existe.')
                    else:  # Crear nueva interacción
                        InteraccionCliente.objects.create(
                            cliente=cliente,
                            fecha=interaccion_fecha,
                            tipo_interaccion=interaccion_tipo,
                            descripcion=interaccion_descripcion
                        )

                return redirect('listarCliente')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                clientes = Cliente.objects.all()
                cliente = Cliente.objects.get(id=idCliente)
                interacciones = InteraccionCliente.objects.filter(cliente=cliente)
                datos = {
                    'clientes': clientes,
                    'cliente': cliente,
                    'interacciones': interacciones,
                    'error': 'Faltan campos obligatorios',
                }
                return render(request, 'crud_clientes/modificar_cliente.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos del cliente
            clientes = Cliente.objects.all()
            cliente = Cliente.objects.get(id=idCliente)
            interacciones = InteraccionCliente.objects.filter(cliente=cliente)
            datos = {
                'clientes': clientes,
                'cliente': cliente,
                'interacciones': interacciones,
            }
            return render(request, 'crud_clientes/modificar_cliente.html', datos)

    except Cliente.DoesNotExist:
        # En caso de que no exista el cliente, manejar el error y devolver la vista con cliente nulo
        clientes = Cliente.objects.all()
        datos = {
            'clientes': clientes,
            'cliente': None,
            'interacciones': [],
            'error': 'El cliente solicitado no existe.',
        }
        return render(request, 'crud_clientes/modificar_cliente.html', datos)








@login_required
def eliminarCliente(request, idCliente=None):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                cliente = Cliente.objects.get(id=id_a_borrar)
                cliente.delete()
                messages.success(request, 'Cliente eliminado exitosamente.')
                return redirect('listarCliente')  # Cambia 'listarCliente' por la vista que lista los clientes
            else:
                # Si faltan campos, devolver el formulario con un error
                clientes = Cliente.objects.all()
                cliente = Cliente.objects.get(id=idCliente)
                datos = {'clientes': clientes, 'cliente': cliente, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_clientes/eliminar_cliente.html', datos)
        else:
            # En caso de GET, cargar el cliente a eliminar y todos los clientes disponibles
            clientes = Cliente.objects.all()
            cliente = Cliente.objects.get(id=idCliente) if idCliente else None
            datos = {'clientes': clientes, 'cliente': cliente}
            return render(request, 'crud_clientes/eliminar_cliente.html', datos)

    except Cliente.DoesNotExist:
        # Si no existe el cliente, manejar el error
        messages.error(request, 'El cliente solicitado no existe.')
        return redirect('listarCliente')  # Redirige a la lista de clientes
    

    ##############################################################################################################################

from rest_framework import viewsets, status
from .models import Cliente, InteraccionCliente
from .serializers import ClienteSerializer, InteraccionClienteSerializer
from rest_framework.response import Response

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        # Comprueba si es una lista de datos
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Valida los datos
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InteraccionClienteViewSet(viewsets.ModelViewSet):
    queryset = InteraccionCliente.objects.all()
    serializer_class = InteraccionClienteSerializer

class ClienteConInteraccionViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer