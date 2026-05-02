import os
import mediapipe

# Obtém o caminho onde a biblioteca foi instalada na venv
mp_path = os.path.dirname(mediapipe.__file__)
print(f"--- Diagnóstico de Ambiente ---")
print(f"Caminho do MediaPipe: {mp_path}")

# Verifica a existência física da pasta 'solutions'
solutions_path = os.path.join(mp_path, "solutions")
if os.path.exists(solutions_path):
    print("✅ A pasta 'solutions' EXISTE fisicamente.")
    print("Conteúdo detectado:", os.listdir(solutions_path))
else:
    print("❌ ERRO: A pasta 'solutions' NÃO EXISTE no diretório.")
    print("Isso indica uma instalação incompleta ou corrompida.")

# Verifica se o Python consegue importar o submódulo
try:
    from mediapipe.solutions import face_mesh
    print("✅ Importação de 'face_mesh' bem-sucedida!")
except ImportError as e:
    print(f"❌ Falha na importação: {e}")