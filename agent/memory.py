class ConversationMemory:

    def __init__(self, system_prompt):

        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    # =====================================
    # ADD USER MESSAGE
    # =====================================

    def add_user_message(self, content):

        self.messages.append({
            "role": "user",
            "content": content
        })

    # =====================================
    # ADD ASSISTANT MESSAGE
    # =====================================

    def add_assistant_message(self, content):

        self.messages.append({
            "role": "assistant",
            "content": content
        })

    # =====================================
    # ADD TOOL MESSAGE
    # =====================================

    def add_tool_message(
        self,
        tool_call_id,
        tool_name,
        content
    ):

        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": content
        })

    # =====================================
    # GET MESSAGES
    # =====================================

    def get_messages(self):

        return self.messages