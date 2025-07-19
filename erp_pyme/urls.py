from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Home import views as home_views
from django.contrib.auth import views as auth_views
from Cliente import views as cliente_views
from Inventario.views import *
from Home.views import *
from User.views import *
from Venta.views import *
from Proveedor import views as proveedor_views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('', home_views.index, name='index'),  # Vista no protegida
    path('vistasprotegidas/', home_views.vistasprotegidas, name='vistasprotegidas'),  # Vista protegida
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forgot-password/',forgot_password, name='forgot_password'),
    path('registro/',registro, name='registro'),
    path('term_cond/', term_cond, name='term_cond'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
    #Clientes
    path('listarCliente/', cliente_views.listarCliente, name='listarCliente'),
    path('agregarCliente/', cliente_views.agregarCliente, name='agregarCliente'),
    path('modificarCliente/<int:idCliente>/', cliente_views.modificarCliente, name='modificarCliente'),
    path('eliminarCliente/<int:idCliente>/', cliente_views.eliminarCliente, name='eliminarCliente'),
    #Ventas
    path('listarVenta/', listarVenta, name='listarVenta'),
    path('agregarVenta/', agregarVenta, name='agregarVenta'),
    path('modificarVenta/<int:idVenta>/', modificarVenta, name='modificarVenta'),
    path('eliminarVenta/<int:idVenta>/', eliminarVenta, name='eliminarVenta'),
    path('eliminar-detalle/', eliminar_detalle, name='eliminar_detalle'),
    path('get-producto-precio/<int:producto_id>/', get_producto_precio, name='get_producto_precio'),
    path('api/ventas-por-producto/', VentasPorProductoAPI.as_view(), name='ventas-por-producto-api'),
    path('api/ganancias-totales/', GananciasTotalesAPI.as_view(), name='ganancias_totales'),
    path('api/productos-vendidos/', ProductosVendidosAPI.as_view(), name='productos_vendidos'),
    path('api/producto-estrella/', ProductoEstrellaAPI.as_view(), name='producto_estrella'),
    path('api/ingresos-diarios/', api_ingresos_diarios, name='api_ingresos_diarios'),
    path('api/categoria-mas-vendida/', CategoriaMasVendidaAPI.as_view(), name='categoria_mas_vendida'),
    path('api/cliente-mas-compras/', ClienteMasComprasAPI.as_view(), name='cliente_mas_compras'),
    path('api/egresos/', EgresosAPI.as_view(), name='egresos'),
    path('bodega/<int:bodega_id>/productos/', detalle_bodega, name='detalle_bodega'),
    #Proveedores
    path('agregarProveedor/', proveedor_views.agregarProveedor, name='agregarProveedor'),
    path('listarProveedor/', proveedor_views.listarProveedor, name='listarProveedor'),
    path('modificarProveedor/<int:idProveedor>/', proveedor_views.modificarProveedor, name='modificarProveedor'),
    path('eliminarProveedor/<int:idProveedor>/', proveedor_views.eliminarProveedor, name='eliminarProveedor'),
    #Pedidos
    path('listarPedido/', proveedor_views.listarPedido, name = 'listarPedido'),
    path('agregarPedido/<int:proveedor_id>/', proveedor_views.agregarPedido, name = 'agregarPedido'),
    #path('modificarPedido/', proveedor_views.listarPedido, name = 'listarPedido'),
    #path('eliminarPedido/', proveedor_views.listarPedido, name = 'listarPedido'),
     path('get-product-price/<int:product_id>/', proveedor_views.get_product_price, name='get_product_price'),
    
    #Categorías
    path('listarCategoria/', listarCategoria, name='listarCategoria'),
    path('agregarCategoria/', agregarCategoria, name='agregarCategoria'),
    path('modificarCategoria/<int:idCategoria>/', modificarCategoria, name='modificarCategoria'),
    path('eliminarCategoria/<int:idCategoria>/', eliminarCategoria, name='eliminarCategoria'),
    #Productos
    path('listarProducto/', listarProducto, name='listarProducto'),
    path('agregarProducto/', agregarProducto, name='agregarProducto'),
    path('modificarProducto/<int:idProducto>/', modificarProducto, name='modificarProducto'),
    path('eliminarProducto/<int:idProducto>/', eliminarProducto, name='eliminarProducto'),
    #Bodegas
    path('listarBodega/', listarBodega, name='listarBodega'),
    path('agregarBodega/', agregarBodega, name='agregarBodega'),
    path('modificarBodega/<int:idBodega>/', modificarBodega, name='modificarBodega'),
    path('eliminarBodega/<int:idBodega>/', eliminarBodega, name='eliminarBodega'),
    # Otras URLs...
    path('filtrar_comunas/', proveedor_views.filtrar_comunas, name='filtrar_comunas'),
    path('get_regiones/', proveedor_views.get_regiones, name='get_regiones'),
    path('get_provincias_por_region/<str:region_id>/', proveedor_views.get_provincias_por_region, name='get_provincias_por_region'),
    path('get_comunas_por_provincia/<str:provincia_id>/', proveedor_views.get_comunas_por_provincia, name='get_comunas_por_provincia'),
    path('get_giros/', proveedor_views.get_giros, name='get_giros'),  # Añade la URL para obtener giros
    path('upload_logo/', proveedor_views.upload_logo, name='upload_logo'),
    path('buscarProveedores/', proveedor_views.buscar_proveedores, name='buscar_proveedores'),
    path('api/', include('Cliente.urls')),
    path('api/', include('Proveedor.urls')),
    path('api/', include('Inventario.urls')),
    path('reportes/', ver_reporte, name='ver_reporte'),
    path('manual/', ver_manual, name='ver_manual'),
    #####################################
    path('reporte_ventas/', reporte_ventas, name='reporte_ventas'),
    path('reporte_clientes_compras/', reporte_clientes_compras, name='reporte_clientes_compras'),
    path('reporte_productos_vendidos/', reporte_productos_vendidos, name='reporte_productos_vendidos'),
    path('reporte_ganancias_netas/', reporte_ganancias_netas, name='reporte_ganancias_netas'),
    path('reporte_ventas_diarias/', reporte_ventas_diarias, name='reporte_ventas_diarias'),



    
]
