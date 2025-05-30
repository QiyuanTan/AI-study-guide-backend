import traceback
from typing import Tuple
from langchain_core.tools import tool
from langgraph.constants import END


def validateMCQs(question: dict) -> Tuple[bool, str]:
    options = question.get("options", [])
    correct = question.get("correct_option", "")
    if not options:
        return False, "MCQ validation failed: No options provided."
    if correct not in options:
        return False, "MCQ validation failed: Correct option not in options list."
    return True, "MCQ validation passed."

def validateCode(question: dict) -> Tuple[bool, str]:
    script = question.get("autograder_script", "")
    samples = question.get("sample_input_output", [])

    try:
        # Syntax check
        compile(script, "<autograder>", "exec")
    except SyntaxError as e:
        return False, f"Syntax error in autograder script: {e}"

    return True, "Code question validation passed."

def validator(state: dict) -> dict:
    index = state["current_index"]
    question = state["questions"][index]  # Get current question
    valid = False
    message = ""

    if question["question_type"] == "mcq":
        valid, message = validateMCQs(question)  # Validate MCQ
    elif question["question_type"] == "code":
        valid, message = validateCode(question)  # Validate Code question

    # Set the validity flag
    state["curr_question_valid"] = valid  # True or False based on validation

    # Determine next node based on the question's validity
    if valid and index + 1 == state["num_questions"]:  # Last question, valid
        state["__next__"] = END
    elif valid:  # Valid question, continue to the autograder
        state["__next__"] = "autograder_generator"
        state["current_index"] += 1
    else:  # Invalid question, regenerate the question
        if question["question_type"] == "mcq":
            state["__next__"] = "generator"
        else:
            state["__next__"] = "autograder_generator"

    # Add validation message for logging/debugging
    state["messages"].append(f"Question {index} validation result: {message}")
    print(f"Question {index} validation result: {message}")

    return state
