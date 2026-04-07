from groq import Groq

def analyze_price(prices: list[float], api_key: str, rsi: float) -> str:
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'''
                    I have these 5 Bitcoin prices from the last 2 minutes: {prices}.
                    RSI for those prices gives: {rsi}.
                    Act as a crypto analyst. Is the trend going up or down? Answer in 1 sentence.
                ''',
            }
        ],
        model="openai/gpt-oss-20b",
    )
    print(chat_completion.choices[0].message.content)