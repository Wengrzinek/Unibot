import sparql
from programy.utils.logging.ylogger import YLogger
from programy.services.service import Service


class DBpediaAPI:
    service = sparql.Service("https://dbpedia.org/", "utf-8", "GET")


class DBpediaService(Service):

    def __init__(self, config=None, api=None):
        Service.__init__(self, config)

        if api is None:
            self._api = DBpediaAPI()
        else:
            self._api = api

    def ask_question(self, client_context, question: str):
        try:
            words = question.split()
            question = " ".join(words[1:])
            statement = 'SELECT' + 'DISTINCT ?' + 'location' + ' WHERE { ?' + 'location' + 'dbo:birthPlace' + 'dbr:Albert_Einstein' + '}'#TODO
            search = self._api.service.query(statement)
            result = ""
            for row in search:
               result = result + row
            else:
                YLogger.error(client_context, "Unknown DBpedia command [%s]", words[0])
                result = ""
            return result
        except Exception:
            YLogger.error(client_context, "General error querying DBpedia for question [%s]", question)
        return ""