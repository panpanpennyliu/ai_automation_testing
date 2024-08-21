import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
import google.generativeai as genai


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


if __name__ == '__main__':

    genai.configure(api_key='AIzaSyCrPehxyHvd-KVBdGGBsKYGihfvY9kJzV0')
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("The opposite of hot is")
    to_markdown(response.text)
