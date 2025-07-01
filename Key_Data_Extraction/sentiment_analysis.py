import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from models import SentimentAnalysisRequest

def build_sentiment_analysis_chain():
    # Load environment variables from .env file
    load_dotenv()
    gemini_api_key = os.environ["GEMINI_API_KEY"]

    # Initialize the LLM with the Gemini API key
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        max_output_tokens=128,
        api_key=gemini_api_key,
    )

    # Define the parser for the structured output
    parser = PydanticOutputParser(pydantic_object=SentimentAnalysisRequest)
    fmt = parser.get_format_instructions()

    # Define the chat prompt template for sentiment analysis
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert for sentiment analysis. "
                "Only analyze relevant information from the text. "
                "If you do not know the value of an attribute asked to analyze, "
                "return cannot-extract for the attribute's value."
                "Respond with **only** valid JSON matching the schema."
            ),
            ("system", "{format_instructions}"),
            ("human", "{text}"),
        ]
    ).partial(format_instructions=fmt)

    # Define the chain for sentiment analysis using the LLM
    chain = prompt | chat_model

    return chain, parser


def sentiment_analysis(text: str):
    chain, parser = build_sentiment_analysis_chain()

    try:
        """Analyze sentiment of the input text using the defined chain."""
        response = chain.invoke({"text": text})
        return parser.parse(response.content)
    except OutputParserException as e:
        print(f"Error parsing output: {e}")
        return None

if __name__ == "__main__":
    text_s_n = "El día comenzó con una brisa ligera y algunas nubes dispersas en el cielo. En la oficina, las actividades siguieron la rutina habitual: envío de correos, reuniones programadas y revisión de informes. En la pausa del almuerzo, la mayoría de los compañeros optaron por el menú del día en la cafetería cercana, sin quejas ni elogios particulares. Al regresar, continuaron las tareas administrativas y el ambiente se mantuvo tranquilo, sin sobresaltos ni intercambios emocionales intensos. Fue una jornada estándar, con sus momentos de concentración y los breves descansos necesarios para recargar energía."
    result = sentiment_analysis(text_s_n)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_s_p = "Desperté con el suave rumor del viento acariciando las cortinas y una sensación de entusiasmo que recorría mi cuerpo. El aroma del café recién hecho impregnaba toda la casa, invitándome a saborear cada sorbo como un pequeño ritual de felicidad. Mientras revisaba mis mensajes, encontré palabras de apoyo y cariño de amigos y familiares, recordándome lo valioso que es el vínculo humano. Al salir a correr, el paisaje matinal me regaló tonos anaranjados y rosados en el horizonte, recordándome que cada día trae nuevas oportunidades para crecer, crear y compartir alegría con los demás."
    result = sentiment_analysis(text_s_p)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_s_ng = "Sentí un nudo en el estómago desde el primer momento en que abrí los ojos: una mezcla de inquietud y desazón que me acompañó todo el día. El tráfico matutino se volvió un caos insoportable, alimentando mi frustración antes incluso de llegar al trabajo. Allí, la pila de correos pendientes parecía crecer sin cesar, y cada llamado telefónico traía solicitudes urgentes que solo añadían presión. Las conversaciones con los colegas giraron en torno a problemas de última hora, y la fatiga mental se instaló con fuerza. Al terminar la jornada, regresé a casa deseando únicamente desconectar del mundo y sumergirme en el silencio más absoluto."
    result = sentiment_analysis(text_s_ng)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_p_p = "Sinto uma gratidão imensa por cada amanhecer que me dá a chance de recomeçar. Hoje acordei com o coração leve, envolvido por uma calma profunda que me lembra que sempre há algo pelo qual sorrir. Ao caminhar pelas ruas, percebi o canto dos pássaros anunciando novas possibilidades e o sol desenhando padrões de luz nas fachadas coloridas. Cada passo foi um convite para abraçar a esperança, cultivar pensamentos otimistas e compartilhar afeto com quem cruza meu caminho. Senti o calor humano estampado em sorrisos e gestos gentis, e a certeza de que a vida, mesmo com seus desafios, pulsa beleza a cada instante."
    result = sentiment_analysis(text_p_p)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_p_n = "O dia iniciou com o céu nublado e poucas pessoas circulando pelas calçadas. O trânsito fluía de forma regular, sem grandes engarrafamentos, e os estabelecimentos comerciais abriam suas portas no horário habitual. Ao longo da manhã, o movimento nos cafés era moderado: alguns frequentadores liam jornal, outros conversavam sobre assuntos rotineiros de trabalho. As conversas giravam em torno de compromissos comuns, como reuniões e tarefas domésticas, sem demonstrar animação excessiva ou desânimo perceptível. Foi um dia como tantos outros, organizado e previsível, sem eventos marcantes nem surpresas."
    result = sentiment_analysis(text_p_n)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_p_ng = "Hoje acordei com uma sensação de peso no peito que parecia impedir qualquer conforto. As notícias pela manhã trouxeram relatos de perdas e dificuldades, e cada manchete aprofundou minha angústia. Ao sair de casa, senti o vento frio como um lembrete cruel de que o mundo pode ser indiferente às nossas dores. As conversas no trabalho soaram mecânicas e até mesmo os colegas mais próximos pareciam distantes. A cada tarefa concluída, o vazio se ampliava, como se nada fizesse sentido, e encontrei-me desejando apenas a quietude do silêncio, longe de expectativas ou decepções."
    result = sentiment_analysis(text_p_ng)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_t_p = "เมื่อเช้านี้ฉันตื่นขึ้นพร้อมกับแสงแดดอ่อน ๆ ที่สาดส่องผ่านผ้าม่าน และรู้สึกเต็มไปด้วยกำลังใจที่พลุ่งพล่านในหัวใจ อากาศยามเช้าทำให้ฉันรู้สึกสดชื่น ระหว่างทางไปสวนสาธารณะ ฉันได้พบกับรอยยิ้มของผู้คนที่สัญจรรอบตัว การสนทนาเล็กน้อยกับคนที่ฉันไม่เคยรู้จักมาก่อนนั้นเต็มไปด้วยมิตรไมตรี เมื่อเดินกลับ ฉันรับรู้ถึงความอบอุ่นภายใน และรังสรรค์ความตั้งใจที่จะแบ่งปันความสุขเหล่านี้ให้กับทุกคนรอบข้าง"
    result = sentiment_analysis(text_t_p)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_t_n = "เช้าวันนี้ไม่มีอะไรพิเศษ แสงไฟจากโคมไฟถนนในระยะไกลสว่างขึ้นเมื่อฉันเดินผ่าน ปริมาณรถบนถนนไม่มากเกินไปและพอให้เคลื่อนตัวได้สะดวก เสียงพูดคุยกันตามร้านกาแฟยังคงเป็นไปตามเรื่องราวกิจวัตร ผู้คนสั่งเมนูอาหารเช้าแบบเดิม ๆ แล้วดื่มกาแฟไปพร้อม ๆ กับการเปิดอ่านข่าวรายวัน ทุกอย่างดำเนินไปตามปกติ ไม่มีเหตุการณ์ใดที่ทำให้รู้สึกตื่นเต้นหรือผิดหวังแต่อย่างใด"
    result = sentiment_analysis(text_t_n)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text_t_ng = "ฉันรู้สึกอ่อนล้าทั้งกายและใจตั้งแต่เช้า เมื่อลืมตา ทุกอย่างดูมืดมนและหนักอึ้ง ข่าวร้ายในโทรศัพท์ยิ่งทำให้ความหวังเลือนหายไป เมื่อเดินทางออกจากบ้าน ฉันเจอการจราจรติดขัดจนแทบไม่ขยับ ป้ายกำกับอารมณ์โกรธและหงุดหงิดชัดเจนในทุกการกระทำของฉัน ในที่ทำงาน งานที่ได้รับกลับมีแต่ปัญหาและคำร้องขอด่วนที่ไม่มีวันสิ้นสุด เมื่อเลิกงาน ฉันรู้สึกอยากหนีจากความวุ่นวายทั้งหมดและพักผ่อนเพียงลำพัง"
    result = sentiment_analysis(text_t_ng)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)

    text = "Đồ khốn nạn, mày tưởng mày là thần thánh gì mà dám hạch sách người khác khắp nơi? Địt mẹ bọn con buôn lời, cả ngày chỉ biết vác cái mồm méo mó của mày ra chém gió khắp chốn! Cút mẹ mày đi cho khuất mắt tao, đừng có mà chõ mũi vào chuyện không liên quan."
    result = sentiment_analysis(text)
    print("\n=== Sentiment Analysis Result ===\n")
    print(result)