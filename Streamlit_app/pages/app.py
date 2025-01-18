import streamlit as st
import requests
import os
from PIL import Image

def main():
    # 1) 페이지 레이아웃
    st.set_page_config(layout="wide")

    # 2) 상단 메뉴, 푸터 감추기
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 3) FastAPI의 /last_result 에서 최근 퍼스널컬러 가져오기
    fastapi_url = "http://127.0.0.1:8000/last_result"

    try:
        response = requests.get(fastapi_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to FastAPI server: {e}")
        return

    data = response.json()
    if "error" in data:
        st.error(f"Server error: {data['error']}")
        return

    personal_color = data["personal_color"]
    image_path = data.get("image_path")

    # ───────────── 텍스트를 HTML로 가운데 정렬 ─────────────
    st.markdown("<h1 style='text-align:center;'>퍼스널 컬러 진단 중 ...</h1>", unsafe_allow_html=True)

    # 퍼스널컬러별 안내문 (subheader 대신 Markdown + HTML)
    if personal_color == "spring":
        st.markdown(
            "<h3 style='text-align:center;'>(테이비) 님의 퍼스널 컬러는 Spring Warm 입니다.</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;'>이 퍼스널 컬러에 해당하는 연예인으로는 아이유, 이종석, 윈터, 윤아 등이 있습니다.</p>",
            unsafe_allow_html=True
        )
    elif personal_color == "summer":
        st.markdown(
            "<h3 style='text-align:center;'>(테이비) 님의 퍼스널 컬러는 Summer Cool 입니다.</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;'>이 퍼스널 컬러에 해당하는 연예인으로는 정채연, 아이린, 장원영, 태연 등이 있습니다.</p>",
            unsafe_allow_html=True
        )
    elif personal_color == "autumn":
        st.markdown(
            "<h3 style='text-align:center;'>(테이비) 님의 퍼스널 컬러는 Autumn Warm 입니다.</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;'>이 퍼스널 컬러에 해당하는 연예인으로는 제니, 이효리, 신세경, 이성경 등이 있습니다.</p>",
            unsafe_allow_html=True
        )
    elif personal_color == "winter":
        st.markdown(
            "<h3 style='text-align:center;'>(테이비) 님의 퍼스널 컬러는 Winter Cool 입니다.</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align:center;'>이 퍼스널 컬러에 해당하는 연예인으로는 지수, 김혜수, 카리나, 임지연 등이 있습니다.</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<h3 style='text-align:center;'>(테이비) 님의 퍼스널 컬러는 {personal_color} 입니다.</h3>",
            unsafe_allow_html=True
        )

    # ───────────── 업로드된 원본 이미지를 가운데 정렬, 크게 표시 ─────────────
    if image_path:
        try:
            uploaded_image = Image.open(image_path)
            uploaded_image = uploaded_image.resize((400, 600))

            # 이미지 앞뒤로 <div style='text-align:center;'> ... </div> 감싸기
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)  # 추가
            st.image(uploaded_image, caption="업로드된 이미지", use_container_width=False, width=400)
            st.markdown("</div>", unsafe_allow_html=True)  # 추가

        except Exception as e:
            st.error(f"Failed to load image: {e}")

    # 4) 해당 폴더(../../images/{personal_color})에 있는 모든 이미지를 띄우기
    base_dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(base_dir, "..", "..", "images", personal_color))

    if os.path.isdir(folder_path):
        image_files = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        if not image_files:
            st.warning(f"No images found in {folder_path}")
        else:
            # 이미지들을 4개씩 가로로 나열
            cols = st.columns(4)
            for i, image_file in enumerate(sorted(image_files)):
                full_path = os.path.join(folder_path, image_file)
                with cols[i % 4]:
                    try:
                        color_image = Image.open(full_path)
                        color_image = color_image.resize((150, 225))
                        st.image(color_image, caption=image_file, use_container_width=False, width=150)
                    except Exception as e:
                        st.error(f"Failed to load image {image_file}: {e}")
    else:
        st.warning(f"Folder not found: {folder_path}")

if __name__ == "__main__":
    main()