import streamlit as st
import base64

def main():
    # 1. 페이지 레이아웃 설정
    st.set_page_config(layout="wide")

    # 2. 상단 메뉴, 푸터 등 숨기기
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 3. 배경 이미지 로드
    background_image_path = "homepgim.jpg"
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    background_image_base64 = get_base64_of_bin_file(background_image_path)

    # 4. CSS: 화면 전체를 Flex로 중앙 정렬
    css_code = f"""
    <style>
    /* 화면 전체 높이 및 여백 제거 */
    html, body, [data-testid="stAppViewContainer"],
    .main, .block-container, .stApp {{
        height: 100%;
        margin: 0;
        padding: 0;
    }}

    /* 수직·수평 중앙 정렬 */
    .stApp {{
        display: flex;
        flex-direction: column;
        justify-content: center;  /* 세로 중앙 정렬 */
        align-items: center;      /* 가로 중앙 정렬 */
        background: url("data:image/jpg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* 텍스트 스타일 + 중앙에서 약간 오른쪽으로 이동(margin-left) */
    .center-text {{
        font-size: 40px;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        white-space: nowrap;
        margin-left: 100px; /* 중앙에서 오른쪽으로 100px 만큼 이동 */
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

    # 5. 텍스트 + 인위적 줄바꿈
    center_text = """
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <div class="center-text">
        패션의 모든 것<br>
        AURA에서 쉽고 간편하게
    </div>
    """
    st.markdown(center_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
