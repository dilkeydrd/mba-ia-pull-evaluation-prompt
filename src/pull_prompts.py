"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_ID = "dilean/bug_to_user_story_v1"
OUTPUT_PATH = Path("prompts/raw_prompt.yml")

def pull_prompts_from_langsmith():
    
    """Faz pull do prompt no LangSmith Hub e retorna serialização"""
    print_section_header("Pull de Prompts do LangSmith Hub")

    #Valida se a variável de ambiente LANGSMITH_API_KEY está definida
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return None

    #Pull do prompt do LangSmith Hub
    prompt = hub.pull(PROMPT_ID)

    #serialize prompt to dict
    serialized_prompt = prompt.model_dump()

    return {
        "id": PROMPT_ID,
        "prompt": serialized_prompt,
    }


def main():
    """Função principal"""
    data = pull_prompts_from_langsmith()

    if data is None:
        print("\n❌ Falha ao obter prompt. Verifique as variáveis de ambiente.")
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    save_yaml(data, OUTPUT_PATH)

    print(f"\n✅ Prompt salvo com sucesso em: {OUTPUT_PATH}")
    return 0

if __name__ == "__main__":
    sys.exit(main())