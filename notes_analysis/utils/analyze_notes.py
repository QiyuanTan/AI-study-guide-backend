import json
import os
import re

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.constants import START
from langgraph.graph import StateGraph

from .llm import get_llm
from .nodes.validator import validator
from .state_types import State

load_dotenv()
llm = get_llm()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

summarizer_prompt_path = os.path.join(BASE_DIR, "utils", "prompts", "summarizer_prompt.txt")
quiz_generator_prompt_path = os.path.join(BASE_DIR, "utils", "prompts", "quiz_generator.txt")
autograder_prompt_path = os.path.join(BASE_DIR, "utils", "prompts", "autograder_prompt.txt")


def clean_markdown(raw_output: str) -> str:
    """
    Cleans model output by removing any Markdown code block formatting.
    Supports all markdown code blocks like ```lang\n...\n``` or just ```
    """
    # Match the first code block in the string regardless of language tag
    match = re.search(r"^```[^\n]*\n([\s\S]*?)\n```$", raw_output.strip(), re.MULTILINE)
    return match.group(1).strip() if match else raw_output.strip()



def generate_questions(notes, syllabus):

    print("Generating questions...")

    graph_builder = StateGraph(State)

    def summarizer(state: State):
        # Summarize the question and context
        with open(summarizer_prompt_path, "r", encoding='utf-8') as f:
            prompt = f.read()

        messages = [
            SystemMessage(prompt),
            HumanMessage(f"Here's the syllabus of my course:\n{syllabus}. \n\n"
                         f"Here's my notes:\n{notes}"),
        ]

        response = llm.invoke(messages, temperature=0.2)

        state["notes_summary"] = response.content
        print(f"generated summary: {response.content}")
        return state

    def generator(state: State):
        with open(quiz_generator_prompt_path, "r", encoding='utf-8') as f:
            prompt = f.read()

        if not state["curr_question_valid"]:
            # regenerate a single question
            print("regenerating single question...")
            messages = [
                SystemMessage(prompt),
                HumanMessage(state["notes_summary"]),
                AIMessage(json.dumps(state["questions"])),
                SystemMessage(
                    f"The question at index {state['current_index']} is invalid. "
                    f"Regenerate **only this question**, and return it as a single JSON object (not a list). "
                    f"Follow the exact schema provided earlier. Do not include explanations, markdown, or formatting."
                ),
                HumanMessage(f"Here is the validator feedback: {state['messages'][-1]}")
            ]
            response = llm.invoke(messages, temperature=0.4)
            question = json.loads(response.content)

            state["questions"][state["current_index"]] = question
            state["curr_question_valid"] = True

            print(f"regenerated question {state['current_index']}: {question}")
            state["messages"].append(f"regenerated question {state['current_index']}: {question}")
            return state
        else:
            # generate all questions
            print("generating questions...")
            messages = [
                SystemMessage(prompt),
                SystemMessage(f"The summary of notes and syllabus is as follows: {state['notes_summary']}"),
                HumanMessage(f"Please generate {state['num_questions']} questions for me."),
            ]

            response = llm.invoke(messages, temperature=0.55, max_tokens=5000*state["num_questions"])
            question = json.loads(clean_markdown(response.content))
            state["questions"] = question["questions"]

            state["messages"].append(f"generated questions: {question}")
            print(f"generated questions: {question}")
            return state

    def autograder(state: State):
        index = state["current_index"]
        question = state["questions"][index]

        if question["question_type"] != "code":
            state["messages"].append(f"Skipping autograder generation for question {index} of type {question['question_type']}.")
            print(f"Skipping autograder generation for question {index} of type {question['question_type']}.")
            return state  # Skip MCQs

        with open(autograder_prompt_path, "r", encoding='utf-8') as f:
            prompt = f.read()

        messages = [
            SystemMessage(prompt),
            HumanMessage(f"Here's the question you need to generate an autograder for:\n{json.dumps(question)}\n"),
        ]

        print("Generating autograder script...")

        if not state["curr_question_valid"]:
            messages.append(AIMessage(json.dumps(state["questions"][index]["autograder_script"])))
            messages.append(SystemMessage(f"The question at index {index} is invalid. "))
            messages.append(HumanMessage(f"Here is the validator's feedback: {state['messages'][-1]}"))

        response = llm.invoke(messages, temperature=0.3)
        response = clean_markdown(response.content)
        question["autograder_script"] = response

        state["messages"].append(f"generated autograder script for question {index}")
        print(f"generated autograder script for question {index}")

        return  state

    graph_builder.add_node("summarizer", summarizer)
    graph_builder.add_node("generator", generator)
    graph_builder.add_node("autograder_generator", autograder)
    graph_builder.add_node("validator", validator)

    graph_builder.add_edge(START, "summarizer")
    graph_builder.add_edge("summarizer", "generator")
    graph_builder.add_edge("generator", "autograder_generator")
    graph_builder.add_edge("autograder_generator", "validator")
    graph_builder.add_conditional_edges("validator", lambda state: state["__next__"])

    graph = graph_builder.compile()

    final_state = graph.invoke({
        "questions": [],
        "num_questions": 5,
        "current_index": 0,
        "notes_summary": "",
        "curr_question_valid": True,
        "messages": [
        ]},
        {"recursion_limit": 15})

    # for message in final_state['messages']:
    #     print(message)

    return final_state["questions"]

if __name__ == "__main__":
    # notes = "lecture 1:\n 1 + 1 = 2 \n2 + 2 = 4\n3 + 3 = 6 addition is fun!"
    # syllabus = "Course on basic math\nTopics: addition, subtraction, multiplication, division\n"
    syllabus = "Recursion and Dynamic Programming\nTopics: Fibonacci sequence, factorial calculation, memoization\n"
    notes = "Lecture 1: Recursion basics\n- Fibonacci sequence\n- Factorial calculation\n- Memoization techniques\n\nLecture 2: Dynamic Programming\n- Coin change problem\n- Longest common subsequence\n- Knapsack problem\n"

    questions = generate_questions(notes, syllabus)

    print("Generated Questions:")
    for question in questions:
        print(question)