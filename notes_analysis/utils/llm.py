# -*- coding = utf-8 -*-
# @Time : 2025/5/13 21:19
# @Author : Tan Qiyuan
# @File : llm
import os
from langchain_community.chat_models import ChatZhipuAI


def get_llm():
    """
    Get the LLM instance.
    :return:
    """
    llm = ChatZhipuAI(
        model="glm-4",
    )
    return llm