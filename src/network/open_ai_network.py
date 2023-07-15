import os
import logging
import requests
from src import error, dto


async def send_chat_completion_request(request: dto.ChatRequest) -> dto.ChatResponse:
    url = '{}/{}'.format(os.environ.get('OPENAI_BASE_URL'), 'chat/completions')

    logging.info('OpenAI request body: {}'.format(request))

    response = requests.post(url, auth=dto.BearerAPIKeyAuth(os.environ.get('OPENAI_API_KEY')), json=request.__dict__)

    if response.status_code == 200:
        return dto.ChatResponse.from_json_dict(response.json())
    elif response.status_code == 429:
        raise error.TokenQuotaReachedError
    else:
        raise error.UnexpectedNetworkError
