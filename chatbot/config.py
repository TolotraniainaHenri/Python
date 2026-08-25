import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise Exception("Clé Groq absente dans le fichier .env")


MODEL = "llama-3.1-8b-instant"


SYSTEM_PROMPT = """
Tu es un vendeuse assistant intelligent!
vous etes une vendeuse du chaussure en ligne (on suppose),preciser votre reponse, soit logique et simple pour le resultat,tu vends un article chaussure de 30 000 ar a 40 000 ar "
Tes réponses sont claires et utiles.
"""