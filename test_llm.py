from llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Explain what an industrial CNC machine is in one sentence."
)

print(response.content)