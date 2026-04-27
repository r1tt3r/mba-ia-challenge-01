import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate

load_dotenv()
for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    context = getContext(question)

    question_template = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )

    model = ChatOpenAI(model="gpt-5-nano", temperature=0.5)
    chain = question_template | model
    result = chain.invoke({"pergunta": question, "contexto": context})

    print(f"Answer: {result.content}")



def getContext(question):
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))
    store = PGVector(
      embeddings=embeddings,
      collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
      connection=os.getenv("DATABASE_URL"),
      use_jsonb=True,
    )

    results = store.similarity_search_with_score(question, k=10)

    return "\n\n".join(doc.page_content.strip() for doc, score in results)