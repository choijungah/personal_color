# personal_color_classifier.py
import cv2
import dlib
import numpy as np
from sklearn.cluster import KMeans

class PersonalColorClassifier:
    def __init__(self, shape_predictor_path: str):
        # dlib 모델 로드
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)

    def get_facial_landmarks(self, image: np.ndarray):
        # 1) dlib로 얼굴 감지 후, 첫 얼굴만 랜드마크 추출
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray, 1)
        if len(faces) == 0:
            return None
        face = faces[0]
        shape = self.predictor(gray, face)
        return shape

    def extract_regions(self, image: np.ndarray, shape: dlib.full_object_detection):
        # 2) 눈/입술/피부 영역을 각각 mask로 분리 후, 해당 픽셀(BGR)만 추출
        left_eye_points = [36, 37, 38, 39, 40, 41]
        right_eye_points = [42, 43, 44, 45, 46, 47]
        lip_points = list(range(48, 60))
        # 턱선 중 일부를 skin 영역 예시로 사용
        skin_points = list(range(2, 15))

        mask_eyes = np.zeros(image.shape[:2], dtype=np.uint8)
        mask_lips = np.zeros(image.shape[:2], dtype=np.uint8)
        mask_skin = np.zeros(image.shape[:2], dtype=np.uint8)

        def fill_polygon(mask, indices):
            pts = [(shape.part(i).x, shape.part(i).y) for i in indices]
            pts = np.array(pts, dtype=np.int32)
            cv2.fillConvexPoly(mask, pts, 255)

        fill_polygon(mask_eyes, left_eye_points + right_eye_points)
        fill_polygon(mask_lips, lip_points)
        fill_polygon(mask_skin, skin_points)

        eyes_region = image[mask_eyes == 255]
        lips_region = image[mask_lips == 255]
        skin_region = image[mask_skin == 255]

        return eyes_region, lips_region, skin_region

    def get_dominant_color(self, image_region: np.ndarray, k: int = 1):
        # 3) K-means(k=1)로 영역 대표색(BGR) 추출
        if len(image_region) == 0:
            return (0, 0, 0)
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(image_region)
        dominant_bgr = kmeans.cluster_centers_[0]
        return tuple(map(int, dominant_bgr))

    def classify_personal_color(self, eyes_bgr, lips_bgr, skin_bgr):
        # 4) (눈,입술,피부) BGR값을 가중평균 후, LAB 변환 → 임계값 기준으로 분류
        avg_b = eyes_bgr[0] * 0.3 + lips_bgr[0] * 0.3 + skin_bgr[0] * 0.4
        avg_g = eyes_bgr[1] * 0.3 + lips_bgr[1] * 0.3 + skin_bgr[1] * 0.4
        avg_r = eyes_bgr[2] * 0.3 + lips_bgr[2] * 0.3 + skin_bgr[2] * 0.4

        color_1x1 = np.uint8([[[avg_b, avg_g, avg_r]]])
        lab_1x1 = cv2.cvtColor(color_1x1, cv2.COLOR_BGR2LAB)[0, 0]
        L_lab, a_lab, b_lab = lab_1x1

        # warm/cool 여부
        if b_lab >= 138:
            warm_or_cool = "warm"
        else:
            warm_or_cool = "cool"

        # spring/autumn / summer/winter
        if warm_or_cool == "warm":
            if L_lab >= 147:
                season = "spring"
            else:
                season = "autumn"
        else:
            if L_lab >= 140:
                season = "summer"
            else:
                season = "winter"
        return season

    def predict_personal_color(self, image_path: str) -> str:
        # 5) 최종적으로 외부에서 호출되는 함수(이미지 경로 -> 퍼스널 컬러 결과)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"[ERROR] Cannot read image: {image_path}")

        shape = self.get_facial_landmarks(image)
        if shape is None:
            raise ValueError("[ERROR] No face found in image.")

        eyes_region, lips_region, skin_region = self.extract_regions(image, shape)
        eyes_bgr = self.get_dominant_color(eyes_region)
        lips_bgr = self.get_dominant_color(lips_region)
        skin_bgr = self.get_dominant_color(skin_region)

        result = self.classify_personal_color(eyes_bgr, lips_bgr, skin_bgr)
        return result