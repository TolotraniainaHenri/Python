from assistant import ChatBot
from memory import load_memory
from memory import save_memory
from utils.helpers import header

header()

memory = load_memory()

bot = ChatBot(memory)

while True:

    question = input("\nVous : ")
    #if(question.__contains__("prix")):
    question += ", Je suis un client qui veut acheter une chaussure "
    if question.lower() in ["quit", "exit"]:

        save_memory(bot.get_memory())

        print("Au revoir !")

        break

    try:

        response = bot.ask(question)

        print("\nIA :", response)

        save_memory(bot.get_memory())

    except Exception as e:

        print("\nErreur :", e)
