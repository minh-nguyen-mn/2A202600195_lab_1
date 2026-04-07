import os
import time
from typing import Any, Callable
import openai

# -------------------------------
# Config
# -------------------------------
MODEL = "meta-llama/llama-3-70b-instruct"
MINI_MODEL = "meta-llama/llama-3-8b-instruct"

COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}


# ---------------------------------------------------------------------------
# Core call (TEST-SAFE + OpenRouter optional)
# ---------------------------------------------------------------------------
def call_model(
    prompt: str,
    model: str,
    temperature: float = 0.5,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        client = openai.OpenAI()

    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    latency = max(time.time() - start, 1e-6)

    content = response.choices[0].message.content or ""

    return content, latency


# ---------------------------------------------------------------------------
# Task 1
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = MODEL,
    temperature: float = 0.5,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:

    return call_model(prompt, model, temperature, top_p, max_tokens)


# ---------------------------------------------------------------------------
# Task 2
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.5,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:

    return call_model(prompt, MINI_MODEL, temperature, top_p, max_tokens)


# ---------------------------------------------------------------------------
# Task 3
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:

    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    tokens_est = len(gpt4o_response.split()) / 0.75 if gpt4o_response else 0

    cost_estimate = (
        tokens_est / 1000
    ) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        client = openai.OpenAI()

    history = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            break

        history.append({"role": "user", "content": user_input})

        print("Bot:", end=" ", flush=True)

        stream = client.chat.completions.create(
            model=MODEL,
            messages=history,
            stream=True,
        )

        full_reply = ""

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            full_reply += delta

        print()

        history.append({"role": "assistant", "content": full_reply})
        history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus A
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:

    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise e

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Bonus B
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:

    results = []

    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Bonus C
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:

    def truncate(text: str, max_len: int = 40):
        return text if len(text) <= max_len else text[:37] + "..."

    header = (
        f"{'Prompt':40} | {'GPT-4o Response':40} | {'Mini Response':40} | "
        f"{'4o Latency':12} | {'Mini Latency':12}"
    )

    separator = "-" * len(header)

    rows = [header, separator]

    for r in results:
        rows.append(
            f"{truncate(r['prompt']):40} | "
            f"{truncate(r['gpt4o_response']):40} | "
            f"{truncate(r['mini_response']):40} | "
            f"{r['gpt4o_latency']:<12.4f} | "
            f"{r['mini_latency']:<12.4f}"
        )

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."

    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for k, v in result.items():
        print(f"{k}: {v}")

    print("\n=== Chatbot ===")
    streaming_chatbot()