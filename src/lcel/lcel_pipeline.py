from src.service.lcel_chain import build_chain
from src.service.lcel_model import get_llm
from src.prompts.lcel_prompt import get_ipl_prompt
from src.service.cost import calculate_cost

def main():
    chain = build_chain()

    # Run pipeline
    response_text = chain.invoke({})
    print("Response:", response_text)

    # Token usage (from model)
    llm = get_llm()
    raw_output = llm.invoke(get_ipl_prompt().format_messages())
    input_tokens = raw_output.usage_metadata["input_tokens"]
    output_tokens = raw_output.usage_metadata["output_tokens"]

    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")

    cost = calculate_cost("gpt-4.1-mini", input_tokens, output_tokens)
    print(f"Estimated cost: ${cost}")

if __name__ == "__main__":
    main()
