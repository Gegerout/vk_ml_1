from TDocument import TDocument


class DocumentProcessor:
    def __init__(self):
        self.documents = {}

    def process(self, doc):
        url = doc.Url
        if url not in self.documents:
            self.documents[url] = {
                "Text": doc.Text,
                "FetchTime": doc.FetchTime,
                "PubDate": doc.PubDate,
                "FirstFetchTime": doc.FetchTime
            }
        else:
            current = self.documents[url]
            if doc.FetchTime > current["FetchTime"]:
                current["Text"] = doc.Text
                current["FetchTime"] = doc.FetchTime
            if doc.FetchTime < current["FirstFetchTime"]:
                current["FirstFetchTime"] = doc.FetchTime
            if doc.FetchTime < current["FetchTime"]:
                current["PubDate"] = doc.PubDate

        return TDocument(
            Url=url,
            Text=self.documents[url]["Text"],
            FetchTime=self.documents[url]["FetchTime"],
            PubDate=self.documents[url]["PubDate"],
            FirstFetchTime=self.documents[url]["FirstFetchTime"]
        )