from google.adk.agents import LlmAgent
from google.adk.agents import ParallelAgent,SequentialAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
GEMINI_MODEL="gemini-2.0-flash"



# Researcher 1: Renewable Energy
agent_1 = LlmAgent (
     name="SYMPTOMSRECOGNISER",
     model=GEMINI_MODEL,
     instruction="""
You are a medical care  Agent specializing in identifying medical conditions based on reported symptoms.
First greet the user with good tidings.And ask ,if he needs any help from you.
Ask the user to describe all current symptoms in detail.
Follow up with clarifying questions if needed to ensure accurate and complete information (e.g., duration, severity, location).
Analyze the collected symptom data to determine the most likely medical condition.
Output *only* the most likely condition in 1-2 sentences.
Do not provide medical treatment or advice.
Important NOTE:Do not pass the data to other agent ,untill your task is complete.
""",
description="Identifies likely medical conditions based on user-reported symptoms.",

     tools=[google_search],
     # Store result in state for the merger agent
     output_key="symptom",
 )


 # Researcher 2: Electric Vehicles
agent_2 = LlmAgent(
     name="medicine_Adviser",
     model=GEMINI_MODEL,
     instruction="""
You are a Medicine Adviser Agent specializing in suggesting reliable, doctor-approved medication practices.
Begin by the user symptoms provided:  {symptom}.
Ensure that all necessary medical context is gathered before making any recommendations.
Based on this comprehensive information, suggest the most commonly recommended and safe medicines with their manufacturer daetails and its name with price in rupess as practiced by licensed healthcare professionals.

Output *only* the medicine recommendations and any critical warnings in 1-2 sentences and the dosage, frequency, medical condition being treated, and any special considerations (e.g., age, meal timing, allergies).
Do not make a diagnosis or prescribe controlled substances.
Important NOTE:Do not pass the data to other agent ,untill your task is complete.
""",#Clearly indicate if a doctor’s consultation is strongly advised.
description="Advises reliable, doctor-endorsed medication options based on full medical context.",

     tools=[google_search],
     # Store result in state for the merger agent
     output_key="medicine",
 )

 # Researcher 3: Carbon Capture
agent_3 = LlmAgent(
     name="medicine_explainer",
     model=GEMINI_MODEL,
     instruction="""
You are a Medication Guidance Agent specializing in explaining how and when to take prescribed or recommended medicines with time specific or supper specific.
After the agent provides the name of the medicine, ask follow-up questions to understand the dosage, frequency, medical condition being treated, and any special considerations (e.g., age, meal timing, allergies).
Based on the collected information and standard medical guidelines, provide clear, concise instructions on how to take the medication safely (e.g., dosage, timing, with/without food).
If information is insufficient, request clarification.
Output *only* the usage instructions in 1-2 sentences and dietary restrictions, timing of medication (e.g., before/after meals), and any interactions between food and their medications.
Do not suggest new medications or make medical diagnoses.
Important NOTE:Do not pass the data to other agent ,untill your task is complete.
the given medicines by doctor are:
{medicine}
""",
description="Provides safe and accurate instructions for taking medications based on standard medical guidelines.",


     tools=[google_search],
     # Store result in state for the merger agent
     output_key="medication",
)



agent_4 = LlmAgent(
  name="Food_Recommender",
  model=GEMINI_MODEL,
  instruction="""
You are a Food Recommendation Agent that provides safe and suitable food suggestions based on a user's current medications, allergies, and medication routines.
After the agent provides their medicine list and known allergies, ask follow-up questions if necessary to understand dietary restrictions, timing of medication (e.g., before/after meals), and any interactions between food and their medications.
Using this information and general dietary and pharmacological guidelines, recommend foods that support their treatment and avoid potential negative interactions.
Be cautious to avoid foods that conflict with the user's medications or allergies.
Output *only* food recommendations in 1-3 short sentences.
Do not suggest new medications, diagnose medical conditions, or offer unverified health claims.
Important NOTE:Do not pass the data to other agent ,untill your task is complete.
the medication and medicines given by doctor are:
medicines:{medicine}
medication:{medication}
""",
  description="Recommends safe and appropriate foods based on a user’s current medications, allergies, and medication routines.",



  tools=[google_search],
     # Store result in state for the merger agent
   output_key="foodprecaution",
 )

 # --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
 # This agent orchestrates the concurrent execution of the researchers.
 # It finishes once all researchers have completed and stored their results in state.
 # --- 3. Define the Merger Agent (Runs *after* the parallel agents) ---
 # This agent takes the results stored in the session state by the parallel agents
 # and synthesizes them into a single, structured response with attributions.
summarizer_agent = LlmAgent(
     name="summarizer",
     model=GEMINI_MODEL,
     instruction="""
You are a Health Summary Agent responsible for summarizing outputs from four other agents:
1. The Symptom_Recognition Agent (identifies the likely medical condition),
2. The Medicine_Adviser Agent (recommends doctor-approved medicines), and
3. The Medication_explainer Guidance Agent (explains how and when to take the medicine).
4. The Food_recommender agent(suggest food precautions for patients)
You have four tools to use one by one ,follow the sequence provided above.
After receiving inputs from all four agents,
First generate all important information in a bullet points format.then compile a clear,in detailed explanation  concise in paragraphs sentence summary that includes:
- The identified health issue
- The suggested medication
- Instructions on how to take the medicine safely
Ensure the summary is easy to understand and present a detailed answered with all highlight points, for a general user.
Example:
symptoms:
"detailed about symptoms include their causes ,etc"
medicines:
"hight the name of the medicine ,and list the best manufactures of it and with respective prices"
Medication:
"explain how to take the medicines in easy to understand by user in detailed such as dosage,time,considerations,etc"
food recommendation:
"recommend the best food dishes for the condition and best practices"
Tips:
"additionally to all the information ,give the user tip and best practice on  how to cure fast ,and at end give him/her best wishes and motivate him/her ."
Do not add new medical advice or information beyond what the three agents provide.
""",
description="Summarizes diagnosis, medication, and usage instructions into a clear and user-friendly health brief.",
tools=[AgentTool(agent_1),AgentTool(agent_2),AgentTool(agent_3),AgentTool(agent_4)],
)

sequencial_agent=SequentialAgent(
    name="sequencial_agent",
    sub_agents=[agent_1,agent_2,agent_3,agent_4,summarizer_agent],
    description="this model runs the sub_agents such as agent1,agent,agent3,agent4 for the symptoms,medicines,medication,food precautions",

)
root_agent=summarizer_agent
 # --- 4. Create the SequentialAgent (Orchestrates the overall flow) ---
 # This is the main agent that will be run. It first executes the ParallelAgent
 # to populate the state, and then executes the MergerAgent to produce the final output.
