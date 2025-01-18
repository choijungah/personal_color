from fastapi import FastAPI, UploadFile, File
import uvicorn
import shutil
import os

from personal_color_classifier import PersonalColorClassifier

app = FastAPI()

# shape_predictor_68_face_landmarks.dat 파일 경로는 실제 경로로 수정해 주세요.
classifier = PersonalColorClassifier(
    "C:/stf/personal_color_class/shape_predictor_68_face_landmarks.dat"
)

# 최근 예측된 퍼스널 컬러를 저장할 전역 변수
last_predicted_color = None
last_uploaded_image_path = None  # 업로드된 이미지 경로를 저장할 변수 추가

# 업로드된 이미지를 저장할 폴더 경로
UPLOAD_FOLDER = "C:/stf/personal_color_class/Streamlit_app/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.post("/predict")
async def predict_personal_color(file: UploadFile = File(...)):
    """
    1) 업로드된 이미지를 서버 uploads 폴더에 저장
    2) PersonalColorClassifier로 퍼스널 컬러 예측
    3) 결과 반환 + 결과를 last_predicted_color에 저장
    """
    global last_predicted_color
    global last_uploaded_image_path  # 전역 변수 사용

    # 1) 업로드된 파일을 uploads 폴더에 저장
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2) 퍼스널 컬러 예측
    try:
        result = classifier.predict_personal_color(file_path)
        # 예측 성공 시, 전역 변수에 기록
        last_predicted_color = result
        last_uploaded_image_path = os.path.abspath(file_path)  # 절대 경로 저장
    except Exception as e:
        return {"error": str(e)}

    # 3) 예측 결과 반환
    return {"personal_color": result, "image_path": last_uploaded_image_path}  # 절대 경로 반환


@app.get("/last_result")
def get_last_result():
    """
    이전에 /predict로 예측한 결과가 있다면 반환,
    없다면 에러 메시지 반환
    """
    global last_predicted_color
    global last_uploaded_image_path  # 전역 변수 사용
    if not last_predicted_color:
        return {"error": "No result yet"}
    return {"personal_color": last_predicted_color, "image_path": last_uploaded_image_path}  # 이미지 경로 포함


if __name__ == "__main__":
    # uvicorn으로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
