import json
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Inventario.models import Categoria, CategoriaGiro, Producto, Bodega
from Proveedor.models import Proveedor
from Ubicacion.models import *
from django.contrib import messages  # Añadir esta importación
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver    
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.

@login_required
def listarCategoria(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    categorias = Categoria.objects.filter(user=request.user)
    return render(request, 'crud_categorias/listar_categoria.html', {'categorias': categorias})


@login_required
def agregarCategoria(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('descripcion'):
            
            
            categoria = Categoria()
            categoria.nombre = request.POST.get('nombre')
            categoria.descripcion = request.POST.get('descripcion')
            categoria.user = request.user
            categoria.save()
            return redirect('listarCategoria')
        else:
            # Si no se completaron todos los campos, podrías mostrar un mensaje de error
            return render(request, 'crud_categorias/agregar_categoria.html')
    else:
        return render(request, 'crud_categorias/agregar_categoria.html')



@login_required
def modificarCategoria(request, idCategoria):
    try:
        if request.method == 'POST':
            if request.POST.get('id') and request.POST.get('nombre') and request.POST.get('descripcion'):

                categoria_id_old = request.POST.get('id')
                categoria_old = Categoria.objects.get(id=categoria_id_old)

                categoria = Categoria()
                categoria.id = request.POST.get('id')
                categoria.nombre = request.POST.get('nombre')
                categoria.descripcion = request.POST.get('descripcion')
                categoria.fecha_creacion = categoria_old.fecha_creacion
                categoria.user = request.user
                categoria.save()
                return redirect('listarCategoria')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                categorias = Categoria.objects.all()
                categoria = Categoria.objects.get(id=idCategoria)
                datos = {'categorias': categorias, 'categoria': categoria, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_categorias/modificar_categoria.html', datos)

        else:
            # Si es una solicitud GET, mostrar el formulario con los datos de la categoría
            categorias = Categoria.objects.all()
            categoria = Categoria.objects.get(id=idCategoria)
            datos = {'categorias': categorias, 'categoria': categoria}
            return render(request, 'crud_categorias/modificar_categoria.html', datos)

    except Categoria.DoesNotExist:
        # En caso de que no exista la categoría, manejar el error y devolver la vista con categoría nula
        categorias = Categoria.objects.all()
        categoria = None
        datos = {'categorias': categorias, 'categoria': categoria}
        return render(request, 'crud_categorias/modificar_categoria.html', datos)




@login_required
def eliminarCategoria(request,idCategoria):
    try:
        if request.method=='POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                tupla = Categoria.objects.get(id = id_a_borrar)
                tupla.delete()
                return redirect('listarCategoria')
            else:
                # Si faltan campos en el formulario, devolver el formulario con un error
                categorias = Categoria.objects.all()
                categoria = Categoria.objects.get(id=idCategoria)
                datos = {'categorias': categorias, 'categoria': categoria, 'error': 'Faltan campos obligatorios'}
                return render(request, 'crud_categorias/eliminar_categoria.html', datos)
        else:  
            categorias = Categoria.objects.all()
            datos = {'categorias': categorias}
            return render (request, "crud_categorias/eliminar_categoria.html", datos)
    except Categoria.DoesNotExist:
        categorias = Categoria.objects.all()
        datos = {'categorias': categorias}
        return render (request, "crud_categorias/eliminar_categoria.html", datos)


##PRODUCTOS##
@login_required
def listarProducto(request):
    # Filtrar clientes por el usuario que ha iniciado sesión
    productos = Producto.objects.filter(user=request.user)
    return render(request, 'crud_productos/listar_producto.html', {'productos': productos})

@login_required
def agregarProducto(request):
    if request.method == 'POST':
        print("Datos recibidos en POST:", request.POST)  # Debugging: Verifica datos enviados

        if (
            request.POST.get('sku') and 
            request.POST.get('nombre') and 
            request.POST.get('precio_compra') and
            request.POST.get('precio_venta') and
            request.POST.get('cantidad') and 
            request.POST.get('categoria') and
            request.POST.get('proveedor') and
            request.POST.get('bodega') and
            request.POST.get('iva')
        ):
            nueva_cantidad = int(request.POST.get('cantidad'))
            bodega_id = int(request.POST.get('bodega'))

            print(f"Bodega ID: {bodega_id}, Cantidad solicitada: {nueva_cantidad}")

            try:
                bodega = Bodega.objects.get(id=bodega_id)
                print(f"Bodega seleccionada: {bodega.nombre}, Capacidad actual: {bodega.capacidad}, Artículos actuales: {bodega.cantidad_art}")

                # Verificar que la capacidad es suficiente antes de modificar cualquier dato
                if bodega.capacidad >= nueva_cantidad:
                    # Calcula las nuevas cantidades
                    nueva_capacidad = bodega.capacidad - nueva_cantidad
                    bodega.cantidad_art = (bodega.cantidad_art or 0) + nueva_cantidad
                    bodega.capacidad = nueva_capacidad

                    print(f"Actualizando bodega: Nueva cantidad de artículos: {bodega.cantidad_art}, Nueva capacidad: {bodega.capacidad}")

                    # Guarda los cambios en la bodega
                    bodega.save()

                    # Crear el producto asociado
                    producto = Producto(
                        sku=request.POST.get('sku'),
                        nombre=request.POST.get('nombre'),
                        precio_compra=float(request.POST.get('precio_compra')),
                        precio_venta=float(request.POST.get('precio_venta')),
                        porc_ganancias=(float(request.POST.get('precio_venta')) - float(request.POST.get('precio_compra'))) / float(request.POST.get('precio_compra')) * 100,
                        cantidad=nueva_cantidad,
                        categoria_id=int(request.POST.get('categoria')),
                        proveedor_id=int(request.POST.get('proveedor')),
                        bodega_id=bodega_id,
                        iva=float(request.POST.get('iva')),
                        user=request.user
                    )

                    # Guarda la imagen del producto, si existe
                    if request.FILES.get('imagen'):
                        producto.img = request.FILES.get('imagen')

                    producto.save()

                    print(f"Producto guardado exitosamente: {producto.nombre}")
                    messages.success(request, 'Producto agregado exitosamente.')
                    return redirect('listarProducto')
                else:
                    print("Capacidad insuficiente para agregar los productos solicitados.")
                    messages.warning(
                        request, 
                        f'No hay suficiente capacidad en la bodega. Solo puedes agregar hasta {bodega.capacidad} artículos.'
                    )
            except Bodega.DoesNotExist:
                print(f"Bodega con ID {bodega_id} no encontrada.")
                messages.error(request, 'La bodega seleccionada no existe.')

    # Datos para cargar el formulario
    categorias = Categoria.objects.filter(user=request.user)
    proveedores = Proveedor.objects.filter(user=request.user)
    bodegas = Bodega.objects.filter(user=request.user)

    return render(request, 'crud_productos/agregar_producto.html', {
        'categorias': categorias,
        'proveedores': proveedores,
        'bodegas': bodegas,
        'capacidades': json.dumps({b.id: b.capacidad for b in bodegas}),  # Convertir capacidades a JSON
    })


@login_required
def modificarProducto(request, idProducto):
    try:
        if request.method == 'POST':
            # Validar que todos los campos obligatorios estén presentes
            if (
                request.POST.get('sku') and 
                request.POST.get('nombre') and 
                request.POST.get('categoria') and 
                request.POST.get('proveedor') and 
                request.POST.get('precio_compra') and 
                request.POST.get('precio_venta') and 
                request.POST.get('cantidad') and 
                request.POST.get('bodega') and 
                request.POST.get('iva')
            ):
                # Recuperar el producto original
                producto_id_old = request.POST.get('id')
                producto_old = Producto.objects.get(id=producto_id_old)

                # Calcular la diferencia de cantidad para ajustar el stock de la bodega
                nueva_cantidad = int(request.POST.get('cantidad'))
                bodega_id = int(request.POST.get('bodega'))
                diferencia = nueva_cantidad - producto_old.cantidad

                # Recuperar la bodega seleccionada
                bodega = Bodega.objects.get(id=bodega_id)

                # Ajustar stock en la bodega
                if diferencia > 0:  # Si la cantidad aumenta
                    if bodega.capacidad >= diferencia:
                        bodega.capacidad -= diferencia
                        bodega.cantidad_art = (bodega.cantidad_art or 0) + diferencia
                    else:
                        messages.warning(
                            request,
                            f'Capacidad insuficiente en la bodega. Puedes agregar hasta {bodega.capacidad} artículos adicionales.'
                        )
                        return redirect('modificarProducto', idProducto=idProducto)
                elif diferencia < 0:  # Si la cantidad disminuye
                    bodega.capacidad += abs(diferencia)
                    bodega.cantidad_art = max((bodega.cantidad_art or 0) + diferencia, 0)

                # Guardar los cambios en la bodega
                bodega.save()

                # Actualizar el producto
                producto = Producto()
                producto.id = request.POST.get('id')
                producto.sku = request.POST.get('sku')
                producto.nombre = request.POST.get('nombre')
                producto.categoria_id = request.POST.get('categoria')
                producto.proveedor_id = request.POST.get('proveedor')
                producto.precio_compra = float(request.POST.get('precio_compra'))
                producto.precio_venta = float(request.POST.get('precio_venta'))
                producto.porc_ganancias = (producto.precio_venta - producto.precio_compra) / producto.precio_compra * 100
                producto.cantidad = nueva_cantidad
                producto.bodega_id = bodega_id
                producto.iva = float(request.POST.get('iva'))
                producto.fecha_creacion = producto_old.fecha_creacion  # Mantener la fecha original
                producto.user = request.user

                # Actualizar imagen si se proporciona una nueva
                if request.FILES.get('imagen'):
                    producto.img = request.FILES.get('imagen')

                producto.save()
                messages.success(request, 'Producto modificado exitosamente.')
                return redirect('listarProducto')
            else:
                # Si faltan campos, cargar datos y mostrar un mensaje de error
                categorias = Categoria.objects.filter(user=request.user)
                proveedores = Proveedor.objects.filter(user=request.user)
                bodegas = Bodega.objects.filter(user=request.user)
                producto = Producto.objects.get(id=idProducto)
                datos = {
                    'productos': Producto.objects.all(),
                    'producto': producto,
                    'categorias': categorias,
                    'proveedores': proveedores,
                    'bodegas': bodegas,
                    'error': 'Faltan campos obligatorios.'
                }
                return render(request, 'crud_productos/modificar_producto.html', datos)
        else:
            # Si es GET, cargar los datos actuales del producto
            categorias = Categoria.objects.filter(user=request.user)
            proveedores = Proveedor.objects.filter(user=request.user)
            bodegas = Bodega.objects.filter(user=request.user)
            producto = Producto.objects.get(id=idProducto)
            datos = {
                'productos': Producto.objects.all(),
                'producto': producto,
                'categorias': categorias,
                'proveedores': proveedores,
                'bodegas': bodegas
            }
            return render(request, 'crud_productos/modificar_producto.html', datos)

    except Producto.DoesNotExist:
        # Si el producto no existe, manejar el error y devolver la vista con producto nulo
        categorias = Categoria.objects.filter(user=request.user)
        proveedores = Proveedor.objects.filter(user=request.user)
        bodegas = Bodega.objects.filter(user=request.user)
        datos = {
            'productos': Producto.objects.all(),
            'producto': None,
            'categorias': categorias,
            'proveedores': proveedores,
            'bodegas': bodegas,
            'error': 'El producto solicitado no existe.'
        }
        return render(request, 'crud_productos/modificar_producto.html', datos)





@login_required
def eliminarProducto(request, idProducto):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                producto = Producto.objects.get(id=id_a_borrar)

                # Actualizar la bodega asociada al producto
                bodega = producto.bodega
                cantidad = producto.cantidad
                bodega.capacidad += cantidad
                bodega.cantidad_art = max((bodega.cantidad_art or 0) - cantidad, 0)
                bodega.save()

                # Eliminar el producto
                producto.delete()

                messages.success(request, 'Producto eliminado exitosamente.')
                return redirect('listarProducto')

        # Recuperar datos para mostrar la confirmación de eliminación
        productos = Producto.objects.all()
        producto = Producto.objects.get(id=idProducto)
        datos = {'productos': productos, 'producto': producto}
        return render(request, "crud_productos/eliminar_producto.html", datos)

    except Producto.DoesNotExist:
        # Si el producto no existe, manejar el error y devolver datos vacíos
        productos = Producto.objects.all()
        producto = None
        datos = {'productos': productos, 'producto': producto, 'error': 'El producto solicitado no existe.'}
        return render(request, "crud_productos/eliminar_producto.html", datos)
##BODEGAS##

@login_required
def listarBodega(request):
    # Filtrar bodegas por el usuario que ha iniciado sesión
    bodegas = Bodega.objects.filter(user=request.user)
    return render(request, 'crud_bodegas/listar_bodega.html', {'bodegas': bodegas})


@login_required
def agregarBodega(request):
    if request.method == 'POST':
        if (
            request.POST.get('nombre') and
            request.POST.get('direccion') and
            request.POST.get('capacidad') and
            request.POST.get('comuna') and
            request.POST.get('provincia') and
            request.POST.get('region')
        ):
            try:
                bodega = Bodega()
                bodega.nombre = request.POST.get('nombre')
                bodega.direccion = request.POST.get('direccion')
                bodega.capacidad = int(request.POST.get('capacidad'))
                bodega.comuna_id = request.POST.get('comuna')
                bodega.provincia_id = request.POST.get('provincia')
                bodega.region_id = request.POST.get('region')
                bodega.user = request.user
                bodega.cantidad_art = 0  # Inicializamos en 0 ya que es una bodega nueva
                bodega.save()
                messages.success(request, 'Bodega creada exitosamente.')
                return redirect('listarBodega')
            except ValueError:
                messages.error(request, 'Por favor, ingrese valores válidos.')
            except Exception as e:
                messages.error(request, f'Error al crear la bodega: {str(e)}')
            return render(request, 'crud_bodegas/agregar_bodega.html')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos.')
            return render(request, 'crud_bodegas/agregar_bodega.html')
    else:
        # Pasamos las comunas, provincias y regiones disponibles al formulario
        comunas = Comuna.objects.all()
        provincias = Provincia.objects.all()
        regiones = Region.objects.all()
        return render(request, 'crud_bodegas/agregar_bodega.html', {
            'comunas': comunas,
            'regiones': regiones,
            'provincias': provincias,
        })

@login_required
def modificarBodega(request, idBodega):
    try:
        if request.method == 'POST':
            if (
                request.POST.get('nombre') and 
                request.POST.get('capacidad') and 
                request.POST.get('direccion') and 
                request.POST.get('comuna') and
                request.POST.get('provincia') and
                request.POST.get('region')
            ):
                # Obtener la bodega existente por su ID
                bodega_id_old = request.POST.get('id')
                bodega_old = Bodega.objects.get(id=bodega_id_old)

                # Crear un nuevo objeto Bodega con los datos modificados
                bodega = Bodega()
                bodega.id = request.POST.get('id')
                bodega.nombre = request.POST.get('nombre')
                bodega.capacidad = request.POST.get('capacidad')
                bodega.direccion = request.POST.get('direccion')
                bodega.comuna_id = request.POST.get('comuna')
                bodega.provincia_id = request.POST.get('provincia')
                bodega.region_id = request.POST.get('region')
                bodega.fecha_creacion = bodega_old.fecha_creacion  # Mantener la fecha original
                bodega.user = request.user  # Asignar el usuario actual

                bodega.save()

                messages.success(request, 'Bodega modificada exitosamente.')
                return redirect('listarBodega')
            else:
                # Si faltan campos obligatorios, mostrar error y datos actuales
                comunas = Comuna.objects.all()
                provincias = Provincia.objects.all()
                regiones = Region.objects.all()
                bodega = Bodega.objects.get(id=idBodega)
                datos = {
                    'bodegas': Bodega.objects.all(),
                    'bodega': bodega,
                    'comunas': comunas,
                    'provincias': provincias,
                    'regiones': regiones,
                    'error': 'Faltan campos obligatorios'
                }
                return render(request, 'crud_bodegas/modificar_bodega.html', datos)

        else:
            # Si es GET, cargar los datos actuales de la bodega
            comunas = Comuna.objects.all()
            provincias = Provincia.objects.all()
            regiones = Region.objects.all()
            bodega = Bodega.objects.get(id=idBodega)
            datos = {
                'bodegas': Bodega.objects.all(),
                'bodega': bodega,
                'comunas': comunas,
                'provincias': provincias,
                'regiones': regiones
            }
            return render(request, 'crud_bodegas/modificar_bodega.html', datos)

    except Bodega.DoesNotExist:
        # Si la bodega no existe, manejar el error y devolver datos nulos
        comunas = Comuna.objects.all()
        provincias = Provincia.objects.all()
        regiones = Region.objects.all()
        datos = {
            'bodegas': Bodega.objects.all(),
            'bodega': None,
            'comunas': comunas,
            'provincias': provincias,
            'regiones': regiones,
            'error': 'La bodega solicitada no existe.'
        }
        return render(request, 'crud_bodegas/modificar_bodega.html', datos)



@login_required
def eliminarBodega(request, idBodega):
    try:
        if request.method == 'POST':
            if request.POST.get('id'):
                id_a_borrar = request.POST.get('id')
                bodega = Bodega.objects.get(id=id_a_borrar)
                bodega.delete()
                return redirect('listarBodega')
            else:
                # Si faltan campos, mostrar un error
                bodegas = Bodega.objects.all()
                bodega = Bodega.objects.get(id=idBodega)
                return render(request, 'crud_bodegas/eliminar_bodega.html', {
                    'bodegas': bodegas,
                    'bodega': bodega,
                    'error': 'Faltan campos obligatorios',
                })
        else:
            # En caso de GET, cargar la bodega a eliminar
            bodegas = Bodega.objects.all()
            bodega = Bodega.objects.get(id=idBodega)
            return render(request, 'crud_bodegas/eliminar_bodega.html', {
                'bodegas': bodegas,
                'bodega': bodega,
            })
    except Bodega.DoesNotExist:
        # Si no existe la bodega, manejar el error
        bodegas = Bodega.objects.all()
        return render(request, 'crud_bodegas/eliminar_bodega.html', {
            'bodegas': bodegas,
        })


from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Categoria, Bodega
from .serializers import CategoriaSerializer, BodegaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def create(self, request, *args, **kwargs):
        # Si el cuerpo de la solicitud es una lista
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Valida los datos
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer

    def create(self, request, *args, **kwargs):
        # Si el cuerpo de la solicitud es una lista
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Valida los datos
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@login_required
def detalle_bodega(request, bodega_id):
    try:
        # Obtener la bodega seleccionada
        bodega = Bodega.objects.get(id=bodega_id, user=request.user)
    except Bodega.DoesNotExist:
        # Si la bodega no existe, redirigir con un mensaje de alerta
        messages.warning(request, "No has seleccionado una bodega válida. Por favor, selecciona una desde la lista.")
        return redirect('listarBodega')
    
    # Filtrar los productos que pertenecen a esta bodega
    productos = Producto.objects.filter(bodega=bodega, user=request.user)

    # Pasar los productos y la bodega al template
    return render(request, 'crud_bodegas/detalle_bodega.html', {
        'bodega': bodega,
        'productos': productos,
    })