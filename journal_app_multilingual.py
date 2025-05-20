
import random
from datetime import datetime
from reportlab.pdfgen import canvas

bible_verses = [
    "John 8:32 – Then you will know the truth, and the truth will set you free.",
    "Jeremiah 29:11 – 'For I know the plans I have for you,' declares the Lord...",
    "Psalm 23:1 – The Lord is my shepherd, I shall not want.",
    "Romans 8:28 – All things work together for good for those who love God.",
    "Proverbs 3:5 – Trust in the Lord with all your heart and lean not on your own understanding.",
    "Matthew 11:28 – Come to me, all who are weary and burdened, and I will give you rest.",
    "Isaiah 41:10 – Do not fear, for I am with you; do not be dismayed, for I am your God.",
]

def choose_language():
    print("🌍 Select Your Language:")
    print("1. English")
    print("2. Français")
    print("3. Kiswahili")
    choice = input("Choose (1/2/3): ")
    if choice == '2':
        return "fr"
    elif choice == '3':
        return "sw"
    else:
        return "en"

def write_entry(messages):
    entry = input(messages['write_prompt'])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("journal.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\n{entry}\n---\n")
    print(messages['entry_saved'])

def read_entries(messages):
    try:
        with open("journal.txt", "r", encoding="utf-8") as file:
            content = file.read()
            print(messages['your_entries'])
            print(content)
    except FileNotFoundError:
        print(messages['no_entries'])

def search_entries(messages):
    keyword = input(messages['search_prompt']).strip().lower()
    try:
        with open("journal.txt", "r", encoding="utf-8") as file:
            content = file.read()
            entries = content.split("---\n")
            results = [entry for entry in entries if keyword in entry.lower()]
            if results:
                print(f"\n{messages['found_entries']} {len(results)}:\n")
                for result in results:
                    print(result + "---\n")
            else:
                print(messages['no_match'])
    except FileNotFoundError:
        print(messages['no_entries'])

def export_to_pdf(messages):
    try:
        with open("journal.txt", "r", encoding="utf-8") as file:
            content = file.read()

        pdf_file = "journal_export.pdf"
        c = canvas.Canvas(pdf_file)
        c.setFont("Helvetica", 12)

        lines = content.split('\n')
        y = 800

        for line in lines:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 800
            c.drawString(50, y, line)
            y -= 18

        c.save()
        print(messages['pdf_exported'])
    except FileNotFoundError:
        print(messages['no_entries'])

def main():
    language = choose_language()

    translations = {
        "en": {
            "title": "Joseph's Journal",
            "slogan": "A Light for the Lost. A Guide for the Chosen.",
            "subtitle": "Write your thoughts, prayers, dreams, and victories.",
            "write_prompt": "Write your journal entry:\n",
            "entry_saved": "✅ Entry saved successfully!",
            "your_entries": "\n📚 Your Journal Entries:\n",
            "no_entries": "❌ No journal entries found.",
            "search_prompt": "🔍 Enter keyword or date (YYYY-MM-DD): ",
            "found_entries": "✅ Found entries:",
            "no_match": "❌ No matching entries found.",
            "pdf_exported": "✅ Journal exported to journal_export.pdf",
            "menu": ["Write a new entry", "Read all entries", "Search entries", "Export journal to PDF", "Exit"],
            "goodbye": "👋 Goodbye! Keep writing!"
        },
        "fr": {
            "title": "Journal de Joseph",
            "slogan": "Une lumière pour les perdus. Un guide pour les élus.",
            "subtitle": "Écrivez vos pensées, prières, rêves et victoires.",
            "write_prompt": "Écrivez votre entrée de journal :\n",
            "entry_saved": "✅ Entrée enregistrée avec succès !",
            "your_entries": "\n📚 Vos entrées de journal :\n",
            "no_entries": "❌ Aucune entrée trouvée.",
            "search_prompt": "🔍 Entrez un mot-clé ou une date (AAAA-MM-JJ) : ",
            "found_entries": "✅ Entrées trouvées :",
            "no_match": "❌ Aucune entrée correspondante trouvée.",
            "pdf_exported": "✅ Journal exporté vers journal_export.pdf",
            "menu": ["Écrire une nouvelle entrée", "Lire toutes les entrées", "Rechercher des entrées", "Exporter le journal en PDF", "Quitter"],
            "goodbye": "👋 Au revoir ! Continuez à écrire !"
        },
        "sw": {
            "title": "Shajara ya Joseph",
            "slogan": "Nuru kwa waliopotea. Mwongozo kwa wateule.",
            "subtitle": "Andika mawazo yako, sala, ndoto, na ushindi.",
            "write_prompt": "Andika andiko lako la shajara:\n",
            "entry_saved": "✅ Umefanikiwa kuhifadhi andiko lako!",
            "your_entries": "\n📚 Maandiko yako ya shajara:\n",
            "no_entries": "❌ Hakuna maandiko yaliyopatikana.",
            "search_prompt": "🔍 Andika neno kuu au tarehe (YYYY-MM-DD): ",
            "found_entries": "✅ Maandiko yaliyopatikana:",
            "no_match": "❌ Hakuna maandiko yaliyolingana.",
            "pdf_exported": "✅ Shajara imehifadhiwa kama journal_export.pdf",
            "menu": ["Andika andiko jipya", "Soma maandiko yote", "Tafuta maandiko", "Hamisha shajara hadi PDF", "Toka"],
            "goodbye": "👋 Kwaheri! Endelea kuandika!"
        }
    }

    messages = translations[language]

    print("=" * 60)
    print(f"📖 {messages['title']}".center(60))
    print(messages["slogan"].center(60))
    print(messages["subtitle"].center(60))
    print("=" * 60)

    verse = random.choice(bible_verses)
    print("📘 Bible Verse of the Day:")
    print(verse)

    while True:
        print("\nMenu:")
        for i, item in enumerate(messages["menu"], 1):
            print(f"{i}. {item}")
        choice = input("Choose an option (1/2/3/4/5): ")

        if choice == '1':
            write_entry(messages)
        elif choice == '2':
            read_entries(messages)
        elif choice == '3':
            search_entries(messages)
        elif choice == '4':
            export_to_pdf(messages)
        elif choice == '5':
            print(messages["goodbye"])
            break
        else:
            print("⚠️ Invalid option. Try again.\n")

# Run the app
main()
