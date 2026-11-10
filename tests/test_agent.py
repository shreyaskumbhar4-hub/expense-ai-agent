from src.agent import run_agent


user_id = 1


while True:

    message = input("You: ")

    if message.lower() in {"exit", "quit"}:
        print("Agent: Goodbye!")
        break

    response = run_agent(
        message,
        user_id
    )

    print("Agent:", response)

