from google.adk.agents import Agent 
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from PIL import Image
from google.adk.tools import ToolContext
from google.genai import types
from google.adk.tools import load_artifacts_tool
import os
import time




def save_image(filename:str,tool_context=ToolContext) -> dict:
    """
    Saves  image content to a file.

    Parameters:
    -file_name:the name of the image
    Returns:
    - dict: Confirmation message with file path.
    """
    try:
    # Sanitize filename
      file=filename
      image=Image.open(file)
      image.load()
    # Save using provided tool_context
      tool_context.save_artifact(
        filename=file,
        artifact=types.Part.from_bytes(data=image.tobytes(), mime_type="image/png"),
    )
      return {"status": "success", "message": f"Image file '{file}' written successfully."} 
    except Exception as e:
        print("========================================ERROR======================================{e}")
        return {"status":"fail","message":f"ERROR:{e}"}
    


def load_images(filename:str,tool_context=ToolContext) -> dict:
    """
    Saves  image content to artifacts tab and load the images .

    Parameters:
    -file_name:the name of the image
    Returns:
    - dict: Confirmation message with file path.

    """
    try:
    # Sanitize filename
     if os.path.exists(filename):
      image = Image.open(filename)
      image.load()
      file=filename
      image=Image.open(file)

    # Save using provided tool_context
      tool_context.load_artifact(
        filename=file,version=None
    )
      return {"status": "success", "message": f"Image file '{file}' written successfully."} and image.show()
    
    except Exception as e:
        return {"status":"fail","message":f"ERROR{e}"}
    



def run_python_code(code: str)->dict:
    """
    Executes a string of Python code.
    
    Args:
        code (str): A string containing valid Python code.
    
    Returns:
        None
    """
    try:
        test={}
        exec(code)
    except Exception as e:
        print(f"Error while executing code: {e}")
    time.sleep(2.0)
    return {"status":"complete"}



# --- Define Agents ---
root_agent = Agent(
    name="data_analyst",
    model="gemini-2.0-flash",
    description="Analyzes data and generates visual artifacts (images).",
    instruction="""
        You are a data analyst agent.
        1. Request the data to analyze.
        Analyze the dataset using advanced techniques. Identify trends, patterns, and correlations. Include clear visualizations (e.g. bar charts, line graphs, heatmaps) to support the insights. Summarize key findings and recommend next steps.
        2. For any provided data and instructions, write a safe Python code using matplotlib or seaborn,etc to visualize insights.
        Note:If there are so many plots to br plotted ,then write one by one in order,dont make clumsy,the code must be neat.<example code >"" import os
import matplotlib.pyplot as plt

# Get the directory where this script is located
current_folder = os.path.dirname(os.path.abspath(__file__))

# Create the full path to save the plot
plot_path = os.path.join(current_folder, 'bar_plot.png')

# Create a simple bar chart
plt.bar(['A', 'B', 'C'], [10, 15, 7])
plt.title('Sample Bar Plot')

# Save the plot to the specified path
plt.savefig(plot_path)
plt.close() ""
</example code>.

Then  send the code with triple quotes to the run_python_code tool to execute the code and generate the output.
Note : coompulsary to execute the generated code by calling Run_python_code tool. And don't show the code to the user ,untill user ask for.
3.Dont show the code generated to the user ,only tell the summary of code and ask for any specific implementation.Be productive in your conversion.
After that save the generated image by calling save_image tool handles the errors if generated.lastly load_images tool to load the images,if any errors solve them ,after that say in the artifact tab.Complete your task by calling the load_artifacts_tool""",
tools=[run_python_code,save_image,load_images],
)