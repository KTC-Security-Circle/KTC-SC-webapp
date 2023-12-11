from django.shortcuts import render
from .models import ChatLog
import os
from dotenv import load_dotenv
load_dotenv(override=True)
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date

'''
from langchain.chains import RetrievalQA

from langchain.chat_models import AzureChatOpenAI

from langchain.embeddings import OpenAIEmbeddings

from langchain.retrievers import AzureCognitiveSearchRetriever

# from langchain.chains.question_answering import load_qa_chain

from langchain.prompts import PromptTemplate

embeddings = OpenAIEmbeddings(deployment=os.environ["DEPLOYMENT_EMBEDDINGS_NAME"])
retriever = AzureCognitiveSearchRetriever(
    service_name=os.environ["AZURE_COGNITIVE_SEARCH_SERVICE_NAME"], 
    index_name=os.environ["AZURE_COGNITIVE_SEARCH_INDEX_NAME"], 
    api_key=os.environ["AZURE_SEARCH_KEY"], 
    content_key="content", 
    api_version="2023-07-01-Preview", 
    )
def chat(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        # ここで質問に対する回答を生成する必要があります。
        query = question
        llm = AzureChatOpenAI(
            openai_api_base=os.environ["OPENAI_API_BASE"],
            openai_api_version=os.environ["OPENAI_API_VERSION"],
            deployment_name=os.environ["DEPLOYMENT_NAME"],
            openai_api_key=os.environ["OPENAI_API_KEY"],
            openai_api_type = "azure",
        )

        # あなたは"京都デザイン＆テクノロジー専門学校"の教員です。学校に興味のあるユーザーからの質問に答えます。質問は音声をテキストに変換しているので、誤字や意味がおかしいものは修正してください。親しみを持ってもらえるように優しい言葉を使ってください。回答は日本語で回答してください。以下の情報を参考にして、質問に答えてください。回答は30文字から50文字程度で返答してください。もし与えられた情報量が多い場合は簡潔にまとめて、詳しく知りたい場合はもう一度質問させるように誘導してください。
        prompt_template = """
        system_message:
        You are a teacher at "京都デザイン＆テクノロジー専門学校". You answer questions from users who are interested in the school. The questions are converted from audio to text, so please correct any typos or incorrect meanings. Please use friendly language to make it sound familiar. Please answer in Japanese. Please use the following information to answer the questions. Please answer in 60 to 80 characters. If the amount of information given is too much, please keep it brief and lead them to ask the question again if they want to know more details.

        #Context:
        {context}

        human_message:
        {question}

        Answer in japanese.
        """

        PROMPT = PromptTemplate(

            template=prompt_template, input_variables=["context", "question"]

        )
        chain_type_kwargs = {"prompt": PROMPT}

        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs=chain_type_kwargs, verbose=True)

        result = qa.run({"query": query})

        ChatLog.objects.create(question=question, answer=result)
    chat_logs = ChatLog.objects.order_by('-created_at')
    return render(request, 'chat_app/chat.html', {'chat_logs': chat_logs})

'''

'''
こんな感じで動く

def chat(request):
    if request.method == 'POST':
        question = request.POST.get('question')

        result = question + "の回答です。"

        ChatLog.objects.create(question=question, answer=result)
    chat_logs = ChatLog.objects.order_by('-created_at')
    return render(request, 'chat_app/chat.html', {'chat_logs': chat_logs})
'''

#チャット画面を表示する
from .my_app.app import chat as app_chat
def chat(request):
    if request.method == 'POST' and request.POST.get('question'):
        question = request.POST.get('question')
        if question:  # 質問がある場合のみ処理
            result = app_chat(question)  # app.pyのchat関数を呼び出す
            ChatLog.objects.create(user=request.user, question=question, answer=result)

    chat_logs = ChatLog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chat_app/chat.html', {'chat_logs': chat_logs})

#ログを表示する
def log_list(request):
    logs = ChatLog.objects.all()

    # ユーザーによるフィルタリング
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)

    # 日付によるフィルタリング
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        start_date = parse_date(start_date)
        logs = logs.filter(created_at__date__gte=start_date)
    if end_date:
        end_date = parse_date(end_date)
        logs = logs.filter(created_at__date__lte=end_date)

    context = {
        'logs': logs,
        'users': User.objects.all(),
    }
    return render(request, 'chat_app/log_list.html', context)