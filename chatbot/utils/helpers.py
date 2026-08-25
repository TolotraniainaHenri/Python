from datetime import datetime


def header():

    print("=" * 60)
    print("        CHATBOT IA")
    print("=" * 60)


def now():

    return datetime.now().strftime("%d/%m/%Y %H:%M")
