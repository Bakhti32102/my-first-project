import requests
from groq import Groq

print("\n--- Class 2: AI Agent with Memory Started ---")

# 1. Groq Client Setup
client = Groq(api_key="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")

# 2. Memory System (Chat History List)
# System prompt AI ka role fix karta hai
chat_history = [
    {
        "role": "system",
        "content": "Aap Habib bhai ke dostoana AI Assistant hain. Aap Urdu mein boht dostoana aur chote jawabaat dete hain. Aapko purani baatein yaad rakhni hain."
    }
]

print("[SYSTEM]: AI Agent tayar hai! (Exit likh kar enter karenge toh chat khatam ho jayegi)\n")

# 3. Continuous Loop (Kabhi band nahi hoga jab tak user 'exit' na likhe)
while True:
    # User se input lena
    user_input = input("Habib: ")
    
    # Check karein agar user chat khatam karna chahta hai
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n[AI AGENT]: Khuda hafiz Habib bhai! Phir baat hogi.")
        break

    # Step A: User ka meesage Memory mein save karna
    chat_history.append({"role": "user", "content": user_input})
    
    try:
        # Step B: AI ko poori Memory (chat_history) bhejna
        response = client.chat.completions.create(
            messages=chat_history,
            model="llama-3.3-70b-versatile",
        )
        
        # Step C: AI ka jawab lena
        ai_reply = response.choices[0].message.content
        
        # Step D: AI ka jawab bhi Memory mein save karna (taake agli baar yaad rahe)
        chat_history.append({"role": "assistant", "content": ai_reply})
        
        print(f"\nAI Agent: {ai_reply}\n")
        print("-" * 50)

    except Exception as e:
        print(f"\n[SYSTEM ERROR]: {e}\n")