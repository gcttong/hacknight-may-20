import os
import getpass
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
from opik.integrations.openai import track_openai
from openai import OpenAI
import opik

# Configure opik
opik.configure(use_local=False, api_key="Nq7plNyXUMKOVW9lx2mZHeXjK")

friendli_token = "flp_MA1lWPi6HjsUjMAisotnAy43vrmTilnbpIyETyGjALAc6"


# Set up Friendli token if not present
if not os.environ.get("FRIENDLI_TOKEN"):
    os.environ["FRIENDLI_TOKEN"] = friendli_token

# Set project name
os.environ["OPIK_PROJECT_NAME"] = "gary-abraham-footballers-rag"

# Weaviate configuration
WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL') or 'pbnlhdtt1yaa2rug3p1a.c0.us-west3.gcp.weaviate.cloud'
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY') or 'CKg9JA2BEmS1uWkGCW5MUCJehBlVM4JNptfi' # This is a read key

weaviate_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_CLUSTER_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    headers={"X-Friendli-Token": os.getenv('FRIENDLI_TOKEN')},
)

print(weaviate_client.is_connected())

book_collection = weaviate_client.collections.get(name="Football")

friendli_client = OpenAI(
    base_url="https://api.friendli.ai/serverless/v1",
    api_key=os.getenv('FRIENDLI_TOKEN')
)

@opik.track
def call_llm(client, messages):
    response = friendli_client.chat.completions.create(
      model="meta-llama-3.3-70b-instruct",
      messages=messages
    )
    return response

user_query = input("What would you like to query for in the Footballers dataset? ")

response = book_collection.query.near_text(
        query=user_query,
        limit=3
    )

@opik.track
def retrieve_context(user_query):
    # Semantic Search
    response = book_collection.query.near_text(
        query=user_query,
        limit=3
    )

    footballers = []
    for book in response.objects:
        footballers.append(book.properties['name'])
    return footballers

@opik.track
def generate_response(user_query, footballers):
  prompt = f"""
  You're a helpful assistant, reply to a chatbot message for someone inquiring for
  footballers. The user query was {user_query}


  These were the footballers that were extracted from the vector
  search:

  {footballers}
  """

  messages=[
      {
          "role": "user",
          "content": prompt
      }
  ]
  response = call_llm(friendli_client, messages)


  return (response.choices[0].message.content)

@opik.track(name="rag-example")
def llm_chain(user_query):
    context = retrieve_context(user_query)
    response = generate_response(user_query, context)
    return response

# Use the LLM chain
user_query = input("What types of footballers are you looking for? ")
result = llm_chain(user_query)
print(result)