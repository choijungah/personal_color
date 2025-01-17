# app.py
import streamlit as st
import requests
import os

def main():
    st.title("Personal Color - Streamlit (app.py)")
    st.subheader("No upload here. We just fetch the last predicted result from FastAPI.")

    # 1) FastAPI의 /last_result 에서 최근 퍼스널컬러 가져오기
    #    (미리 main.py에서 /predict 로 이미지 업로드 & 예측을 한번 진행했다고 가정)
    fastapi_url = "http://127.0.0.1:8000/last_result"

    try:
        response = requests.get(fastapi_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to FastAPI server: {e}")
        return

    data = response.json()
    # data 예: {"personal_color": "spring"} or {"error": "..."}
    if "error" in data:
        st.error(f"Server error: {data['error']}")
        return

    personal_color = data["personal_color"]
    st.success(f"Your personal color is: {personal_color}")

    # 2) 해당 폴더(../../images/{personal_color})에 있는 모든 이미지를 띄우기
    base_dir = os.path.dirname(__file__)  # app.py가 위치한 폴더 (pages/)
    folder_path = os.path.join(base_dir, "..", "..", "images", personal_color)

    if os.path.isdir(folder_path):
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        if not image_files:
            st.warning(f"No images found in {folder_path}")
        else:
            st.write(f"Found {len(image_files)} images in {folder_path}:")
            for image_file in sorted(image_files):
                full_path = os.path.join(folder_path, image_file)
                st.image(full_path, caption=image_file)
    else:
        st.warning(f"Folder not found: {folder_path}")

if __name__ == "__main__":
    main()
