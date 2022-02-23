def get_user_input(message, valid_answers=None, default_answer=None):
    """Show message to user and get input from user.

    Args:
        message (str): Message to show to user. It should not contain newline, valid choices and default answer as they will be added automatically.
        valid_answers (list[str]): list of valid answers that user can enter. This answers will also be added to message.
        default_answer (str, optional): A default answer that user can enter. Defaults to None.

    Returns:
        str: User input.
    """
    if valid_answers:
        message += "({})".format("/".join(valid_answers))

    if default_answer:
        message += "[{}]".format(default_answer)

    answer = input(message).lower()

    while valid_answers and answer not in valid_answers + ['']:
        print(f"Wrong answer!")
        answer = input(message).lower()
    return answer or default_answer or ''