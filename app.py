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

try:
    if not api_key:
        st.error("Por favor, insira a sua Chave de API para continuar.")
    elif not query:
        st.warning("Por favor, digite o que deseja procurar.")
    else:
        with st.spinner("A aceder à internet e a procurar as informações mais recentes..."):
            try:
                # 1. Inicializa o cliente oficial com a nova chave AQ...
                client = genai.Client(api_key=api_key)
                
                # 2. Configura o modelo para pesquisar na Web (Google Search Grounding)
                # Isso resolve o erro 404/405 e traz dados de hoje/ao vivo
                config = types.GenerateContentConfig(
                    google_search_retrieval=types.GoogleSearchRetrieval(
                        dynamic_retrieval_config=types.DynamicRetrievalConfig(
                            mode="MODE_DYNAMIC",
                            dynamic_threshold=0.3,
                        )
                    )
                )
                
                # 3. Faz a chamada ao modelo adequado (gemini-2.5-flash)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Forneça as informações desportivas mais recentes e em tempo real sobre: {query}",
                    config=config
                )
                
                # 4. Exibe o resultado na tela
                st.subheader("📊 Resultados Encontrados:")
                st.markdown(response.text)
                
                # Exibe as fontes da pesquisa se disponíveis
                if response.candidates and response.candidates[0].grounding_metadata:
                    metadata = response.candidates[0].grounding_metadata
                    if metadata.web_search_queries:
                        st.info(f"Fontes pesquisadas: {', '.join(metadata.web_search_queries)}")

            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
                st.info("Verifique se a sua chave de API está correta e se a biblioteca 'google-genai' está atualizada.")
