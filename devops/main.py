from agent import agent

while True:

    question = input("\nAsk DevOps Agent > ")

    if question.lower() in ["quit", "exit"]:
        break

    response = agent.invoke(
        {
            "messages": [
                ("user", question)
            ]
        }
    )

    print("\n")
    print(response["messages"][-1].content)