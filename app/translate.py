import requests
import uuid
from flask import current_app
from flask_babel import _

def translate(text, source_language, dest_language):
    if 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY' not in current_app.config or \
            not current_app.config['TRANSLATOR_TEXT_SUBSCRIPTION_KEY']:
        return _('Error: the translation service is not configured.')
    key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
    if not key_var_name in current_app.config:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = current_app.config[key_var_name]

    endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
    if not endpoint_var_name in current_app.config:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = current_app.config[endpoint_var_name]

    # If you encounter any issues with the base_url or path, make sure
    # that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
    path = '/translate?api-version=3.0'
    params = f"&from={source_language}&to={dest_language}"
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    translation = response[0]['translations'][0]['text'] # unpacking translated text from the response

    if request.status_code != 200:
        return _('Error: the translation service failed.')
    return translation

# def translate(text, source_language, dest_language):
#     if 'MS_TRANSLATOR_KEY' not in current_app.config or \
#             not current_app.config['MS_TRANSLATOR_KEY']:
#         return _('Error: the translation service is not configured.')
#     auth = {
#         'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
#     r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
#                      '/Translate?text={}&from={}&to={}'.format(
#                          text, source_language, dest_language),
#                      headers=auth)
#     if r.status_code != 200:
#         return _('Error: the translation service failed.')
#     return json.loads(r.content.decode('utf-8-sig'))
