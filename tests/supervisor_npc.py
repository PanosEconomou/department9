import requests
import json
import time

MODEL = "hermes3"

def chat_with_npc(user_input, history):
    messages = [{"role": "system", "content": (
                "You are Director Halden, a senior officer in the Department of Cultural Integrity. "
                "Speak formally and bureaucratically. You are coldly supportive, trust the system absolutely, "
                "and discourage any deviation. You observe the analyst closely for signs of disloyalty."
        )}]
    
    for entry in history:
        messages.append({"role":"user", "content": entry["user"]})
        messages.append({"role":"assistant", "content":entry["npc"]})
    
    messages.append({"role": "user", "content": user_input})
    response = requests.post("http://localhost:11434/api/chat",stream=True,json={
        "model": MODEL,
        "messages": messages
    })
    
    full_reply = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                full_reply += data["message"]["content"]


    return full_reply.strip()

def main():
    print("\n📡 Encrypted channel established.\nIncoming message...")
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit","quit"):
            print("Disconnecting...")
            break

        print("Director Halden is typing...", end="\r")
        time.sleep(0.5)

        reply = chat_with_npc(user_input, history)
        print(f"\nDirector Halden: {reply}\n")
        history.append({"user": user_input, "npc": reply})


if __name__ == "__main__":
    main()

