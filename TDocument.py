import json

class TDocument:
    def __init__(self, Url, PubDate, FetchTime, Text, FirstFetchTime=None):
        self.Url = Url
        self.PubDate = PubDate
        self.FetchTime = FetchTime
        self.Text = Text
        self.FirstFetchTime = FirstFetchTime

    @staticmethod
    def from_json(json_str):
        try:
            data = json.loads(json_str)
            return TDocument(**data)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Failed to parse document: {e}")
            return None

    def to_json(self):
        return json.dumps(self.__dict__)
