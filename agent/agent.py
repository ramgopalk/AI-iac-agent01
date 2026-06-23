import json

from groq import Groq

from config import Config
from tools import TOOLS, execute_tool
from prompts import SYSTEM_PROMPT
from agent.memory import ConversationMemory


class AzureAgent:

    def __init__(self):

        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

        self.memory = ConversationMemory(
            SYSTEM_PROMPT
        )

    # =====================================
    # MAIN CHAT LOOP
    # =====================================

    def chat(self, user_input):

        self.memory.add_user_message(user_input)

        # =====================================
        # FIRST LLM CALL
        # =====================================

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.memory.get_messages(),
            tools=TOOLS
        )

        assistant_message = response.choices[0].message

        # =====================================
        # NO TOOL CALL
        # =====================================

        if not assistant_message.tool_calls:

            final_message = assistant_message.content

            self.memory.add_assistant_message(
                final_message
            )

            return final_message

        # =====================================
        # STORE ASSISTANT TOOL CALL MESSAGE
        # =====================================

        self.memory.messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": assistant_message.tool_calls
        })

        # =====================================
        # EXECUTE TOOL CALLS
        # =====================================

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"\n[TOOL CALL] {tool_name}")
            print(f"[ARGUMENTS] {arguments}")

            tool_result = execute_tool(
                tool_name,
                arguments
            )

            print("\n[TOOL RESULT]")
            print(json.dumps(tool_result, indent=2))

            # =====================================
            # DIRECT DISCOVERY RESPONSES
            # =====================================

            if tool_name == "list_resource_groups":

                if not tool_result:
                    return "No Azure resource groups found."

                formatted = "\n".join([
                    f"- {rg['name']} ({rg['location']})"
                    for rg in tool_result
                ])

                final_message = (
                    "Azure Resource Groups:\n\n"
                    f"{formatted}"
                )

                self.memory.add_assistant_message(
                    final_message
                )

                return final_message

            elif tool_name == "list_acr_registries":

                if not tool_result:
                    return "No Azure Container Registries found."

                formatted = "\n".join([
                    f"- {acr['name']} ({acr['location']})"
                    for acr in tool_result
                ])

                final_message = (
                    "Azure Container Registries:\n\n"
                    f"{formatted}"
                )

                self.memory.add_assistant_message(
                    final_message
                )

                return final_message

            elif tool_name == "list_aks_clusters":

                if not tool_result:
                    return "No AKS clusters found."

                formatted = "\n".join([
                    f"- {aks['name']} ({aks['location']})"
                    for aks in tool_result
                ])

                final_message = (
                    "Azure AKS Clusters:\n\n"
                    f"{formatted}"
                )

                self.memory.add_assistant_message(
                    final_message
                )

                return final_message

            # =====================================
            # TERRAFORM EXECUTION TOOL SUMMARY
            # =====================================

            tool_summary = {
                "status": "success"
            }

            if isinstance(tool_result, dict):

                failed = False
                error_message = None

                for stage in ["init", "plan", "apply"]:

                    stage_result = tool_result.get(stage)

                    if stage_result:

                        if stage_result.get("returncode") != 0:

                            failed = True

                            error_message = (
                                stage_result.get("stderr")
                                or stage_result.get("stdout")
                            )

                            break

                if failed:

                    tool_summary = {
                        "status": "failed",
                        "error": error_message
                    }

                else:

                    tool_summary = {
                        "status": "success",
                        "message": f"{tool_name} executed successfully"
                    }

            # =====================================
            # STORE TOOL MESSAGE
            # =====================================

            self.memory.add_tool_message(
                tool_call.id,
                tool_name,
                json.dumps(tool_summary)
            )

        # =====================================
        # FINAL LLM RESPONSE
        # =====================================

        second_response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.memory.get_messages()
        )

        final_message = second_response.choices[0].message.content

        self.memory.add_assistant_message(
            final_message
        )

        return final_message