import json
from openai import OpenAI
import os
from time import time
import sqlite3


print("Running db_bot_interactions.py")

currDir =  os.path.dirname(__file__)


def getPath(fileName):
  return os.path.join(currDir, fileName)


sqlliteDbPath = getPath("aidb.sqlite")
setupSqlDbPath = getPath("songs_database.sql")
setupSqlDbRowsPath = getPath("songs_db_rows.sql")


if os.path.exists(sqlliteDbPath):
  os.remove(sqlliteDbPath)


sqlliteCon = sqlite3.connect(sqlliteDbPath)
sqlliteCursor = sqlliteCon.cursor()


with (
        open(setupSqlDbPath) as setupDbFile,
        open(setupSqlDbRowsPath) as setupDbRowsFile
        ):
  setupSqlDbScript = setupDbFile.read()
  setupDbRowsScript = setupDbRowsFile.read()

sqlliteCursor.executescript(setupSqlDbScript)
sqlliteCursor.executescript(setupDbRowsScript)

def runSql(query):
  result = sqlliteCursor.execute(query).fetchall()
  return result


configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
  config = json.load(configFile)

openAiClient = OpenAI(api_key = config["openaiKey"])
openAiClient.models.list()
chosenModel = "gpt-4o"


def getChatGptResponse(content):
  stream = openAiClient.chat.completions.create(
    model=chosenModel,
    messages=[{"role": "user", "content": content}],
    stream=True,
  )


  responseList = []
  for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      responseList.append(chunk.choices[0].delta.content)

  result = "".join(responseList)
  return result


commonSqlOnlyRequest = "Give me a sqlite statement that answers my question. Only respond with sqlite syntax. If there is an error, do not explain it or comment on it."
strategies = {
  "zero-shot": setupSqlDbScript + commonSqlOnlyRequest,
  "single_domain_double_shot": (setupSqlDbScript+
                                "Which artists are never features on songs from other artists?"+
                                " \nSELECT a.artistName\nFROM Artist INNER JOIN ArtistSong as ON a.artistId = as.artistId\n;"+
                                commonSqlOnlyRequest)
}

questions = [
  "Which artist features the most songs that are not their own?",
  "What different genres of songs are there?",
  "How many songs is Graham Coxon on, including his work with Blur?",
  "What are the two most popular songs?",
  "Which album has the most total plays?",
  "Which artist wrote 'Mirror Ball'?",
  "Which artists do not feature on any other artist's songs?"
]


def sanitizeForJustSql(value):
  gptStartSqlMarker = "```"
  gptEndSqlMarker = "```"
  if gptStartSqlMarker in value:
    value = value.split(gptStartSqlMarker, 1)[1]
    newlineIndex = value.find("\n")
    if newlineIndex != -1:
      value = value[newlineIndex+1:]
  if gptEndSqlMarker in value:
    value = value.split(gptEndSqlMarker, 1)[0]
  
  return value.strip()


for strategy in strategies:
  responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
  questionResults = []
  print("########################################################################")
  print(f"Running strategy: {strategy}")
  for question in questions:

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Question:")
    print(question)
    error = "None"

    try:
      getSqlfromQuestionEngineeredPrompt = strategies[strategy] + " " + question
      sqlSyntaxResponse = getChatGptResponse(getSqlfromQuestionEngineeredPrompt)
      sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
      print("SQL Syntax Response:")
      print(sqlSyntaxResponse)
      queryRawResponse = str(runSql(sqlSyntaxResponse))
      print("Query Raw Response:")
      print(queryRawResponse)

      friendlyResultsPrompt = "I asked this question: \""+question+ "\"from this database: \""+setupSqlDbScript+"\"and got this response: \""+queryRawResponse+"\"Please tell me this data in everyday speech. Don't give any suggestions or follow-up chatter."
      friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
      print("Friendly Response:")
      print(friendlyResponse)


    except Exception as err:
      error = str(err)
      print(err)

    questionResults.append({
      "question": question,
      "sql": sqlSyntaxResponse,
      "queryRawResponse": queryRawResponse,
      "friendlyResponse": friendlyResponse,
      "error": error
    })

  responses["questionResults"] = questionResults

  with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
    json.dump(responses, outFile, indent=2)




sqlliteCursor.close()
sqlliteCon.close()
print("Done!")
  
