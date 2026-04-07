from groq import Groq

def analyze_price(prices: list[float], api_key: str, rsi: float, fvg: int, msa: int) -> str:
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'''
                    I have these 5 Bitcoin prices from the last 2 minutes: {prices}.
                    RSI for those prices gives: {rsi}.
                    FVG for those prices gives: {fvg}.
                    MSA for those prices gives: {msa}.
                    Act as a crypto analyst. Is the trend going up or down? Answer in 1 sentence.
                ''',
            }
        ],
        model="openai/gpt-oss-20b",
    )
    
    response = chat_completion.choices[0].message.content

    return response