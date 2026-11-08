from dotenv import load_dotenv

from interface import Repl
from llm import Chat, SqlGenerator

if __name__ == "__main__":
    load_dotenv()
    Repl(Chat(), SqlGenerator()).run()
