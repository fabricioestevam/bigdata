"""
Detector de Ônibus - YOLO + OCR
"""
from ultralytics import YOLO
import easyocr
import cv2
import numpy as np


class BusDetector:
    """
    Detecta ônibus em imagens usando YOLOv8 + EasyOCR
    """
    
    def __init__(self, linhas_validas):
        """
        Args:
            linhas_validas: lista de linhas válidas (ex: ["437", "2441", ...])
        """
        self.linhas_validas = linhas_validas
        self.model = YOLO("yolov8n.pt")
        self.reader = easyocr.Reader(['pt', 'en'], gpu=False)
        print(f"✅ BusDetector inicializado ({len(linhas_validas)} linhas)")
    
    def detectar_linha(self, img):
        """
        Detecta ônibus e identifica linha do letreiro
        
        Args:
            img: imagem numpy array (BGR)
            
        Returns:
            str ou None: número da linha detectada
        """
        try:
            # 1. YOLO detecta ônibus
            results = self.model(img, conf=0.5)[0]
            
            for det in results.boxes:
                cls_id = int(det.cls[0])
                class_name = self.model.names[cls_id]
                
                if class_name == "bus":
                    confidence = float(det.conf[0])
                    print(f"🚌 Ônibus detectado (conf: {confidence:.2f})")
                    
                    # 2. Recortar região do ônibus
                    x1, y1, x2, y2 = map(int, det.xyxy[0])
                    onibus_crop = img[y1:y2, x1:x2]
                    
                    if onibus_crop.size == 0:
                        continue
                    
                    # 3. Focar no letreiro (parte superior)
                    altura = onibus_crop.shape[0]
                    letreiro_crop = onibus_crop[0:int(altura*0.35), :]
                    
                    # 4. Pré-processamento
                    gray = cv2.cvtColor(letreiro_crop, cv2.COLOR_BGR2GRAY)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    enhanced = clahe.apply(gray)
                    thresh = cv2.adaptiveThreshold(
                        enhanced, 255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY, 11, 2
                    )
                    
                    # 5. OCR
                    print("🔍 Executando OCR...")
                    ocr_results = self.reader.readtext(thresh)
                    
                    # 6. Procurar linhas válidas
                    for (bbox, text, conf_ocr) in ocr_results:
                        numeros = ''.join(filter(str.isdigit, text))
                        print(f"   OCR: '{text}' → '{numeros}' (conf: {conf_ocr:.2f})")
                        
                        if numeros in self.linhas_validas and conf_ocr > 0.4:
                            print(f"✅ LINHA {numeros} IDENTIFICADA!")
                            return numeros
            
            print("ℹ️  Nenhuma linha válida detectada")
            return None
            
        except Exception as e:
            print(f"❌ Erro na detecção: {e}")
            return None