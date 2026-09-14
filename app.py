import streamlit as st
from google import genai
from google.genai import types

# Configuração da página do Streamlit
st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados, jogos e notícias desportivas mais recentes com o Gemini.")

# Entrada da Chave de API (Começando com AQ...)
api_key = st.text_input("AQ.Ab8RN6LRVXTnfUKdoTqVNbE1FA1T-AFq2gPfiQzNnmUBZuSAMA", type="password")

# Entrada da pesquisa do utilizador
query = st.text_input(
    "O que deseja procurar?", 
    placeholder="Ex: Resultados dos jogos da Champions League de hoje"
)

if st.button("Buscar Informações"):
    if not api_key:
        st.error("Por favor, insira a sua Chave de API para continuar.")
    elif not query:
        st.warning("Por favor, digite o que deseja procurar.")
    else:
        with st.spinner("A aceder à internet e a procurar as informações mais recentes..."):
            try:
            try:
                # 1. Inicializa o cliente oficial com a sua chave AQ...
                client = genai.Client(api_key=api_key)
                
                # CORREÇÃO DEFINITIVA: Removemos o 'config' completamente para eliminar o erro do Pydantic.
                # Forçamos o modelo a trazer dados recentes diretamente pelo comando de texto.
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Você é um assistente desportivo em tempo real. Forneça as informações desportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                )
                
                # 4. Exibe o resultado no ecrã do Streamlit
                st.subheader("📊 Resultados Encontrados:")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
                st.info("Verifique se a sua chave de API está correta.")
