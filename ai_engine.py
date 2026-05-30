
# ==========================================
# SYNOPTIMESH — AI ENGINE (GROQ)
# ==========================================

from groq import Groq

GROQ_API_KEY         = "YOUR_API_KEY_HERE"   # <-- paste your Groq key
groq_client          = Groq(api_key=GROQ_API_KEY)
conversation_history = []

# ==========================================
# SINGLE QUERY
# ==========================================

def ask_ai(prompt):

    conversation_history.append({
        "role": "user",
        "content": prompt
    })

    recent = conversation_history[-6:]

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Synoptimesh, an advanced brain-computer interface AI assistant. "
                        "You help control desktop, mobile, IoT, and embedded systems. "
                        "Be concise, helpful, and accurate."
                    )
                },
                *recent
            ]
        )

        reply = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        print(f"\n[SYNOPTIMESH AI]\n{reply}\n")
        return reply
    
    except Exception as e:
        print(f"\n[AI ERROR] {e}\n")

# ==========================================
# FULL AI SESSION (loops until exit)
# ==========================================

def start_ai_session():

    print("\n" + "=" * 50)
    print("   SYNOPTIMESH AI — SESSION STARTED")
    print("   Type 'exit' or 'back' to return")
    print("=" * 50 + "\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "back", "return", "quit"]:
            print("\n[AI] Session ended. Returning...\n")
            break

        if user_input == "":
            continue

        ask_ai(user_input)

# ==========================================
# CLEAR MEMORY
# ==========================================

def clear_memory():
    conversation_history.clear()
    print("\n[AI] Memory cleared.\n")
