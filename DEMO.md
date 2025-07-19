# 🎯 Demo Guide - Horus ERP
**Guía completa para explorar el sistema**

> **Demo en vivo:** [horus-erp.onrender.com](https://horus-erp.onrender.com/)

## 🛠️ **Notas Técnicas para Desarrolladores**

### **Arquitectura y Estructura**
```python
# Estructura modular del proyecto
Apps Django: User, Cliente, Proveedor, Inventario, Venta, Ubicacion, Home
Cada módulo: modelos + vistas + urls + templates
```

### **Seguridad y Autenticación**
```python
# Multi-tenancy en cada consulta
clientes = Cliente.objects.filter(usuario=request.user)

# Autenticación JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Custom User Model
AUTH_USER_MODEL = 'User.CustomUser'
```

### **Validaciones y Datos**
- ✅ **Validación de RUT chileno** en modelos
- ✅ **Validación de email y teléfono** 
- ✅ **Validación de edad** (fecha nacimiento)
- ✅ **Unicidad de clientes** por usuario
- ✅ **Ubicaciones jerárquicas** (Región → Provincia → Comuna)

### **Base de Datos**
```python
# PostgreSQL con configuración dinámica
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
    }
}
```

### **APIs REST Disponibles**
```
/api/clientes/          → CRUD clientes
/api/ventas/            → CRUD ventas  
/api/productos/         → CRUD productos
/api/proveedores/       → CRUD proveedores
/api/auth/login/        → JWT authentication
/api/auth/refresh/      → Token refresh
```

### **Funcionalidades Avanzadas**
- ✅ **Signals** para lógica reactiva
- ✅ **Recovery password** por email con tokens seguros
- ✅ **Upload de archivos** (logos proveedores)
- ✅ **WhiteNoise** para archivos estáticos en producción
- ✅ **Variables de entorno** para datos sensibles

---

## 🚀 **Acceso Rápido al Demo**

### **Usuario Demo Disponible**
```
Usuario: demo@erp.com
Contraseña: Demo1234
```

### **O Crear Tu Propio Usuario**
1. Click en **"Registrarse"**
2. Completa los datos:
   - **Nombre:** Tu nombre
   - **Email:** tu_email@ejemplo.com  
   - **Empresa:** Nombre de tu empresa demo
   - **RUT Empresa:** 12345678-9 (formato chileno)
   - **Contraseña:** Mínimo 8 caracteres
3. **¡Listo!** Ya tienes tu workspace aislado

---

## 📋 **Tour Completo del Sistema**

### **🏠 1. Dashboard Principal**
**Lo que verás:**
- Resumen de ventas del mes
- Productos con stock bajo
- Clientes recientes
- Métricas principales

**Funcionalidades destacadas:**
- Gráficos en tiempo real
- Enlaces rápidos a módulos
- Notificaciones del sistema

---

### **👥 2. Gestión de Clientes**

#### **Agregar Cliente Demo**
1. **Menú:** Clientes → Añadir Cliente
2. **Datos sugeridos:**
   ```
   RUT: 12345678-9
   Nombre: Juan
   Apellido: Pérez
   Teléfono: 912345678
   Email: cliente1@erp.com
   Fecha de nacimiento: 1990-01-01
   Género: Masculino
   Dirección: Av. Providencia 123
   Región: Metropolitana
   Comuna: Santiago Centro
   ```
3. **Tip:** Para ventas rápidas, crea un "Cliente Genérico"
4. **Guardar** → El cliente aparece en la lista

#### **Explorar Funcionalidades:**
- ✅ **Búsqueda:** Prueba buscar por nombre o RUT
- ✅ **Filtros:** Por región, género, fecha
- ✅ **Edición:** Click en cualquier cliente para modificar
- ✅ **Historial:** Ver todas las ventas del cliente

---

### **📦 4. Gestión de Pedidos**

#### **Realizar Pedido Demo**
1. **Menú:** Pedidos → Realizar Pedido
2. **Seleccionar:**
   - Proveedor: Proveedor Demo
   - Productos a reabastecer
3. **Configurar cantidades:**
   ```
   Producto: Coca Cola 1L
   Cantidad: 50 unidades
   Precio unitario: $1.000
   ```
4. **Confirmar pedido** → Se actualiza automáticamente

#### **Funcionalidades Destacadas:**
- ✅ **Gestión de reabastecimiento** automático
- ✅ **Cálculo de costos** por pedido
- ✅ **Historial completo** de pedidos
- ✅ **Estados de pedido** (pendiente, recibido, cancelado)

---

### **💰 5. Sistema de Ventas**

#### **Registrar Venta Demo**
1. **Menú:** Ventas → Registrar Venta
2. **Seleccionar:**
   - Cliente: Juan Pérez (o Cliente Genérico)
   - Método pago: Efectivo
3. **Agregar productos al carrito:**
   ```
   Producto: Coca Cola 1L
   Cantidad: 3
   Precio: $1.500
   Descuento: 5%
   
   Producto: Otro producto
   Cantidad: 1
   Precio: $5.000
   Descuento: 0%
   ```
4. **Observar:**
   - Cálculo automático de subtotales
   - Aplicación de descuentos
   - Total final actualizado en tiempo real
   - Comprobante generado automáticamente

#### **Funcionalidades Avanzadas:**
- ✅ **Múltiples productos** por venta
- ✅ **Descuentos individuales** por producto
- ✅ **Cálculos automáticos** de totales
- ✅ **Historial completo** de transacciones
- ✅ **Filtros por fecha** y método de pago

---

### **📦 6. Gestión de Inventario**

#### **Categorías de Productos**
1. **Menú:** Inventario → Categorías
2. **Crear categorías demo:**
   ```
   Nombre: Bebidas
   Descripción: Productos líquidos para consumo
   
   Nombre: Tecnología
   Descripción: Equipos y accesorios tecnológicos
   
   Nombre: Oficina
   Descripción: Suministros de oficina
   ```

#### **Bodegas/Almacenes**
1. **Menú:** Inventario → Bodegas
2. **Crear bodega demo:**
   ```
   Nombre: Bodega Central
   Dirección: Av. Principal 456
   Región: Metropolitana
   Comuna: Santiago Centro
   Capacidad: 1000 productos
   ```

#### **Productos**
1. **Menú:** Inventario → Productos
2. **Agregar producto demo:**
   ```
   Nombre: Coca Cola 1L
   Categoría: Bebidas
   Proveedor: Proveedor Demo
   Bodega: Bodega Central
   Stock inicial: 100
   Precio Compra: $1.000
   Precio Venta: $1.500
   Stock Mínimo: 20
   ```

**Funcionalidades clave:**
- ✅ **Control de stock** en tiempo real
- ✅ **Alertas de stock bajo**
- ✅ **Múltiples bodegas** por empresa
- ✅ **Categorización** de productos
- ✅ **Márgenes de ganancia** automáticos

---

### **🏢 7. Gestión de Proveedores**

#### **Agregar Proveedor Demo**
1. **Menú:** Proveedores → Añadir Proveedor
2. **Datos sugeridos:**
   ```
   RUT: 98765432-1
   Nombre: Proveedor Demo
   Dirección: Calle Falsa 123
   Región: Metropolitana
   Provincia: Santiago
   Comuna: Santiago Centro
   Teléfono: 922334455
   Email: proveedor@erp.com
   Giro: Alimentos
   ```

#### **Características Destacadas:**
- ✅ **Clasificación por giros** económicos chilenos
- ✅ **Geolocalización** completa (región/provincia/comuna)
- ✅ **Upload de logos** empresariales
- ✅ **Integración** con sistema de compras

---

### **📍 8. Sistema de Ubicaciones**

**Funcionalidad Automática:**
- ✅ **Base de datos completa** de Chile
- ✅ **Jerarquía:** Región → Provincia → Comuna
- ✅ **Dropdowns dinámicos** (selecciona región → aparecen provincias)
- ✅ **Validaciones** de ubicaciones reales
- ✅ **Reutilizable** en clientes, proveedores, bodegas

**Pruébalo:**
1. En cualquier formulario, selecciona **Región Metropolitana**
2. Observa cómo aparecen las provincias automáticamente
3. Selecciona **Santiago** → Aparecen todas las comunas

---

## 🔒 **Funcionalidades de Seguridad**

### **Workspace Aislado**
- Cada usuario ve **solo sus datos**
- Sistema **multi-tenant** real
- No hay cross-contamination entre empresas

### **Autenticación Robusta**
1. **Prueba Recovery Password:**
   - Login → "¿Olvidaste tu contraseña?"
   - Ingresa tu email → Revisa bandeja
   - Sigue el link para resetear

2. **Session Management:**
   - Logout automático por inactividad
   - Tokens JWT seguros
   - Validaciones en cada request

---

## 📊 **Reportes y Análisis**

### **Dashboard de Métricas**
- **Ventas del mes:** Gráfico con tendencias
- **Top productos:** Los más vendidos
- **Stock crítico:** Productos bajo mínimo
- **Clientes activos:** Ultimas compras

### **Filtros Avanzados**
- **Por fechas:** Últimos 7 días, mes, año
- **Por categorías:** Tecnología, oficina, etc.
- **Por clientes:** Historial específico
- **Por métodos de pago:** Efectivo, transferencia, etc.

---

## 💡 **Flujo de Trabajo Completo Demo**

### **Escenario: Nueva Empresa Retail**

**1. Setup Inicial (5 min)**
```
→ Registrarse como nueva empresa
→ Crear 2-3 categorías de productos
→ Configurar bodega principal
→ Agregar 3-4 proveedores
```

**2. Cargar Inventario (5 min)**
```
→ Agregar 5-6 productos con stock
→ Configurar precios compra/venta
→ Establecer stock mínimo
```

**3. Gestión de Clientes (3 min)**
```
→ Registrar 2-3 clientes
→ Con datos completos de ubicación
→ Información de contacto
```

**4. Proceso de Ventas (5 min)**
```
→ Crear venta multi-producto
→ Aplicar descuentos
→ Verificar cálculos automáticos
→ Revisar historial de cliente
```

**5. Análisis y Reportes (2 min)**
```
→ Dashboard con métricas actualizadas
→ Productos con stock bajo
→ Rendimiento de ventas
```

---

## 🛠️ **Aspectos Técnicos Destacados**

### **Para Desarrolladores**
```python
# Multi-tenancy en cada consulta
clientes = Cliente.objects.filter(usuario=request.user)

# Transacciones atómicas en ventas
@transaction.atomic
def crear_venta(request):
    # Crear venta + detalles + actualizar stock
    pass

# APIs REST disponibles
/api/clientes/
/api/ventas/
/api/productos/
```

### **Base de Datos Real**
- **PostgreSQL en Azure** (no SQLite local)
- **Data real de ubicaciones** chilenas
- **Relaciones complejas** entre modelos
- **Validaciones de integridad** completas

---

## 🎯 **Qué Evaluar Como Reclutador**

### **Funcionalidades Empresariales**
- ✅ ¿Los cálculos son correctos?
- ✅ ¿La navegación es intuitiva?
- ✅ ¿Los filtros funcionan bien?
- ✅ ¿Las validaciones previenen errores?

### **Aspectos Técnicos**
- ✅ ¿La app es responsive?
- ✅ ¿Los formularios manejan errores?
- ✅ ¿El sistema es rápido?
- ✅ ¿La seguridad es adecuada?

### **Calidad de Código**
- ✅ ¿La estructura es mantenible?
- ✅ ¿Las URLs son semánticas?
- ✅ ¿Los modelos están bien diseñados?
- ✅ ¿El deploy funciona en producción?

---

## 📞 **¿Preguntas o Issues?**

**Desarrollador:** Vicente Fraile  
**Email:** vi.fraile.valdes@gmail.com  
**Repositorio:** [github.com/mrx7819/horus-erp-clean](https://github.com/mrx7819/horus-erp-clean)

---

**⭐ ¡Gracias por explorar Horus ERP! ⭐**

*Este sistema demuestra capacidades de desarrollo full-stack con enfoque empresarial real.*
