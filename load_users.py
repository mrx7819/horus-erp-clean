import os
import django
import json
from pathlib import Path
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# Configura el entorno antes de cualquier otra importación de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_pyme.settings'

try:
    django.setup()
except Exception as e:
    print(f"❌ Error al configurar Django: {e}")
    exit(1)

def load_users():
    try:
        # Construye la ruta al archivo JSON
        json_path = Path(__file__).resolve().parent / 'Json' / 'Users.json'
        
        # Verifica si el directorio y archivo existen
        if not json_path.parent.exists():
            print(f"Error: El directorio {json_path.parent} no existe.")
            return
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
            
            # Contadores
            created_count = 0
            updated_count = 0
            
            # Itera y crea cada usuario
            for user_data in data:
                try:
                    user, created = User.objects.get_or_create(
                        username=user_data['username'],
                        defaults={
                            'email': user_data.get('email', ''),
                            'first_name': user_data.get('first_name', ''),
                            'last_name': user_data.get('last_name', ''),
                            'is_superuser': user_data.get('is_superuser', False),
                            'is_staff': user_data.get('is_staff', False),
                            'is_active': user_data.get('is_active', True),
                        }
                    )
                    
                    if created:
                        # Valida contraseña
                        if len(user_data['password']) < 8:
                            print(f"⚠️ La contraseña para el usuario '{user.username}' es demasiado corta.")
                            continue
                        # Establece la contraseña
                        user.set_password(user_data['password'])
                        user.save()
                        created_count += 1
                        print(f"✅ Usuario '{user.username}' creado exitosamente.")
                    else:
                        updated_count += 1
                        print(f"ℹ️ Usuario '{user.username}' ya existe.")
                        
                except KeyError as e:
                    print(f"❌ Error: Falta el campo {e} en los datos del usuario")
                except IntegrityError as e:
                    print(f"❌ Error de integridad al crear usuario: {e}")
                except Exception as e:
                    print(f"❌ Error al procesar el usuario: {e}")
            
            # Resumen final
            if created_count + updated_count == 0:
                print("⚠️ No se procesaron usuarios. Revisa el archivo JSON.")
                return
            print("\n=== Resumen de la operación ===")
            print(f"Total de usuarios creados: {created_count}")
            print(f"Total de usuarios existentes: {updated_count}")
            print(f"Total procesado: {created_count + updated_count}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == '__main__':
    try:
        load_users()
    except KeyboardInterrupt:
        print("\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
