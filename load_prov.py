import os
import django
import json
from pathlib import Path

# Configura el entorno antes de cualquier otra importación de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_pyme.settings'
django.setup()

# Ahora podemos importar los modelos de Django
from Ubicacion.models import Provincia, Region

def load_prov():
    try:
        # Construye la ruta al archivo JSON
        json_path = Path(__file__).resolve().parent / 'Json' / 'Provincias.json'
        
        if not json_path.exists():
            print(f"Error: No se encuentra el archivo en la ruta: {json_path}")
            return

        # Obtener todas las regiones y convertir sus códigos a strings
        regiones = {str(region.codigo_region): region for region in Region.objects.all()}
        
        with open(json_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                return
            
            created_count = 0
            updated_count = 0
            error_count = 0
            
            for provincia_data in data:
                try:
                    # Convertir códigos a strings
                    codigo_provincia = str(provincia_data['codigo_provincia'])
                    codigo_region = str(provincia_data['region'])
                    
                    # Obtener la región
                    region = regiones.get(codigo_region)
                    if not region:
                        raise Region.DoesNotExist(f"No existe la región con código {codigo_region}")
                    
                    # Intentar obtener la provincia existente o crear una nueva
                    try:
                        provincia = Provincia.objects.get(codigo_provincia=codigo_provincia)
                        # Actualizar los datos si la provincia existe
                        provincia.nombre = provincia_data['nombre']
                        provincia.region = region
                        provincia.save()
                        updated_count += 1
                        print(f"ℹ️ Provincia '{provincia.nombre}' actualizada en la región '{region.nombre}'.")
                    except Provincia.DoesNotExist:
                        # Crear nueva provincia
                        provincia = Provincia.objects.create(
                            codigo_provincia=codigo_provincia,
                            nombre=provincia_data['nombre'],
                            region=region
                        )
                        created_count += 1
                        print(f"✅ Provincia '{provincia.nombre}' creada en la región '{region.nombre}'.")
                        
                except Region.DoesNotExist as e:
                    error_count += 1
                    print(f"❌ Error: {str(e)}")
                except KeyError as e:
                    error_count += 1
                    print(f"❌ Error: Falta el campo {e} en los datos de la provincia")
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error al procesar la provincia {provincia_data.get('codigo_provincia', 'desconocida')}: {str(e)}")
            
            print("\n=== Resumen de la operación ===")
            print(f"Total de provincias creadas: {created_count}")
            print(f"Total de provincias actualizadas: {updated_count}")
            print(f"Total de errores: {error_count}")
            print(f"Total procesado: {created_count + updated_count + error_count}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == '__main__':
    try:
        load_prov()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")