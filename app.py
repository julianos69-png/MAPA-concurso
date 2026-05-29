import streamlit as st
import requests
import json

# CONFIGURAÇÃO DA INTERFACE
st.set_page_config(page_title="IA Concursos Jurídicos", page_icon="⚖️")
st.title("⚖️ Simulador de Casos Práticos para Concursos")
st.write("Treine para a fase discursiva com casos inéditos baseados na jurisprudência.")

# Recupera a API Key dos Secrets do Streamlit
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Por favor, configure a sua GEMINI_API_KEY nos Secrets.")
    st.stop()

# FUNÇÃO DE CONEXÃO DIRETA COM A API ESTÁVEL DO GOOGLE
def chamar_gemini(prompt_texto):
    # Mudança crucial: Usando a rota v1 estável e o modelo correto da geração atual
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_texto}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            dados = response.json()
            # Extrai o texto da resposta do formato padrão do Google
            return dados['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erro na API do Google (Código {response.status_code}): {response.text}"
    except Exception as e:
        return f"Erro de conexão de rede: {e}"

# SELEÇÃO DA MATÉRIA
materia = st.selectbox("Escolha a matéria:", ["Direito Penal", "Direito Constitucional", "Direito Administrativo"])

if "caso_gerado" not in st.session_state:
    st.session_state.caso_gerado = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Botão para gerar o caso
if st.button("Gerar Novo Caso Prático 🚀"):
    with st.spinner("A banca está elaborando a sua questão..."):
        prompt = f"Atue como banca examinadora de concurso jurídico de alta performance. Crie um caso prático complexo e inédito sobre {materia}, baseado em jurisprudência recente do STF/STJ. Ao final, faça 1 ou 2 perguntas discursivas. Não dê a resposta ou o gabarito."
        st.session_state.caso_gerado = chamar_gemini(prompt)
        st.session_state.feedback = ""

if st.session_state.caso_generated := st.session_state.caso_gerado:
    st.subheader("📝 Caso Prático Proposto:")
    st.info(st.session_state.caso_generated)
    
    resposta_aluno = st.text_area("Digite sua resposta fundamentada aqui:", height=250)
    
    if st.button("Enviar Resposta para Correção 📤"):
        if not resposta_aluno:
            st.warning("Por favor, digite uma resposta antes de enviar.")
        else:
            with st.spinner("O examinador está avaliando sua resposta..."):
                prompt_correcao = f"Você é o examinador que criou este caso:\n{st.session_state.caso_generated}\n\nO aluno respondeu:\n{resposta_aluno}\n\nFaça uma correção detalhada dando nota de 0 a 10, pontos positivos, pontos a melhorar e o gabarito ideal com base na lei."
                st.session_state.feedback = chamar_gemini(prompt_correcao)

if st.session_state.feedback:
    st.subheader("📊 Avaliação da Banca Examinadora:")
    st.success(st.session_state.feedback)
