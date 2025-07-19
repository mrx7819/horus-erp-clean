import os
import django
import json
from pathlib import Path

# Configura el entorno antes de cualquier otra importación de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_pyme.settings'
django.setup()

# Ahora podemos importar los modelos de Django
from Proveedor.models import CategoriaGiro, Giro

def load_giros():
    try:
        # Construye la ruta al archivo JSON
        json_path = Path(__file__).resolve().parent / 'Json' / 'codigos.json'
        
        if not json_path.exists():
            print(f"Error: No se encuentra el archivo en la ruta: {json_path}")
            return

        # Obtener todas las categorías existentes
        categorias = {categoria.nombre: categoria for categoria in CategoriaGiro.objects.all()}
        
        with open(json_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar el JSON: {e}")
                return
            
            created_count = 0
            updated_count = 0
            error_count = 0
            
            for giro_data in data:
                try:
                    categoria_nombre = giro_data['categoria']
                    
                    # Obtener o crear la categoría
                    if categoria_nombre not in categorias:
                        categoria = CategoriaGiro.objects.create(nombre=categoria_nombre)
                        categorias[categoria_nombre] = categoria
                        print(f"✅ Categoría '{categoria_nombre}' creada.")
                    else:
                        categoria = categorias[categoria_nombre]
                    
                    # Intentar obtener el giro existente o crear uno nuevo
                    try:
                        giro = Giro.objects.get(codigo=giro_data['codigo'])
                        # Actualizar los datos si el giro existe
                        giro.nombre = giro_data['nombre']
                        giro.categoria = categoria
                        giro.save()
                        updated_count += 1
                        print(f"ℹ️ Giro '{giro.nombre}' actualizado en la categoría '{categoria.nombre}'.")
                    except Giro.DoesNotExist:
                        # Crear nuevo giro
                        giro = Giro.objects.create(
                            codigo=giro_data['codigo'],
                            nombre=giro_data['nombre'],
                            categoria=categoria
                        )
                        created_count += 1
                        print(f"✅ Giro '{giro.nombre}' creado en la categoría '{categoria.nombre}'.")
                        
                except KeyError as e:
                    error_count += 1
                    print(f"❌ Error: Falta el campo {e} en los datos del giro")
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error al procesar el giro {giro_data.get('codigo', 'desconocido')}: {str(e)}")
            
            print("\n=== Resumen de la operación ===")
            print(f"Total de giros creados: {created_count}")
            print(f"Total de giros actualizados: {updated_count}")
            print(f"Total de errores: {error_count}")
            print(f"Total procesado: {created_count + updated_count + error_count}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == '__main__':
    try:
        load_giros()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
