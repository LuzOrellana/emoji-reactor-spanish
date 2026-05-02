import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import os
import time
import math

# ==========================================
# 1. SETUP MEDIA PIPE E PASTAS
# ==========================================
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def load_jpg(path, base_size=(250, 250)):
    try:
        img_pil = Image.open(path).convert("RGB")
        img_pil = img_pil.resize(base_size, Image.Resampling.LANCZOS)
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
        return None

image_files = {
    "THUMBS_UP": ["thumbsup_1.jpg", "thumbsup_2.jpg", "thumbsup_3.jpg", "thumbsup_4.jpg", "thumbsup_5.jpg"],
    "HAPPY": ["happy_1.jpg", "happy_2.jpg", "happy_3.jpg", "happy_4.jpg", "happy_5.jpg"],
    "SCARY": ["scaryface_1.jpg", "scaryface_2.jpg", "scaryface_3.jpg", "scaryface_4.jpg", "scaryface_5.jpg"],
    "YOU": ["you_1.jpg", "you_2.jpg", "you_3.jpg"]
}

# Carrega na memória RAM para zero lag
loaded_images = {}
for category, files in image_files.items():
    loaded_images[category] = []
    for f in files:
        path = os.path.join("assets", f)
        img = load_jpg(path)
        if img is not None:
            loaded_images[category].append(img)

# ==========================================
# 2. SISTEMA DE COOLDOWN E JANELAS
# ==========================================
cap = cv2.VideoCapture(0)

CAM_WINDOW = "Camera Feed"
CAM_X, CAM_Y = 50, 100  # Posição fixa da câmera na tela

is_reacting = False
reaction_start_time = 0
REACTION_DURATION = 2.0  # Tempo que os pop-ups ficam na tela
active_windows = []      # Lista para guardar as janelas abertas

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    cam_h, cam_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)

    detected_state = "NEUTRAL"

    # --- LÓGICA DAS MÃOS ---
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            
            thumb_tip = lm[mp_hands.HandLandmark.THUMB_TIP].y
            thumb_ip = lm[mp_hands.HandLandmark.THUMB_IP].y
            index_tip = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_pip = lm[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            middle_tip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            middle_pip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            
            if thumb_tip < thumb_ip and index_tip > index_pip and middle_tip > middle_pip:
                detected_state = "THUMBS_UP"
            elif index_tip < index_pip and middle_tip > middle_pip and thumb_tip > thumb_ip:
                detected_state = "YOU"

    # --- LÓGICA DO ROSTO ---
    if detected_state == "NEUTRAL" and face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            # Pegando as coordenadas reais usando trigonometria
            upper_lip = face_landmarks.landmark[13]
            lower_lip = face_landmarks.landmark[14]
            mouth_left = face_landmarks.landmark[61]
            mouth_right = face_landmarks.landmark[291]
            
            # Cálculo de abertura (Vertical) e largura (Horizontal)
            mouth_opening = lower_lip.y - upper_lip.y
            mouth_width = math.hypot(mouth_right.x - mouth_left.x, mouth_right.y - mouth_left.y)
            
            # Ajuste de Sensibilidade: 
            # Checa PRIMEIRO se a boca está bem aberta (abaixamos de 0.08 para 0.05)
            if mouth_opening > 0.05:
                detected_state = "SCARY"
            # Se não está aberta o suficiente para ser um grito, checa se está larga (sorriso)
            elif mouth_width > 0.12:
                detected_state = "HAPPY"

    # ==========================================
    # 3. RENDERIZAÇÃO ESTÉTICA (Bateria de Pop-ups)
    # ==========================================
    current_time = time.time()

    # Dispara os pop-ups apenas se não estiver em cooldown
    if detected_state != "NEUTRAL" and not is_reacting and loaded_images.get(detected_state):
        is_reacting = True
        reaction_start_time = current_time
        
        start_x = CAM_X + cam_w + 20 # Nasce logo à direita da câmera
        start_y = CAM_Y
        spacing = 15 # Espaço de 15px entre as janelas
        
        # Abre todas as imagens da pasta lado a lado
        for i, img_to_show in enumerate(loaded_images[detected_state]):
            win_name = f"React_{detected_state}_{i}"
            cv2.imshow(win_name, img_to_show)
            
            # Calcula a posição de cada imagem na fila
            pos_x = start_x + (i * (img_to_show.shape[1] + spacing))
            cv2.moveWindow(win_name, pos_x, start_y)
            
            # Guarda o nome da janela para fechar depois
            active_windows.append(win_name)

    # Fecha todas as janelas extras após 2 segundos
    if is_reacting and (current_time - reaction_start_time > REACTION_DURATION):
        is_reacting = False
        for win in active_windows:
            try:
                cv2.destroyWindow(win)
            except:
                pass
        active_windows.clear()

    # Exibe a câmera com o status
    cv2.putText(frame, f"STATUS: {detected_state}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow(CAM_WINDOW, frame)
    cv2.moveWindow(CAM_WINDOW, CAM_X, CAM_Y)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()