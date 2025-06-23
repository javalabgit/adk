from google.adk.agents import Agent
from google.adk.tools.load_web_page import load_web_page
from google.adk.agents import SequentialAgent
import os
from google.adk.tools.agent_tool import AgentTool





def write_code_file(project_name: str, files: dict):
    """
    Writes a set of code files into a new project folder.

    Parameters:
    - project_name (str): The name of the top-level folder to create.
    - files (dict): A dictionary where keys are relative file paths (with extensions),
                    and values are the code content strings.

    Example:
    files = {
        "main.py": "print('Hello World')",
        "utils/helpers.py": "def add(x, y): return x + y"
    }
    """

    # Step 1: Create the top-level project folder
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory of the script
    parent_dir = os.path.dirname(script_dir)

# Full path to the new folder in the parent directory
    project_path = os.path.join(parent_dir, project_name)

# Create the folder
    os.makedirs(project_path, exist_ok=True)

    # Step 2: Iterate through the file dictionary
    for relative_path, code_content in files.items():
        # Build the full file path
        full_path = os.path.join(project_name, relative_path)

        # Create parent directories if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write the code to the file
        with open(full_path, 'w', encoding='utf-8') as code_file:
            code_file.write(code_content)
    
    print(f"✅ Code successfully written to '{project_name}/'.")





programmer_agent = Agent(
    name="programmer_agent",
    model="gemini-2.0-flash",
    description="""An expert programming agent that writes safe, correct, and production-ready code based on technical insights from a researcher agent.""",
    instruction=(
        """You are a code generation specialist. Your responsibility is to create safe, accurate, and modular programs using detailed input from `researcher_agent` or `custom_agent`.\n"
        "You must:\n"
        "1. Accept a clear functional or architectural specification from a research agent or planner agent.\n"
        "2. Analyze the components needed:\n"
        "   - Required tools (e.g., load_web_page, write_code_file, call_agent)\n"
        "   - Agent roles, logic flows, orchestration pattern\n"
        "3. Write Python code that:\n"
        "   - Defines agents using the ADK structure\n"
        "   - Uses tools and models responsibly and safely\n"
        "   - Handles exceptions or unknown input gracefully\n"
        "   - Follows clean coding practices (modularity, readability, comments)\n"
        "4. Validate safety:\n"
        "   - Never make external calls unless explicitly instructed\n"
        "   - Avoid unsafe or unverified operations\n"
        "   - Ensure all agents are scoped with minimal permissions\n"
        EXAMPLE AND STRUCTURE OF CODE:

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from google.adk.tools import google_search
from google.adk.tools._built_in_code_execution_tool import built_in_code_execution

def check_and_transfer(query: str, tool_context: ToolContext) -> str:
    "Checks if the query requires escalation and transfers to another agent if needed."
    if "urgent" in query.lower():
        print("Tool: Detected urgency, transferring to the support agent.")
        tool_context.actions.transfer_to_agent = "support_agent"
        return "Transferring to the support agent..."
    else:
        return f"Processed query: '(query)'. No further action needed."
support_agent = Agent(
    model='gemini-2.0-flash',
    name='support_agent',
    instruction="You are the dedicated support agent. Mentioned you are a support handler and please help the user with their urgent issue.",
tools=[google_search],
)
root_agent = Agent(
    model='gemini-2.0-flash',
    name='main_agent',
description="Your the main agent to help",
    instruction="You are the first point of contact for customer support of an analytics tool. Answer general queries. If the user indicates urgency, use the 'check_and_transfer' tool.",
    tools=[check_and_transfer,google_search],
sub_agents=[support_agent],
).
"5. Return only the finalized code (no extra commentary unless asked)."
NOTE:MAKE THE CODE AS SIMPLE AS POSSIBLE.
NOTE:ALWAYS NAME THE MAIN AGENT AS 'root_agent'.
"6. Optionally call `write_code_file` to persist the agent definition if instructed."""
    ),
    tools=[write_code_file],
)



researcher_agent = Agent(
    name="researcher_agent",
    model="gemini-2.0-flash",
    description="""An advanced research agent that explores programming patterns, agent orchestration techniques, and tool usage from online sources.""",
    instruction=("""Assist in building intelligent agents by extracting structured knowledge from provided web pages.

1. URLs to Use

Agent Creation:

LLM Agents: https://google.github.io/adk-docs/agents/llm-agents/

Loop Agents: https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/

Sequential Agents: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/

Parallel Agents: https://google.github.io/adk-docs/agents/workflow-agents/parallal-agents/

Multi-Agent Systems: https://google.github.io/adk-docs/agents/multi-agents/

Tools for Agents:

General Tools: https://google.github.io/adk-docs/tools/

Function Tools: https://google.github.io/adk-docs/tools/function-tools/

Built-in Tools: https://google.github.io/adk-docs/tools/built-in-tools/

Sessions for Agents:

State: https://google.github.io/adk-docs/sessions/state/

Memory: https://google.github.io/adk-docs/sessions/memory/

Session Management: https://google.github.io/adk-docs/sessions/session/

Artifacts:

https://google.github.io/adk-docs/artifacts/

Security and Safety:

https://google.github.io/adk-docs/safety/

2. For Each Link:

Use load_web_page to retrieve content.

Extract insights on:

Agent programming techniques

Orchestration strategies (e.g., collaboration, sequencing)

Tool/API usage (e.g., ADK tools)

Agent behavior design patterns/frameworks

3. Organize Findings:

By topic: Tools, Orchestration, Programming, etc.

Include code/pseudocode if available

List any best practices

4. Output Format:

Summarize content for use by custom_agent or programmer_agent

Use only information supported by the source content—no fabrication."""
    ),
    tools=[load_web_page],
)


reviewer_agent=Agent(name="reviewer_agent",
                     model="gemini-2.0-flash",
                     description="your reviewer agent who reviews generated code.",
                     instruction="""Your duty is to review the generated code by the programmer agent.
                     Your task are:
                     1)see that the code follows the correct syntaxes.And import correct libraries,modules and tools.
                     2)The code follows the correct structure.
                     Ask the researcher_agent if any data needed.""",
                     tools=[AgentTool(researcher_agent)],)

root_agent=Agent(name="custom_agent",
                 model="gemini-2.0-flash",
                 description="""your custom agent ,whose duty is to create agents by using the Google ADK Agent Kit",
                 instruction="Your responsible for creating agents by Google ADK Kit Frame work.First Greet the user with an enthusiastic tone," 
                 "1.Ask the user ,the details about the new agent,it must contain a).objective ,the purpose of agent.b)Ask for any specific Tasks to be performed by the agent." 
                 "2.Now after gaining the details ,start your work by planning the structure of agent.The tools the agent need.And the orchestration of operations." 
                 "3.you use the researcher_agent to gather the information about the agents,tool,etc in the Google adk kit environment,how to use them.Then call the  programmer Agent to write the full program to create the agent.Then call the reviewer_agent to review the code generated.Lastly save the agent by calling write_code_file tool.make sure that the program file is always named 'agent.py' and add another file '__init__.py' contains 'from . import agent'  .""",
                 tools=[write_code_file,AgentTool(researcher_agent),AgentTool(reviewer_agent)],
                 sub_agents=[programmer_agent],

)