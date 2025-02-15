from enum import Enum


class LLMOptions(str, Enum):
    o1_mini = "o1-mini"
    deepseek = "deepseek-r1-distill-llama-70b-specdec"
    llama_instant = "llama-3.1-8b-instant"
    llama_70b = "llama-3.3-70b-versatile"
