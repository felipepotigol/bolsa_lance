#teste_modelo.py

from transformers import pipeline

print("Carregando modelo...")

pipe = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct"
)

print("Modelo carregado!")

pergunta = "O que é Aprendizagem Federativa?"

resposta = pipe(
    pergunta,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7
)

print(resposta[0]["generated_text"])
