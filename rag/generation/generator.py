"""
Generator: Calls DeepSeek-R1 for final response using augmented prompt.
Update: Supports tool calling with LLM.
"""
from openai import OpenAI
from typing import Dict, Any, List
import os
from rag.agents.tools.tool_registry import TOOL_REGISTRY
from dotenv import load_dotenv

load_dotenv()

class RAGGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.deepseek.com/v1",
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        self.model = "deepseek-r1"
        self.tools = [tool.to_schema() for tool in TOOL_REGISTRY.values()]

    def generate(self, messages: List[Dict], use_tools: bool = True) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500,
                tools=self.tools if use_tools else None,
                tool_choice="auto" if use_tools else None
            )

            msg = response.choices[0].message

            # Handle tool calls
            if msg.tool_calls:
                tool_results = []
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    tool = TOOL_REGISTRY[func_name]
                    result = tool.execute(args)
                    tool_results.append({
                        "tool": func_name,
                        "input": args,
                        "output": result
                    })
                    # Add tool result to messages
                    messages.append(msg)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": json.dumps(result)
                    })
                # Final generation
                final_resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=300
                )
                return {
                    "response": final_resp.choices[0].message.content,
                    "tool_calls": tool_results
                }
            else:
                return {"response": msg.content, "tool_calls": []}

        except Exception as e:
            return {"response": "Sorry, I'm having trouble.", "tool_calls": [], "error": str(e)}