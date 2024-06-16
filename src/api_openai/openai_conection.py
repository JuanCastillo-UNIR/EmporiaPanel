from openai import OpenAI
import json, os, pypandoc


def get_completion(_openai_client, prompt: str, user_msg: str):
    args = {
        "messages": [{"role": "system", "content": prompt['system_message']}]
        + [{"role": "user", "content": user_msg if user_msg is not None else ""}],
        "model": prompt['deployment_name'],
        "temperature": prompt['temperature'],
        "max_tokens": prompt['max_response_length'],
        "top_p": prompt['top_p'],
        "frequency_penalty": prompt['frequency_penalty'],
        "presence_penalty": prompt['presence_penalty'],
        "stop": prompt['stop_sequences'],
        "stream": prompt['stream']
    }
    return _openai_client.chat.completions.create(**args)  # type: ignore

def call_api(user_msg, prompt_name='prompt'):
    _openai_client = OpenAI(api_key=os.getenv('OPEN_AI__API_KEY'))
    path = os.path.join(
                os.sep.join(__file__.split(os.sep)[:-1]),
                f"{prompt_name}.json",
    )
    with open(path, encoding="utf-8") as json_file:
        prompt_json = json.load(json_file)
    response = get_completion(_openai_client, prompt_json, str(user_msg))
    html_content = pypandoc.convert_text(
        response.choices[0].message.content,
        'html',
        format='md',
        extra_args=['-V', 'mainfont="Arial"', '--css=styles.css']
    )
    return html_content