from company_list import companies_top20
from metrics import metrics_all, metrics_short

import os
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatPerplexity

NCompanies = len(companies_top20)
NMetrics   = len(metrics_all)

def setUpLLM():
    file_path = 'perplexity_key'
    with open(file_path, 'r') as file:
        file_contents = file.read()

    os.environ['PPLX_API_KEY'] = file_contents

def createChat(model = 'llama-3.1-sonar-huge-128k-online',
               temperature=0.0):
    
    chat = ChatPerplexity(model=model, temperature=temperature)
    
    # define the chat prompt template
    system_message = "You are the assistant"
    human_message = "{input}"
    prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message)
    ])

    return prompt | chat

def getPrompt():
    prompt_text_template = """{METRIC} for {COMPANY}.
    If the information is not available, report it with a -1.
    Clearly list all sources"""

    return prompt_text_template

def checkIsValidCompanyId(companyId):
    if companyId >= NCompanies:
        raise ValueError(f"companyId must be less than {NCompanies}")
    
def checkIsValidMetricId(metricId):
    if metricId >= NMetrics:
        raise ValueError(f"metricId must be less than {NMetrics}")

def composePrompt(companyId,metricId):
    checkIsValidCompanyId(companyId)
    checkIsValidMetricId(metricId)

def getPromptResponse(chat,companyId,metricsId,response):
    checkIsValidCompanyId(companyId)
    checkIsValidMetricId(metricsId)

    company = companies_top20[companyId]
    metric  = metrics_all[metricsId]

    if response.get(company) is not None:
        response[company][metric] = {}
    else:
        response[company] = {}
        response[company][metric] = {}

    prompt_text = getPrompt().format(METRIC=metric,COMPANY=company)
    chat_response = chat.invoke({"input":prompt_text})
    response[company][metric] = chat_response

def getResponses(chat,companyId,response):
    for metricId in range(NMetrics):
        print(metricId, 'of', NMetrics, ':',  metrics_all[metricId])
        getPromptResponse(chat,companyId,metricId,response)


    