import requests
import json
from groq import Groq

print("\n--- Class 4: Multi-Tool AI Agent Started ---")

# 1. Groq Client Init
client = Groq(api_key="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")

# --- TOOL 1: Weather Fetcher ---
def get_current_weather(city):
    """Sheher ka live weather fetch karne wala tool"""
    try:
        url = f"https://wttr.in/{city}?format=%t"
        res = requests.get(url)
        temp = res.text.strip()
        return f"{city} ka temperature {temp} hai."
    except:
        return "Weather fetch nahi ho saka."

# --- TOOL 2: Math Calculator ---
def calculate_math(expression):
    """Math calculations karne wala tool"""
    try:
        # Python ka eval function math calculate karta hai
        result = eval(expression)
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Math calculate nahi ho saka: {e}"

# 2. Both Tools Definitions for AI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Kisi sheher ka live weather maloom karne ke liye use karein.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Sheher ka naam"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Koi bhi math ya hisaab kitaab solve karne ke liye use karein (e.g. 250 * 15, 1200 / 4, 45 + 90).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression e.g. '250 * 15'"}
                },
                "required": ["expression"]
            }
        }
    }
]

# 3. Chat History (Memory)
messages = [
    {
        "role": "system",
        "content": "Aap Habib bhai ke Smart Multi-Tool Assistant hain. Zaroorat ke mutabiq sahi tool (Weather ya Math) choose karein."
    }
]

print("[SYSTEM]: Multi-Tool Agent Ready! ('exit' likhein band karne ke liye)\n")

# 4. Continuous Loop
while True:
    user_input = input("Habib: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n[AI AGENT]: Khuda hafiz Habib bhai!")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Check agar AI ne koi tool call karne ka faisla kiya hai
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                tool_output = ""

                # Decision 1: Weather Tool
                if function_name == "get_current_weather":
                    city_name = function_args.get("city")
                    print(f"\n[SYSTEM]: ⚡ Weather Tool Running for: {city_name}")
                    tool_output = get_current_weather(city_name)

                # Decision 2: Math Tool
                elif function_name == "calculate_math":
                    expr = function_args.get("expression")
                    print(f"\n[SYSTEM]: 🧮 Math Calculator Tool Running for: {expr}")
                    tool_output = calculate_math(expr)

                # Send tool output back to AI
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                })

                # Get final answer from AI
                second_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages
                )
                ai_reply = second_response.choices[0].message.content
                print(f"\nAI Agent: {ai_reply}\n")
                messages.append({"role": "assistant", "content": ai_reply})
        else:
            ai_reply = response_message.content
            print(f"\nAI Agent: {ai_reply}\n")
            messages.append({"role": "assistant", "content": ai_reply})

        print("-" * 50)

    except Exception as e:
        print(f"\n[SYSTEM ERROR]: {e}\n")