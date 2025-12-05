from langchain_core.output_parsers import StrOutputParser
from src.prompts.lcel_prompt import get_ipl_prompt
from src.service.lcel_model import get_llm

def build_chain():
    prompt = get_ipl_prompt()
    model = get_llm()
    parser = StrOutputParser()

    # LCEL pipeline
    return prompt | model | parser
