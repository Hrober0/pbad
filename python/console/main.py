from dotenv import load_dotenv

from interface import Repl
from llm import Chat

if __name__ == "__main__":
    load_dotenv()
    Repl(Chat()).run()
