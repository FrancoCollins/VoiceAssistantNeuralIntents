import requests
from bs4 import BeautifulSoup


def search(self, query: str, language: str) -> str:
    """Search the query with different websites (Wikipedia, etc).
    :param self: assistant who gets the query info
    :param language: is the response query and response language
    :param query: query to search"""
    try:
        first_url = f"https://{language}.wikipedia.org/wiki/{query}"
        request = requests.get(first_url)
        soup = BeautifulSoup(request.text, "html.parser")
        content = soup.find("div", attrs={"class": "mw-parser-output"})

        while content.find("p") is None:
            content = content.find_next("div", attrs={"class": "mw-parser-output"})

        paragraphs = content.find_all("p")[:2]

        text = ""

        for i in range(len(paragraphs)):
            text += paragraphs[i].text + "\n"

        if text is not None and text.strip() != "":

            # Strip brackets
            while text.find("[") != -1:
                text = text.replace(text[text.find("["):text.find("]") + 1], "")

            print(text)
            self.auto_learn(query, ["what is " + query, "tell me definition of " + query, "tell me about " + query,
                                    "explain " + query + " to me", "search " + query, "google " + query,
                                    "search in internet " + query], text)
            return text

        else:
            return "Parsing Error"

    except Exception as e:
        print("Wikipedia definition not found.")
        print(e.with_traceback())
        return "Definition not found."

# TODO: Search somewhere else
