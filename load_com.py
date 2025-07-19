import os
import django
import json
from pathlib import Path

# Configura el entorno antes de cualquier otra importación de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_pyme.settings'
django.setup()

# Ahora podemos importar los modelos de Django
from Ubicacion.models import Comuna, Provincia

def load_com():
    try:
        # Construye la ruta al archivo JSON
        json_path = Path(__file__).resolve().parent / 'Json' / 'Comunas.json'
        
        if not json_path.exists():
            print(f"Error: No se encuentra el archivo en la ruta: {json_path}")
            return

        # Obtener todas las provincias y convertir sus códigos a strings
        provincias = {str(provincia.codigo_provincia): provincia for provincia in Provincia.objects.all()}
        
        with open(json_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                return
            
            created_count = 0
            updated_count = 0
            error_count = 0
            
            for comuna_data in data:
                try:
                    # Convertir códigos a strings
                    codigo_comuna = str(comuna_data['codigo_comuna'])
                    codigo_provincia = str(comuna_data['provincia'])
                    
                    # Obtener la provincia
                    provincia = provincias.get(codigo_provincia)
                    if not provincia:
                        raise Provincia.DoesNotExist(f"No existe la provincia con código {codigo_provincia}")
                    
                    # Intentar obtener la comuna existente o crear una nueva
                    try:
                        comuna = Comuna.objects.get(codigo_comuna=codigo_comuna)
                        # Actualizar los datos si la comuna existe
                        comuna.nombre = comuna_data['nombre']
                        comuna.provincia = provincia
                        comuna.save()
                        updated_count += 1
                        print(f"ℹ️ Comuna '{comuna.nombre}' actualizada en la provincia '{provincia.nombre}'.")
                    except Comuna.DoesNotExist:
                        # Crear nueva comuna
                        comuna = Comuna.objects.create(
                            codigo_comuna=codigo_comuna,
                            nombre=comuna_data['nombre'],
                            provincia=provincia
                        )
                        created_count += 1
                        print(f"✅ Comuna '{comuna.nombre}' creada en la provincia '{provincia.nombre}'.")
                        
                except Provincia.DoesNotExist as e:
                    error_count += 1
                    print(f"❌ Error: {str(e)}")
                except KeyError as e:
                    error_count += 1
                    print(f"❌ Error: Falta el campo {e} en los datos de la comuna")
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error al procesar la comuna {comuna_data.get('codigo_comuna', 'desconocida')}: {str(e)}")
            
            print("\n=== Resumen de la operación ===")
            print(f"Total de comunas creadas: {created_count}")
            print(f"Total de comunas actualizadas: {updated_count}")
            print(f"Total de errores: {error_count}")
            print(f"Total procesado: {created_count + updated_count + error_count}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == '__main__':
    try:
        load_com()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")