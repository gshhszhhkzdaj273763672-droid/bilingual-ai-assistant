import os, requests

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
]

def ask_ai(text, bn):
    if not KEY or KEY == "YOUR_API_KEY_HERE":
        return "API Key set kora hoyni."
    hint = "Reply in Bangla." if bn else "Reply in English."
    data = {"contents": [{"parts": [{"text": hint + "\n" + text}]}]}
    last_err = "Unknown error"
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            r = requests.post(url, params={"key": KEY}, json=data, timeout=30).json()
            if "error" in r:
                last_err = r["error"].get("message", "Unknown error")
                low = last_err.lower()
                if "high demand" in low or "overloaded" in low or "not found" in low:
                    continue
                return "API Error: " + last_err
            return r["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            last_err = str(e)
    return "API Error: " + last_err

if __name__ == "__main__":
    name = input("Apnar nam ki? ").strip() or "Friend"
    while True:
        msg = input(name + ": ").strip()
        if msg.lower() in ["exit", "quit", "bye"]:
            break
        if not msg:
            continue
        bn = any("\u0980" <= c <= "\u09ff" for c in msg)
        print("AI:", ask_ai(msg, bn))
