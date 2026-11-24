import json
import assistant

with open("app_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

if __name__ == "__main__":
    print(f"=== {cfg['app_name']} (v{cfg['version']}) ===")
    name = input("Apnar nam ki? ").strip() or "Friend"
    while True:
        msg = input(name + ": ").strip()
        if msg.lower() in ["exit", "quit", "bye"]:
            break
        if not msg:
            continue
        bn = any("\u0980" <= c <= "\u09ff" for c in msg)
        print("AI:", assistant.ask_ai(msg, bn))
