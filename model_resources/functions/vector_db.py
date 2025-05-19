"""
Vector Database Utilities
Authors: Matt Robson
Date: 12.5.2025
"""

import os
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


def create_vector_db(
    source_dir: str,
    persist_dir: str,
    split_tokens: bool = True,
    chunk_size: int = 2000,
    chunk_overlap: int = 100,
    verbose: bool = True
) -> Chroma:
    """
    Create and persist a Chroma vector database from text files in a directory.

    Args:
        source_dir: Directory containing .txt files.
        persist_dir: Directory to store the Chroma DB.
        split_tokens: Whether to split text into token-based chunks.
        chunk_size: Number of tokens per chunk (if splitting).
        chunk_overlap: Number of overlapping tokens between chunks.
        verbose: If True, prints progress updates.

    Returns:
        A Chroma vector store object with the processed documents.
    """
    if verbose:
        print(f"📂 Loading documents from: {source_dir}")

    loader = DirectoryLoader(source_dir, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if split_tokens:
        if verbose:
            print("🔀 Splitting documents using token-based chunking...")
        splitter = TokenTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        docs_chunks = splitter.split_documents(documents)
    else:
        docs_chunks = documents

    if verbose:
        print("🧠 Generating embeddings with OpenAI...")

    embeddings = OpenAIEmbeddings()

    if verbose:
        print(f"💾 Creating Chroma DB at: {persist_dir}")

    vector_db = Chroma.from_documents(
        docs_chunks,
        embeddings,
        persist_directory=persist_dir
    )
    vector_db.persist()

    if verbose:
        print(f"✅ Vector DB created and saved to: {persist_dir}")

    return vector_db


def read_text_database(
    persist_directory: str,
    embeddings=OpenAIEmbeddings(),
) -> Chroma:
    """
    Load an existing Chroma vector database from disk.

    Args:
        persist_directory: Path to the persisted Chroma directory.
        embeddings: Embedding function to use for querying (default: OpenAIEmbeddings).

    Returns:
        The loaded Chroma vector store.
    """
    paperdb = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    print(f"✅ Database loaded from {persist_directory}")
    return paperdb