from datetime import datetime
import yaml
import os


def export_conversation(agent_name, conversation_name=None):
    if conversation_name:
        history_file = os.path.join(
            "conversations", agent_name, f"{conversation_name}.yaml"
        )
    else:
        history_file = os.path.join("agents", agent_name, "history.yaml")
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = yaml.safe_load(file)
        return history
    return {"interactions": []}


def get_conversation(agent_name, conversation_name=None, limit=100, page=1):
    if conversation_name:
        history_file = os.path.join(
            "conversations", agent_name, f"{conversation_name}.yaml"
        )
    else:
        history_file = os.path.join("agents", agent_name, "history.yaml")
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            history = yaml.safe_load(file)
        # Limit the number of interactions returned
        history["interactions"] = history["interactions"][
            (page - 1) * limit : page * limit
        ]

        return history
    return {"interactions": []}


def new_conversation(agent_name, conversation_name):
    history = {"interactions": []}
    history_file = os.path.join(
        "conversations", agent_name, f"{conversation_name}.yaml"
    )
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w") as file:
        yaml.safe_dump(history, file)


def log_interaction(role: str, message: str, agent_name: str, conversation_name: str):
    history = get_conversation(
        agent_name=agent_name, conversation_name=conversation_name
    )
    if history is None:
        history = {"interactions": []}
    history_file = os.path.join(
        "conversations", agent_name, f"{conversation_name}.yaml"
    )
    os.makedirs(os.path.dirname(history_file), exist_ok=True)

    history["interactions"].append(
        {
            "role": role,
            "message": message,
            "timestamp": datetime.now().strftime("%B %d, %Y %I:%M %p"),
        }
    )
    with open(history_file, "w") as file:
        yaml.safe_dump(history, file)


def delete_history(agent_name, conversation_name=None):
    history = {"interactions": []}
    if conversation_name:
        history_file = os.path.join(
            "conversations", agent_name, f"{conversation_name}.yaml"
        )
    else:
        history_file = os.path.join("agents", agent_name, "history.yaml")
    with open(history_file, "w") as file:
        yaml.safe_dump(history, file)


def delete_message(agent_name, message, conversation_name=None):
    history = get_conversation(
        agent_name=agent_name, conversation_name=conversation_name
    )
    history["interactions"] = [
        interaction
        for interaction in history["interactions"]
        if interaction["message"] != message
    ]
    if not conversation_name:
        conversation_name = "history"
    history_file = os.path.join(
        "conversations", agent_name, f"{conversation_name}.yaml"
    )
    with open(history_file, "w") as file:
        yaml.safe_dump(history, file)
