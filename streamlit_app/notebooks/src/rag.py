"""RAG helper copied from the workspace.
"""

from operator import itemgetter
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

try:
    from pdf_ingestion import PdfIngestion
except ModuleNotFoundError:  # pragma: no cover
    from notebooks.src.pdf_ingestion import PdfIngestion

DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "pdf_files"

PROMPT = ChatPromptTemplate.from_template(
    """
You are a technical assistant for our data analytics team.
Answer the question below focusing on the context below.
If there is no answer in the context, just say: "there is no answer"


QUESTION:
{question}


CONTEXT:
{context}


ANSWER:
Be precise and very concise.
"""
)


def _format_docs(docs: list[Document]) -> str:
    return "\n\n".join(
        f"[page {d.metadata.get('page', '?')}] {d.page_content}" for d in docs
    )


def load_chunks(pdf_path: str | None = None):
    ingestor = PdfIngestion(chunk_size=1200, chunk_overlap=180)

    if pdf_path is not None:
        pdfs = [Path(pdf_path)]
    else:
        pdfs = sorted(DATA_DIR.glob("*.pdf"))

    if not pdfs:
        raise FileNotFoundError(f"No PDF found in {DATA_DIR}")

    chunks = []
    for pdf in pdfs:
        chunks.extend(ingestor.process(str(pdf)))
    return chunks


def build_retriever(pdf_path: str | None = None, k: int = 3):
    chunks = load_chunks(pdf_path)
    embed = OpenAIEmbeddings(model="text-embedding-3-small")
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embed,
        collection_name="capstone_focused_docs",
    )
    return store.as_retriever(search_kwargs={"k": k})


def build_chain(retriever, model: str = "gpt-4o-mini"):
    llm = ChatOpenAI(model=model)
    parser = StrOutputParser()

    return (
        {
            "context": lambda x: _format_docs(retriever.invoke(x["question"])),
            "question": lambda x: x["question"],
        }
        | PROMPT
        | llm
        | parser
    )


def build_rag(pdf_path: str | None = None, k: int = 3, model: str = "gpt-4o-mini"):
    retriever = build_retriever(pdf_path=pdf_path, k=k)
    return build_chain(retriever, model=model)


# Conversational/Memory functions omitted for brevity; they mirror workspace's rag.py
