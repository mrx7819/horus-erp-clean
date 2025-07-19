import os
import django
import json
from pathlib import Path

# Configura el entorno antes de cualquier otra importación de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_pyme.settings'
django.setup()

# Ahora podemos importar los modelos de Django
from Ubicacion.models import Region 

def load_reg():
    try:
        # Construye la ruta al archivo JSON
        json_path = Path(__file__).resolve().parent / 'Json' / 'Regiones.json'
        
        # Verifica si el archivo existe
        if not json_path.exists():
            print(f"Error: No se encuentra el archivo en la ruta: {json_path}")
            return

        # Abre y lee el archivo JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                return
            
            # Contador para seguimiento
            created_count = 0
            updated_count = 0
            
            # Itera y crea cada región
            for region_data in data:
                try:
                    region, created = Region.objects.get_or_create(
                        codigo_region=region_data['codigo_region'],
                        defaults={'nombre': region_data['nombre']}
                    )
                    
                    if created:
                        created_count += 1
                        print(f"✅ Región '{region.nombre}' creada exitosamente.")
                    else:
                        updated_count += 1
                        print(f"ℹ️ Región '{region.nombre}' ya existe.")
                        
                except KeyError as e:
                    print(f"❌ Error: Falta el campo {e} en los datos de la región")
                except Exception as e:
                    print(f"❌ Error al procesar la región: {e}")
            
            # Resumen final
            print("\n=== Resumen de la operación ===")
            print(f"Total de regiones creadas: {created_count}")
            print(f"Total de regiones existentes: {updated_count}")
            print(f"Total procesado: {created_count + updated_count}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == '__main__':
    try:
        load_reg()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")