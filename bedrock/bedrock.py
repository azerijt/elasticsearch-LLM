
# streamlit run app.py
import os
import boto3
import json
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

session = boto3.Session()
print("Current AWS profile:", session.profile_name)
# chain function to create our bedrock object 
def bedrock_chain():
    profile = "default"

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",
    )
# model selection
    cohere_llm = Bedrock(
        model_id="cohere.command-light-text-v14", client=bedrock_runtime, credentials_profile_name=profile
    )
    cohere_llm.model_kwargs = {"temperature": 0.5, "max_tokens": 400}

#     kwargs ={ aws bedrock-runtime invoke-model \
# --model-id cohere.command-light-text-v14 \
# --body "{\"prompt\":\"\",\"max_tokens\":400,\"temperature\":0.75,\"p\":0.01,\"k\":0,\"stop_sequences\":[],\"return_likelihoods\":\"NONE\"}" \
# --cli-binary-format raw-in-base64-out \
# --region us-east-1 \
# invoke-model-output.txt}

# prompt template includes instruction, context, input
    prompt_template = """System: The following is a friendly conversation between a knowledgeable helpful assistant and a customer.
    The assistant is talkative and provides lots of specific details from it's context.

    Current conversation:
    {history}

    User: {input}
    Bot:"""
    PROMPT = PromptTemplate(
        input_variables=["history", "input"], template=prompt_template
    )
# configure memory
    memory = ConversationBufferMemory(human_prefix="User", ai_prefix="Bot")
    conversation = ConversationChain(
        prompt=PROMPT,
        llm= cohere_llm,
        verbose=True,
        memory=memory,
    )

    return conversation

def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    return chain({"input": prompt}), num_tokens


def clear_memory(chain):
    return chain.memory.clear()