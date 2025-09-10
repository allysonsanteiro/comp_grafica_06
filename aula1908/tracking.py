import cv2
import time

# === CONFIG: caminho do vídeo ===
VIDEO_PATH = r"C:\Users\sante\OneDrive\Documentos\Allyson\ComputaçãoGrafica\aula1908\Media\video_street.mp4"  # troque para o seu arquivo

# --- abre o vídeo ---
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise FileNotFoundError(f"Não consegui abrir o vídeo: {VIDEO_PATH}")

# --- lê o primeiro frame ---
ok, frame = cap.read()
if not ok:
    cap.release()
    raise RuntimeError("Falha ao ler o primeiro frame.")

# --- seleção da ROI com o mouse ---
# Instruções: clique e arraste; ENTER/ESPAÇO confirma; ESC cancela
roi = cv2.selectROI("Selecione a área (ROI) e pressione ENTER/ESPAÇO", frame,
                    fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Selecione a área (ROI) e pressione ENTER/ESPAÇO")

if roi == (0, 0, 0, 0):
    cap.release()
    cv2.destroyAllWindows()
    raise ValueError("Nenhuma ROI válida foi selecionada.")

# --- cria o tracker KCF (compat. com OpenCV >= 4.x) ---
def create_kcf():
    if hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerKCF_create"):
        return cv2.legacy.TrackerKCF_create()
    if hasattr(cv2, "TrackerKCF_create"):
        return cv2.TrackerKCF_create()
    raise RuntimeError("KCF Tracker não disponível. Instale opencv-contrib-python.")

tracker = create_kcf()

# --- inicializa o tracker ---
ok_init = tracker.init(frame, roi)
if not ok_init:
    cap.release()
    cv2.destroyAllWindows()
    raise RuntimeError("Falha ao inicializar o tracker com a ROI.")

# --- loop de tracking ---
while True:
    ok, frame = cap.read()
    if not ok:
        break

    t0 = time.time()
    ok, box = tracker.update(frame)
    fps = 1.0 / max(time.time() - t0, 1e-6)

    if ok:
        x, y, w, h = map(int, box)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        status_txt = "OK"
    else:
        status_txt = "FALHOU"
        cv2.putText(frame, "Perda de tracking - pressione 'r' para redefinir ROI",
                    (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, f"KCF | FPS: {int(fps)} | {status_txt}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 200, 50), 2)

    cv2.imshow("KCF Tracking (ESC/Q sai | R redefine ROI)", frame)
    key = cv2.waitKey(1) & 0xFF

    if key in (27, ord('q')):  # ESC ou 'q'
        break

    if key == ord('r'):
        new_roi = cv2.selectROI("Redefinir ROI (ENTER/ESPAÇO confirma, ESC cancela)",
                                frame, False, True)
        cv2.destroyWindow("Redefinir ROI (ENTER/ESPAÇO confirma, ESC cancela)")
        if new_roi != (0, 0, 0, 0):
            tracker = create_kcf()
            tracker.init(frame, new_roi)

cap.release()
cv2.destroyAllWindows()