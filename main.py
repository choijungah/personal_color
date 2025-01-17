# main.py
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
# 실제 서비스라면 DB나 캐시 사용을 권장하지만, 여기서는 예시로 전역 변수 사용
last_predicted_color = None

@app.post("/predict")
async def predict_personal_color(file: UploadFile = File(...)):
    """
    1) 업로드된 이미지를 서버 임시 파일로 저장
    2) PersonalColorClassifier로 퍼스널 컬러 예측
    3) 결과 반환 + 결과를 last_predicted_color에 저장
    """
    global last_predicted_color

    # 1) 업로드된 파일을 임시 경로로 저장
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2) 퍼스널 컬러 예측
    try:
        result = classifier.predict_personal_color(temp_filename)
        # 예측 성공 시, 전역 변수에 기록
        last_predicted_color = result
    except Exception as e:
        return {"error": str(e)}
    finally:
        # 임시 파일 제거
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    # 3) 예측 결과 반환
    return {"personal_color": result}


@app.get("/last_result")
def get_last_result():
    """
    이전에 /predict로 예측한 결과가 있다면 반환,
    없다면 에러 메시지 반환
    """
    global last_predicted_color
    if not last_predicted_color:
        return {"error": "No result yet"}
    return {"personal_color": last_predicted_color}


if __name__ == "__main__":
    # uvicorn으로 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
