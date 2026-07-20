import requests
import json
from groq import Groq

print("\n--- Class 3: Smart AI Agent with Tools Started ---")

# 1. Groq Client Init
client = Groq(api_key="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")

# 2. Real Python Function (Weather Fetcher)
def get_current_weather(city):
    """Sheher ka live weather fetch karne wala tool"""
    try:
        url = f"https://wttr.in/{city}?format=%t"
        res = requests.get(url)
        temp = res.text.strip()
        return f"{city} ka temperature is waqt {temp} hai."
    except:
        return "Weather fetch nahi ho saka."

# 3. Tool Description (AI ko batana ke hamare paas ye tool majood hai)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Kisi bhi sheher ka live weather aur temperature maloom karne ke liye ye tool use karein.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Sheher ka naam, e.g. Lahore, Multan, Karachi"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 4. Chat History (Memory)
messages = [
    {
        "role": "system",
        "content": "Aap Habib bhai ke Smart Assistant hain. Agar weather ka poochen toh get_current_weather tool call karein, warna aam baat karein."
    }
]

print("[SYSTEM]: Smart Agent Tools ke sath tayar hai! ('exit' likhein band karne ke liye)\n")

# 5. Continuous Loop
while True:
    user_input = input("Habib: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n[AI AGENT]: Khuda hafiz Habib bhai!")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        # AI se response mangwana (Tools ke sath)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check karein kya AI ne kisi tool/function ko call karne ka faisla kiya hai?
        if response_message.tool_calls:
            print("\n[SYSTEM]: 🧠 AI Agent ne Tool Call karne ka faisla kiya...")
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "get_current_weather":
                    # Tool run karna
                    city_name = function_args.get("city")
                    print(f"[SYSTEM]: ⚡ Weather Tool running for: {city_name}")
                    tool_output = get_current_weather(city_name)
                    
                    # Tool ka result AI ko wapis bhejna
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output
                    })
                    
                    # AI se final jawab lena
                    second_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages
                    )
                    ai_reply = second_response.choices[0].message.content
                    print(f"\nAI Agent: {ai_reply}\n")
                    messages.append({"role": "assistant", "content": ai_reply})
        else:
            # Agar tool zaroori nahi tha, toh aam jawab
            ai_reply = response_message.content
            print(f"\nAI Agent: {ai_reply}\n")
            messages.append({"role": "assistant", "content": ai_reply})

        print("-" * 50)

    except Exception as e:
        print(f"\n[SYSTEM ERROR]: {e}\n")