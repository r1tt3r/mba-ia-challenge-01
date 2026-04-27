from search import search_prompt

def main():
    print("Chat started. Type 'exit' to quit.\n")
    while True:
        question = input("Question: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        search_prompt(question)

if __name__ == "__main__":
    main()