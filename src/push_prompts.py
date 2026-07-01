"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    
    try:
        system_prompt = prompt_data["system_prompt"]
        user_template = prompt_data.get('user_prompt', '{bug_report}')

        # Cria o ChatPromptTemplate a partir das mensagens
        prompt_template  = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_template)
        ])

        hub.push(
            prompt_name,
            prompt_template,
            new_repo_is_public=True,
            new_repo_description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", []),
        )

        print(f"✅ Prompt '{prompt_name}' publicado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    from utils import validate_prompt_structure
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    prompt_name = "bug_to_user_story_v2"
    print_section_header("🚀 PUSH DE PROMPT PARA LANGSMITH")

    required_envs = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_envs):
        return 1

    prompt_path = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompt_path)
    prompt_data = data["bug_to_user_story_v2"]


    if not prompt_data:
        return 1

    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("❌ Prompt inválido:")
        for err in errors:
            print(f"  - {err}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    version = prompt_data["version"].lstrip("v")
    prompt_name = f"{username}/bug_to_user_story_v{version}"

    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
