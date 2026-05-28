import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO DA IA (Pegando a chave de segurança do Streamlit)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Por favor, configure a sua GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')
# CONFIGURAÇÃO DA INTERFACE DO USUÁRIO
st.set_page_config(page_title="IA Concursos Jurídicos", page_icon="⚖️")
st.title("⚖️ Simulador de Casos Práticos para Concursos")
st.write("Treine para a fase discursiva com casos inéditos baseados na jurisprudência.")

# PASSO 1: Seleção da Matéria
materia = st.selectbox(
    "Escolha a matéria que deseja treinar:",
    ["Direito Penal", "Direito Constitucional", "Direito Administrativo"]
)

# Inicializando variáveis de estado para o app não "esquecer" o caso gerado
if "caso_gerado" not in st.session_state:
    st.session_state.caso_gerado = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# PROMPT 1: Comando para gerar o caso prático
prompt_gerador = f"""
Atue como um membro de banca examinadora de concursos públicos jurídicos de alta performance (como Magistratura ou Ministério Público).
Crie um caso prático inédito e fictício sobre {materia}.
O caso deve ser complexo, envolver uma situação fática detalhada e exigir que o candidato conheça a jurisprudência recente do STF ou STJ.
Ao final do caso, faça de 1 a 2 perguntas discursivas e diretas sobre a situação.
Não dê a resposta ou o gabarito ainda.
"""

# Botão para gerar o caso
if st.button("Gerar Novo Caso Prático 🚀"):
    with st.spinner("A banca está elaborando a sua questão..."):
        try:
            response = model.generate_content(prompt_gerador)
            st.session_state.caso_gerado = response.text
            st.session_state.feedback = "" # Limpa o feedback anterior
        except Exception as e:
            st.error(f"Erro ao conectar com a IA: {e}")

# Se o caso já foi gerado, mostra na tela
if st.session_state.caso_gerado:
    st.subheader("📝 Caso Prático Proposto:")
    st.info(st.session_state.caso_gerado)
    
    # PASSO 2: Campo para o aluno responder
    resposta_aluno = st.text_area("Digite sua resposta fundamentada aqui (cite artigos e jurisprudência se lembrar):", height=250)
    
    # Botão para enviar a resposta
    if st.button("Enviar Resposta para Correção 📤"):
        if not resposta_aluno:
            st.warning("Por favor, digite uma resposta antes de enviar.")
        else:
            # PROMPT 2: Comando para avaliar a resposta do aluno
            prompt_avaliador = f"""
            Você é o examinador da banca de concurso jurídico que criou o seguinte caso prático:
            ---
            {st.session_state.caso_gerado}
            ---
            
            O aluno enviou a seguinte resposta para a sua avaliação:
            ---
            {resposta_aluno}
            ---
            
            Faça uma correção criteriosa e profissional da resposta do aluno. Seu retorno deve conter:
            1. Uma nota de 0 a 10.
            2. Pontos Positivos: O que o aluno acertou.
            3. Pontos de Melhoria: O que ele esqueceu de mencionar, teses jurídicas omitidas ou erros de capitulação legal.
            4. Gabarito Ideal: Uma breve explicação de qual seria a resposta perfeita com base na lei e na jurisprudência do STF/STJ.
            
            Seja firme na correção, simulando uma banca real, mas construtivo.
            """
            
            with st.spinner("O examinador está corrigindo sua prova..."):
                try:
                    response_correcao = model.generate_content(prompt_avaliador)
                    st.session_state.feedback = response_correcao.text
                except Exception as e:
                    st.error(f"Erro ao gerar correção: {e}")

# Se houver feedback, mostra na tela
if st.session_state.feedback:
    st.subheader("📊 Avaliação da Banca Examinadora:")
    st.success(st.session_state.feedback)
