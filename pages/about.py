import streamlit as st
from menu import menu
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)
st.title("EasyPressure")
def main():
    # CSS-Stil definieren
    st.markdown("""
    <style>
    .mixed-color-text {
        color: #20B2AA; /* Farbe #20B2AA */
    }
    .name {
        font-size: 24px;
    }
    .nowrap {
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

    # Informationen über das Entwicklerteam
    st.markdown("""
    ## Unser Team:
    - <span class="name mixed-color-text">**Amal Osmanov:**</span> Student der Biomedizinischen Labordiagnostik Bachelor an der ZHAW <span class="nowrap">Wädenswil</span>
        - <span class="mixed-color-text">**Interessen:**</span> Biologie, Medizin, Genetik, Molekularbiologie
        - <span class="mixed-color-text">**Hobbies:**</span> Gitarre, Reisen, Logik
        - <span class="mixed-color-text">**Kontakt:**</span> [osmanama@students.zhaw.ch](mailto:osmanama@students.zhaw.ch), [LinkedIn](https://www.linkedin.com/in/amal-osmanov)
    - <span class="name mixed-color-text">**Zuzana Dvorak:**</span> Studentin der Biomedizinischen Labordiagnostik Bachelor an der ZHAW <span class="nowrap">Wädenswil</span>
        - <span class="mixed-color-text">**Interessen:**</span> Biomedizin, Biochemie, Chemie, Pharmazie, Histologie, Hämatologie
        - <span class="mixed-color-text">**Hobbies:**</span> Sport, River Crusing, Musik, Tanzen, Kulturtourismus, Wissenschaft
        - <span class="mixed-color-text">**Kontakt:**</span> [dvorazuz@students.zhaw.ch](mailto:dvorazuz@students.zhaw.ch), [LinkedIn](https://www.linkedin.com/in/zuzana-dvorak)
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()