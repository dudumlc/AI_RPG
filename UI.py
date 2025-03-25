from langchain_groq import ChatGroq 
from langchain.prompts import PromptTemplate
import streamlit as st
import os

# give title to the page
st.title('🤖 Teste RPG')

# Caixa de seleção do tema do RPG

if "desabilitado_tema" not in st.session_state:
    st.session_state["desabilitado_tema"] = False

def desabilitar_tema():
    st.session_state["desabilitado_tema"] = True

if "desabilitado_personagem" not in st.session_state:
    st.session_state["desabilitado_personagem"] = False

def desabilitar_personagem():
    st.session_state["desabilitado_personagem"] = True

tema = False
personagem= False

with st.expander("Configure as informações do RPG da maneira que quiser."):
    tema = st.text_area('1. Qual o tema do RPG que você deseja jogar?', key='tema',  disabled=st.session_state['desabilitado_tema'], on_change=desabilitar_tema)

    personagem = st.text_area("2. Descreva o seu personagem. Coloque todas as habilidades e características relevantes", key= 'personagem', disabled=st.session_state['desabilitado_personagem'], on_change=desabilitar_personagem)

    if tema and personagem:
        st.text("Tudo certo! O jogo já vai começar.")

# initialize session variables at the start once
if 'model' not in st.session_state:
    st.session_state['model'] = ChatGroq(api_key="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", model='qwen-2.5-32b')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Criando o Prompt Template
rpg_prompt = PromptTemplate(
    input_variables=["history", "user_input"],
    template=(
        """
        Você é um Mestre de RPG experiente, narrando uma aventura épica para os jogadores. 
        Utilize uma linguagem imersiva e descritiva. Responda de forma envolvente, sem revelar informações ocultas antes do momento certo. Use descrições detalhadas para ambientação.\n\n
        O jogador escolheu o tema do RPG como {tema}. Dessa forma, crie situações criativas e envolventes apenas dentro dessa temática.\n\n
        Além disso, o personagem do jogador tem a seguinte descrição: {personagem}. Crie situações que potencializem as habilidades e características do personagem criado.\n\n 
        Histórico da aventura:\n{history}\n\n
        Jogador: {user_input}\n
        Mestre:
        """
    )
)

# create sidebar to adjust parameters
#st.sidebar.title('Model Parameters')
#temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
#max_tokens = st.sidebar.slider('Max Tokens', min_value=1, max_value=4096, value=256)

# update the interface with the previous messages
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

### TESTEEEEEEE
model = st.session_state['model']
if tema and personagem:
    prompt_intro = """
        Você é um Mestre de RPG experiente, narrando uma aventura épica para os jogadores. 
        Utilize uma linguagem imersiva e descritiva. Responda de forma envolvente, sem revelar informações ocultas antes do momento certo. Use descrições detalhadas para ambientação.\n\n
        O jogador escolheu o tema do RPG como {tema}. Dessa forma, crie situações criativas e envolventes apenas dentro dessa temática.\n\n
        Além disso, o personagem do jogador tem a seguinte descrição: {personagem}. Crie situações que potencializem as habilidades e características do personagem criado.\n\n
        Faça uma introdução do RPG e crie a primeira situação para o usuário jogar.
        """
    intro = model.invoke(prompt_intro.format(tema=tema, personagem=personagem)).content

    st.session_state['messages'].append({"role": "assistant", "content": intro})
    with st.chat_message('assistant'):
        st.markdown(intro)

# create the chat interface
if prompt := st.chat_input("Digite sua ação"):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # Criar o prompt final com histórico e entrada do usuário
    final_prompt = rpg_prompt.format(history=st.session_state['messages'], user_input=prompt, tema= tema, personagem= personagem)
    
    # Obtém a resposta do modelo
    model = st.session_state['model']
    response = model.invoke(final_prompt).content

    # Adiciona a resposta do assistente ao histórico
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # Exibe a resposta do assistente na interface
    with st.chat_message('assistant'):
        st.markdown(response)
