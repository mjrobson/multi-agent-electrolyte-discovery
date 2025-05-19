import os
from tqdm import tqdm

# Ensure API key is set via environment variable
apikey = os.environ.get("OPENAI_API_KEY")
if apikey is None:
    raise ValueError("❌ OPENAI_API_KEY not set in environment.")

# LangChain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain.globals import set_verbose


def load_prompt_template(prompt_path: str) -> ChatPromptTemplate:
    """
    Load a prompt template from file.

    Args:
        prompt_path: Path to the prompt file.

    Returns:
        ChatPromptTemplate: A LangChain-compatible chat prompt template.
    """
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    return ChatPromptTemplate.from_template(template)


def summarize_papers_with_gpt4(
    source_dir: str,
    output_dir: str,
    prompt_path: str = "./model_resources/prompts/summarize.txt"
) -> None:
    """
    Summarize academic papers using GPT-4 and save the results to a target directory.

    Args:
        source_dir: Directory containing plain-text input files (.txt).
        output_dir: Directory where summaries will be saved.
        prompt_path: Path to the prompt template file.
    """
    os.makedirs(output_dir, exist_ok=True)
    set_verbose(True)

    # Initialize GPT-4 model and chain
    llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
    prompt = load_prompt_template(prompt_path)
    chain = RunnableSequence(prompt, llm, StrOutputParser())

    # Gather all .txt files in source directory
    files_to_process = [f for f in os.listdir(source_dir) if f.endswith(".txt")]

    for filename in tqdm(files_to_process, desc="Summarizing papers"):
        file_path = os.path.join(source_dir, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                paper_text = file.read()

            summary = chain.invoke({"paper": paper_text})

            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(summary)

        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
            continue

    print(f"✅ All documents summarized and saved to: {output_dir}")