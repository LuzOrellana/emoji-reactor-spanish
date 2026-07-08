import cv2
try:
    import mediapipe as mp
except Exception:
    print("Error: mediapipe no está instalado o no se pudo importar. Instale mediapipe con: pip install mediapipe")
    raise
import numpy as np
from PIL import Image
import os
import time
import math

# ==========================================
# 1. CONFIGURACIÓN DE MEDIAPIPE
# ==========================================
mp_malla_rostro = mp.solutions.face_mesh
mp_manos = mp.solutions.hands

malla_rostro = mp_malla_rostro.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

manos = mp_manos.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def cargar_imagen(path, tamano_base=(250, 250)):
    try:
        imagen_pil = Image.open(path).convert("RGB")
        imagen_pil = imagen_pil.resize(tamano_base, Image.Resampling.LANCZOS)
        return cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error al cargar {path}: {e}")
        return None

archivos_imagenes = {
    "TA_BIEN": ["Poli.jpeg","thumbsup_1.jpg", "thumbsup_2.jpg", "thumbsup_3.jpg", "thumbsup_4.jpg", "thumbsup_5.jpg"],
    "FELIZ": ["happy_1.jpg", "happy_2.jpg", "happy_3.jpg", "happy_4.jpg", "happy_5.jpg"],
    "ASUSTADO": ["scaryface_1.jpg", "scaryface_2.jpg", "scaryface_3.jpg", "scaryface_4.jpg", "scaryface_5.jpg"],
    "BURLA": ["you_1.jpg", "you_2.jpg", "you_3.jpg"],
}

imagenes_cargadas = {}

for categoria, archivos in archivos_imagenes.items():
    imagenes_cargadas[categoria] = []
    for archivo in archivos:
        ruta = os.path.join("assets", archivo)
        imagen = cargar_imagen(ruta)
        if imagen is not None:
            imagenes_cargadas[categoria].append(imagen)

# ==========================================
# 2. SISTEMA PRINCIPAL
# ==========================================
camara = cv2.VideoCapture(0)

ventana_camara = "Camara"
pos_x_camara, pos_y_camara = 50, 100

estado_reaccionando = False
inicio_reaccion = 0
duracion_reaccion = 2.0
ventanas_activas = []

while camara.isOpened():

    exito, frame = camara.read()
    if not exito:
        break

    frame = cv2.flip(frame, 1)
    alto_cam, ancho_cam, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultados_rostro = malla_rostro.process(frame_rgb)
    resultados_manos = manos.process(frame_rgb)

    estado_detectado = "NEUTRAL"

    # --- DETECCIÓN DE MANOS ---
    if resultados_manos.multi_hand_landmarks:
        for mano in resultados_manos.multi_hand_landmarks:
            lm = mano.landmark

            pulgar_punta = lm[mp_manos.HandLandmark.THUMB_TIP].y
            pulgar_base = lm[mp_manos.HandLandmark.THUMB_IP].y
            indice_punta = lm[mp_manos.HandLandmark.INDEX_FINGER_TIP].y
            indice_base = lm[mp_manos.HandLandmark.INDEX_FINGER_PIP].y
            medio_punta = lm[mp_manos.HandLandmark.MIDDLE_FINGER_TIP].y
            medio_base = lm[mp_manos.HandLandmark.MIDDLE_FINGER_PIP].y

            if pulgar_punta < pulgar_base and indice_punta > indice_base and medio_punta > medio_base:
                estado_detectado = "TA_BIEN"
            elif indice_punta < indice_base and medio_punta > medio_base and pulgar_punta > pulgar_base:
                estado_detectado = "BURLA"
            elif len(resultados_manos.multi_hand_landmarks) == 2:
                estado_detectado = "SORPRESA"

    # --- DETECCIÓN DE ROSTRO ---
    if estado_detectado == "NEUTRAL" and resultados_rostro.multi_face_landmarks:
        for rostro in resultados_rostro.multi_face_landmarks:

            labio_superior = rostro.landmark[13]
            labio_inferior = rostro.landmark[14]
            comisura_izq = rostro.landmark[61]
            comisura_der = rostro.landmark[291]

            apertura_boca = labio_inferior.y - labio_superior.y
            ancho_boca = math.hypot(comisura_der.x - comisura_izq.x,
                                    comisura_der.y - comisura_izq.y)

            if apertura_boca > 0.05:
                estado_detectado = "ASUSTADO"
            elif ancho_boca > 0.12:
                estado_detectado = "FELIZ"

    # ==========================================
    # 3. REACCIONES (POPUPS)
    # ==========================================
    tiempo_actual = time.time()

    if estado_detectado != "NEUTRAL" and not estado_reaccionando and imagenes_cargadas.get(estado_detectado):
        estado_reaccionando = True
        inicio_reaccion = tiempo_actual

        inicio_x = pos_x_camara + ancho_cam + 20
        inicio_y = pos_y_camara
        separacion = 15

        for i, imagen_popup in enumerate(imagenes_cargadas[estado_detectado]):
            nombre_ventana = f"Popup_{estado_detectado}_{i}"
            cv2.imshow(nombre_ventana, imagen_popup)

            pos_x = inicio_x + (i * (imagen_popup.shape[1] + separacion))
            cv2.moveWindow(nombre_ventana, pos_x, inicio_y)

            ventanas_activas.append(nombre_ventana)

    if estado_reaccionando and (tiempo_actual - inicio_reaccion > duracion_reaccion):
        estado_reaccionando = False

        for ventana in ventanas_activas:
            try:
                cv2.destroyWindow(ventana)
            except:
                pass

        ventanas_activas.clear()

    # ==========================================
    # 4. MOSTRAR CÁMARA
    # ==========================================
    cv2.putText(frame, f"ESTADO: {estado_detectado}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow(ventana_camara, frame)
    cv2.moveWindow(ventana_camara, pos_x_camara, pos_y_camara)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q') or tecla == 27:
        break

camara.release()
cv2.destroyAllWindows()