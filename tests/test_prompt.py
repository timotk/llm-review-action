from llm_action.prompt import create_prompt


def test_create_prompt():
    content = "This is a test."
    # user_instruction = "This is a user instruction."
    prompt = create_prompt(content)
    assert content in prompt
    assert "$defs" in prompt, "The json schema is missing."


def test_create_prompt_with_user_instructions():
    content = "This is a test."
    user_instruction = "This is a user instruction."
    prompt = create_prompt(content, user_instruction=user_instruction)
    assert content in prompt
    assert "Here are some additional instructions:" in prompt
