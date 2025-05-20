
import random
from datetime import datetime

bible_verses = [
    "John 8:32 – Then you will know the truth, and the truth will set you free.",
    "Jeremiah 29:11 – 'For I know the plans I have for you,' declares the Lord...",
    "Psalm 23:1 – The Lord is my shepherd, I shall not want.",
    "Romans 8:28 – All things work together for good for those who love God.",
    "Proverbs 3:5 – Trust in the Lord with all your heart and lean not on your own understanding.",
    "Matthew 11:28 – Come to me, all who are weary and burdened, and I will give you rest.",
    "Isaiah 41:10 – Do not fear, for I am with you; do not be dismayed, for I am your God.",
]

def write_entry():
    entry = input("Write your journal entry:\n")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("journal.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}]\n{entry}\n---\n")
    print("✅ Entry saved successfully!\n")

def read_entries():
    try:
        with open("journal.txt", "r", encoding="utf-8") as file:
            content = file.read()
            print("\n📚 Your Journal Entries:\n")
            print(content)
    except FileNotFoundError:
        print("❌ No entries found yet. Start writing your first one!")

def search_entries():
    keyword = input("🔍 Enter a keyword or date (YYYY-MM-DD) to search: ").strip().lower()
    try:
        with open("journal.txt", "r", encoding="utf-8") as file:
            content = file.read()
            entries = content.split("---\n")
            results = [entry for entry in entries if keyword in entry.lower()]
            if results:
                print(f"\n✅ Found {len(results)} matching entry(ies):\n")
                for result in results:
                    print(result + "---\n")
            else:
                print("❌ No matching entries found.")
    except FileNotFoundError:
        print("❌ No journal file found.")

def main():
    print("=" * 60)
    print("📖 Joseph's Journal".center(60))
    print("A Light for the Lost. A Guide for the Chosen.".center(60))
    print("Write your thoughts, prayers, dreams, and victories.".center(60))
    print("=" * 60)

    verse = random.choice(bible_verses)
    print("📘 Bible Verse of the Day:")
    print(verse)

    while True:
        print("\nMenu:")
        print("1. Write a new entry")
        print("2. Read all entries")
        print("3. Search entries")
        print("4. Exit")

        choice = input("Choose an option (1/2/3/4): ")

        if choice == '1':
            write_entry()
        elif choice == '2':
            read_entries()
        elif choice == '3':
            search_entries()
        elif choice == '4':
            print("👋 Goodbye, Joseph! Keep writing!")
            break
        else:
            print("⚠️ Invalid option. Try again.\n")

# Run the app
main()
