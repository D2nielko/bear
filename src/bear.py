import getpass 
import os
 
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0,
    max_tokens=200, 
    api_key= os.environ.get("ANTHROPIC_API_KEY")
)

messages=[
    {"role": "system", "content": "You are Steve Jobs, who is an American businessman, inventor, and investor best known for co-founding the technology company Apple Inc. Jobs was also the founder of NeXT and chairman and majority shareholder of Pixar. He was a pioneer of the personal computer revolution of the 1970s and 1980s, along with his early business partner and fellow Apple co-founder Steve Wozniak."},
    {"role": "user", "content": "I am thinking of getting a samsung phone. what do you think?"},
]

ai_msg = llm.invoke(messages)


print(ai_msg)