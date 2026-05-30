import json
from typing import List, Dict, Any, Optional, Callable, Union
from .prompt import build_prompt
from ..utils.formatter import OutputFormatter

REACT = "Plan > Act > Observe > Respond. Format: Thought, Action, Action Input (JSON), Observation..., Final Answer."

class Agent:
    def __init__(self, role: str, task: str):
        self.role, self.task, self.tools, self.funcs = role, task, [], {}
    
    def add_tool(self, name: str, desc: str, params: Dict, req: List[str] = None, func: Callable = None):
        schema = {"name": name, "description": desc, "parameters": {"type": "object", "properties": params, "required": req or []}}
        self.tools.append(schema)
        if func: self.funcs[name] = func

    def prompt(self, query: str, context: str = "") -> str:
        constr = f"1. Follow ReAct format.\n2. Use tools:\n{json.dumps(self.tools)}" if self.tools else "Answer directly."
        return build_prompt(role=self.role, task=self.task, context=context, constraint=constr, input_data=query)

    def call_tool(self, action: str, action_input: Union[str, Dict]) -> Any:
        if isinstance(action_input, str):
            try: action_input = json.loads(action_input)
            except: pass
        if action in self.funcs:
            try:
                return self.funcs[action](**action_input) if isinstance(action_input, dict) else self.funcs[action](action_input)
            except Exception as e:
                return f"Error executing {action}: {str(e)}"
        return f"Error: Tool {action} not found."

    def format_output(self, data: Any, format_type: str = "markdown") -> str:
        """Utility to format data using the built-in formatter."""
        return OutputFormatter.format(data, format_type)

class MultiAgentManager:
    def __init__(self): self.agents: Dict[str, Agent] = {}

    def add_agent(self, name: str, role: str, task: str):
        self.agents[name] = Agent(role, task)
        return self.agents[name]

    def route_prompt(self, query: str) -> str:
        roles = {n: a.role for n, a in self.agents.items()}
        return build_prompt(
            role="Router Agent",
            task=f"Route query to best agent: {json.dumps(roles)}",
            output_contract={"agent_name": "name from keys", "reason": "why"},
            input_data=query
        )

def get_react_prompt(query: str, tools: List[Dict], role: str = "AI") -> str:
    a = Agent(role, REACT)
    a.tools = tools
    return a.prompt(query)
