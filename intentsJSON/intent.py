class intent:
    tag: str
    patterns: [str]
    responses: [str]

    def __init__(self, tag: str, patterns: [str], responses: [str]):
        self.tag = tag
        self.patterns = patterns
        self.responses = responses
