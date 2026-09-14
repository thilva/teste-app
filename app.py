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
        with st.spinner("A processar as informações desportivas mais recentes..."):
            try:
            try:
                # CORREÇÃO DEFINITIVA PARA O ERRO 401:
                # Passamos a chave de forma explícita e configuramos também o parâmetro http_options 
                # para garantir que o cabeçalho correto de API Key é enviado.
                client = genai.Client(
                    api_key=api_key,
                    http_options={'headers': {'x-goog-api-key': api_key}}
                )
                
                # Faz a chamada direta ao modelo 
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Você é um assistente desportivo em tempo real. Forneça as informações desportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                )
                
                # Exibe o resultado no ecrã do Streamlit
                st.subheader("📊 Resultados Encontrados:")
                st.markdown(response.text)


            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
                st.info("Verifique se a sua chave de API está correta.")
