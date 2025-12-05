def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    prices = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4.1": {"input": 0.01, "output": 0.03},
        "gpt-4.1-mini": {"input": 0.0005, "output": 0.0015},
        "gpt-5": {"input": 0.015, "output": 0.045},
    }

    input_rate = prices[model_name]["input"]
    output_rate = prices[model_name]["output"]

    cost = (input_tokens / 1000) * input_rate + \
           (output_tokens / 1000) * output_rate
    return round(cost, 6)
