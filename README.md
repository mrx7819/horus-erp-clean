# 🚀 Horus ERP
**Sistema ERP integral para PyMEs desarrollado con Django**

[![Demo](https://img.shields.io/badge/Demo-Live-success)](https://horus-erp.onrender.com/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Azure-blue)](https://azure.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> Sistema de gestión empresarial completo con arquitectura multi-tenant, diseñado específicamente para pequeñas y medianas empresas.

## 🎯 **Demo en Vivo**
**[👉 Ver Horus ERP funcionando](https://horus-erp.onrender.com/)**

*Usuario demo disponible en la aplicación*

---

## 🏗️ **Arquitectura del Sistema**

### **Multi-Tenant & Modular**
- **Workspaces aislados** por empresa
- **7 módulos funcionales** independientes
- **APIs REST** completas con Django REST Framework
- **Autenticación JWT** con refresh tokens

### **Módulos Principales**
```
├── 👤 Gestión de Usuarios    → Autenticación, roles, empresas
├── 👥 Clientes             → CRM básico, historial, contactos
├── 💰 Ventas               → Facturación, cotizaciones, reportes
├── 📦 Inventario           → Stock, categorías, bodegas
├── 🏢 Proveedores          → Gestión, ubicación, giros
├── 📍 Ubicaciones          → Sistema jerárquico Chile completo
└── 📊 Dashboard            → Métricas, reportes, análisis
```

---

## 🛠️ **Stack Tecnológico**

### **Backend**
- **Django 4.x** - Framework principal
- **Django REST Framework** - APIs RESTful
- **PostgreSQL** - Base de datos (Azure)
- **JWT Authentication** - Tokens seguros
- **Custom User Model** - Usuarios empresariales

### **Frontend**
- **HTML5, CSS3, JavaScript** - Interfaz responsive
- **Bootstrap** - Framework UI
- **Chart.js** - Gráficos y reportes
- **AJAX** - Comunicación asíncrona

### **Infraestructura**
- **Render** - Hosting y deployment
- **Azure Database** - PostgreSQL gestionado
- **WhiteNoise** - Archivos estáticos
- **Git** - Control de versiones

---

## ✨ **Características Principales**

### **🔐 Autenticación Avanzada**
- Login/registro con validaciones
- Recuperación de contraseña por email
- JWT tokens con refresh automático
- Protección CSRF y validaciones seguras

### **👥 Gestión de Clientes**
- Registro completo con RUT chileno
- Historial de interacciones
- Búsqueda y filtros avanzados
- Integración con sistema de ventas

### **💰 Sistema de Ventas**
- Cotizaciones y facturación
- Múltiples métodos de pago
- Cálculo automático de totales y descuentos
- Historial completo de transacciones

### **📦 Control de Inventario**
- Gestión de stock en tiempo real
- Múltiples bodegas por empresa
- Categorización de productos
- Alertas de stock bajo

### **🏢 Gestión de Proveedores**
- Base de datos completa
- Geolocalización con API chilena
- Clasificación por giros económicos
- Integración con sistema de compras

### **📍 Sistema de Ubicaciones**
- **Geolocalización Chile completa**
- Jerarquía Región → Provincia → Comuna
- Integración con clientes y proveedores
- Reutilizable en todos los módulos

---

## 🚀 **Instalación y Configuración**

### **Prerrequisitos**
- Python 3.8+
- PostgreSQL 12+
- pip y virtualenv

### **Instalación Local**
```bash
# Clonar repositorio
git clone https://github.com/mrx7819/horus-erp.git
cd horus-erp

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

### **Variables de Entorno Requeridas**
```env
SECRET_KEY=tu-secret-key-django
DB_NAME=nombre_base_datos
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=host_db
DB_PORT=5432
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=password_app_gmail
```

---

## 📱 **Capturas del Sistema**

### Dashboard Principal
*Vista general con métricas en tiempo real*

### Gestión de Ventas  
*Interface intuitiva para facturación*

### Control de Inventario
*Gestión de stock y productos*

---

## 🎯 **Casos de Uso**

**Ideal para:**
- 🏪 Pequeños comercios y tiendas
- 🏭 Empresas manufactureras pequeñas  
- 📊 Distribuidoras y mayoristas
- 🛠️ Empresas de servicios
- 📈 Startups en crecimiento

---

## 🔮 **Roadmap de Desarrollo**

### **v2.0 - En Desarrollo**
- [ ] API móvil con React Native
- [ ] Dashboard avanzado con BI
- [ ] Integración con bancos chilenos
- [ ] Reportes automáticos PDF
- [ ] Sistema de notificaciones push

### **v2.1 - Futuro**
- [ ] Integración con SII (facturación electrónica)
- [ ] Módulo de RRHH básico
- [ ] App móvil nativa
- [ ] Machine Learning para predicciones

---

## 🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 **Licencia**

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 **Desarrollador**

**Vicente Fraile** - Ingeniero Informático
- 📧 Email: vi.fraile.valdes@gmail.com
- 💼 LinkedIn: [Vicente Fraile](linkedin.com/in/vicente-fraile)
- 🌐 Portfolio: [horus-erp.onrender.com](https://horus-erp.onrender.com/)

---

## 🏆 **Tecnologías Destacadas**

- **Arquitectura Multi-Tenant** - Cada empresa opera independientemente
- **API REST Completa** - Endpoints documentados para integración
- **Seguridad Empresarial** - JWT, CSRF protection, validaciones
- **Escalabilidad** - Diseño preparado para crecimiento
- **UX/UI Responsive** - Funciona en desktop, tablet y móvil

---

⭐ **¡Si te gustó el proyecto, dale una estrella!** ⭐
