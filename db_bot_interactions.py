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

  # TODO: Review this portion of code
  responseList = []
  for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      responseList.append(chunk.choices[0].delta.content)

  result = "".join(responseList)
  return result


commonSqlOnlyRequest = "Give me a sqlite statement that answers my question. Only respond with sqlite syntax. If there is an error, do not explain it or comment on it."
strategies = {
  "zero-shot": setupSqlDbScript + commonSqlOnlyRequest,
  # TODO: ADD A single_domain_double_shot example later
}

questions = [
  "Which artist features the most songs that are not their own?",
  "What different genres of songs are there?",
  "How many songs is Graham Coxon on, including his work with Blur?",
  "What are the two most popular songs?",
  "Which album has the most total plays?",
  "Which artist wrote 'Mirrorball'?"
]




sqlliteCursor.close()
  
