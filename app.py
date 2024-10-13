import streamlit as st
from core.lexer import Lexer, LexerError
from core.parser import JSONParser
from utils.json_utils import parsedData_to_patient_record

def load_readme():
    """Função para carregar e exibir o conteúdo do README.md"""
    with open("readme.md", "r", encoding="utf-8") as file:
        return file.read()

def display_patient_dashboard(patient_record):
    """Função para exibir o relatório do paciente como um dashboard moderno"""
    # Acessando corretamente as informações pessoais
    st.subheader(f"Patient: {patient_record.patient_info.name}")

    # Informações pessoais
    st.markdown(f"**ID:** {patient_record.patient_info.patient_id}")
    st.markdown(f"**Age:** {patient_record.patient_info.age}")
    st.markdown(f"**Gender:** {patient_record.patient_info.gender}")

    st.divider()

    # Histórico Médico
    st.markdown("### Medical History")
    for history in patient_record.medical_history:
        st.markdown(
            f"- **Condition:** {history.condition} "
            f"(**Diagnosed Date:** {history.diagnosed_date}, **Status:** {history.status})"
        )

    st.divider()

    # Consultas
    st.markdown("### Consultations")
    for consultation in patient_record.consultations:
        st.markdown(
            f"- **Date:** {consultation.date}\n"
            f"  - **Doctor:** {consultation.doctor}\n"
            f"  - **Symptoms:** {consultation.symptoms}\n"
            f"  - **Diagnosis:** {consultation.diagnosis}"
        )



def main():
    st.set_page_config(page_title="Recursive Syntactic Analyzer", layout="wide")
    
    # Controle de estado para exibir README ou aplicação
    if "show_readme" not in st.session_state:
        st.session_state.show_readme = True

    # Alternância entre README e aplicação
    if st.session_state.show_readme:
        if st.button("Ir para Aplicação", key="to_app"):
            st.session_state.show_readme = False
        st.markdown(load_readme(), unsafe_allow_html=True)
    else:
        if st.button("Ver README", key="to_readme"):
            st.session_state.show_readme = True
        
        # Interface principal da aplicação
        st.title('Recursive Syntactic Analyzer')

        st.subheader("JSON Input")
        user_input = st.text_area("Enter JSON:", height=300)

        if st.button("Analyze"):
            try:
                # Lexer e Parser
                lexer = Lexer(user_input)
                tokens = lexer.generate_tokens()
                st.success("Tokens generated successfully!")

                parser = JSONParser(tokens)
                parsed_data = parser.parse()
                patient_record = parsedData_to_patient_record(parsed_data)

                # Dashboard do paciente
                st.success("Parsed Data:")
                st.write(patient_record)
                st.divider()
                display_patient_dashboard(patient_record)

            except LexerError as e:
                st.error(f"Erro encontrado: {str(e)}")

if __name__ == '__main__':
    main()
