import logging
from openai import AzureOpenAI, AuthenticationError, RateLimitError, APIConnectionError, BadRequestError

from app.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
)


def call_claude(
    messages: list[dict],
    system_prompt: str,
    max_tokens: int = 1000,
) -> str:
    logger.info(
        "Llamando a Azure OpenAI | deployment=%s | mensajes=%d | max_tokens=%d",
        AZURE_OPENAI_DEPLOYMENT, len(messages), max_tokens,
    )

    full_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in messages
    ]

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=full_messages,
            max_tokens=max_tokens,
        )
        text = response.choices[0].message.content
        logger.info(
            "Respuesta recibida | tokens_usados=%d",
            response.usage.completion_tokens,
        )
        return text

    except AuthenticationError:
        logger.error("Error de autenticación: API Key o endpoint inválido.")
        raise ValueError("La clave o el endpoint de Azure OpenAI son inválidos o han expirado.")

    except RateLimitError:
        logger.error("Límite de tasa alcanzado.")
        raise ValueError("Se alcanzó el límite de solicitudes. Intenta de nuevo en unos segundos.")

    except APIConnectionError:
        logger.error("No se pudo conectar con Azure OpenAI.")
        raise ValueError("No se pudo conectar con el servicio de IA. Verifica tu conexión a internet.")

    except BadRequestError as e:
        logger.error("Solicitud inválida: %s", str(e))
        raise ValueError(f"Solicitud inválida: {str(e)}")

    except Exception as e:
        logger.error("Error inesperado al llamar a Azure OpenAI: %s", str(e))
        raise ValueError(f"Ocurrió un error inesperado al procesar tu solicitud: {str(e)}")
