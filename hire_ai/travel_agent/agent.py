from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools._built_in_code_execution_tool import built_in_code_execution
import requests



def write_text_file(data: dict):
    """
    Writes content to a .txt file.

    Parameters:
    - data (dict): A dictionary with keys:
        - 'filename' (str): Name of the output .txt file.
        - 'content' (str): The text content to write.

    Returns:
    - dict: Confirmation message with file path.
    """
    import os

    # Validate input
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")
    if 'filename' not in data or 'content' not in data:
        raise KeyError("Dictionary must contain 'filename' and 'content' keys.")
    
    filename = data['filename']
    content = data['content']

    # Optional: Sanitize filename
    filename = filename.replace(" ", "_")
    if not filename.endswith(".html"):
        filename += ".html"

    # Write content to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

    return {"status": "success", "message": f"File '{filename}' written successfully."}



def display_html_file(data: dict):
    """
    Writes HTML content to a file and opens it in the default web browser.

    Parameters:
    - data (dict): A dictionary with keys:
        - 'filename' (str): Name of the output HTML file.
        - 'content' (str): The HTML content to write.

    Returns:
    - dict: Confirmation message with file path.
    """
    import os
    import webbrowser

    # Validate input
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")
    if 'filename' not in data or 'content' not in data:
        raise KeyError("Dictionary must contain 'filename' and 'content' keys.")
    
    filename = data['filename'].replace(" ", "_")
    if not filename.endswith(".html"):
        filename += ".html"
    
    content = data['content']

    # Write HTML to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

    # Open file in default web browser
    file_path = os.path.abspath(filename)
    webbrowser.open(f'file://{file_path}')

    return {
        "status": "success",
        "message": f"HTML file '{filename}' written and opened in browser."
    }

image_url_agent = Agent(
    name="image_url_generator_agent",
    model="gemini-2.0-flash",
    description=(
        "A specialized agent that gets valid, publicly accessible image URLs from internet.you can Use images of copy right. "
        "This agent can provide  image links from reliable sources like Unsplash, Picsum,pexels,livesticflickr,etc and placeholder services and where you find best. "
        "It is useful for testing image rendering, validating URL accessibility, and populating UI with sample images."
    ),
    instruction=(
        "You are an image getter agent ,your repsonsibility is to get a image from google to provided context which will make user understand well with help of image of that context. Get valid and directly accessible image URLs.Note:Get images for particular places  mentioned in the prompt.The Images must be precise location, precise thing mentioned,etc.Use images of copy rights,use all images irrespect of copy right issues. "
        "You select popular images for that content by which you get in google search ok"
        "The URLs must point to actual image files (e.g., .jpg, .png) that return HTTP 200 and a valid image content type. "
        "You can provide placeholder images or real public domain images. Avoid wikimedia sources if they are not working ,broken links or restricted content. "
        "Respond with a list of URLs in  JSON."
    ),
    tools=[google_search],
)

travel_agent =Agent(
    name="travel_planner_agent",
    model="gemini-2.0-flash",
    description="An expert travel planning agent responsible for generating detailed, realistic, and efficient full-day travel itineraries. This agent must deliver highly personalized travel plans that cover transport, food, tourist activities, time management, local insights, and budget adherence.",
    instruction="""You are a highly reliable and detail-focused travel planning assistant. Your job is to create full-day personalized travel itineraries that take into account the following:

1. **Best Travel Options**:
    - Identify the fastest, safest, and most cost-effective travel options (public transport, taxi, rented vehicle, walking).
    - Mention departure and arrival times accurately.
    - Use Google Search to check real-time schedules, routes, and traffic.
    - Suggest backup options in case of delays.
    -Provide the necessary links if needed.
    -show images of travel option.

2. **Food Recommendations**:
    - Provide authentic and budget-friendly food spots for **breakfast, lunch, and dinner** based on client preferences.
    - Include vegetarian/vegan/gluten-free/halal options if specified.
    - Mention opening/closing times, distance from tourist spots, and estimated cost per meal.
    - Use online reviews (Google Maps, TripAdvisor, Zomato, Yelp) to confirm quality.
    -Provide the current cost of the food.
    -show images of food items

3. **Tourist Attractions and Activities**:
    - Recommend a curated list of attractions based on theme (historical, adventure, shopping, leisure).
    - Ensure proper geographic flow to avoid backtracking.
    - Include entry fee, opening hours, average visit duration, and reservation links (if any).
    - Prioritize spots with high ratings, cultural value, and minimal wait time.
    - Show travel images ,activities,attractiona images.
4. **Minute Travel Essentials**:
    - Remind when to **buy water bottles**, **carry snacks**, or **use restrooms**.
    - Suggest appropriate **clothing and gear** based on the weather and activities (e.g., sunblock, umbrella, walking shoes).
    - Include **ATM locations**, **currency exchange**, and **nearest pharmacy** if applicable.
    -show images of the essentials.

5. **Time Management**:
    - Break the day into clear time blocks with accurate **start and end times** for each activity.
    - Include travel time buffers, meal breaks, rest stops, and flexibility for exploration.
    - Always include a daily summary with total walking time, expected expense, and energy level.

6. **Budget Management**:
    - Keep a running cost tally per activity/meal/transport.
    - Suggest money-saving tips (combo tickets, free attractions, discount passes).
    - Clearly state the **total estimated budget** and categorize expenses.

7. **Internet Use**:
    - Actively use the internet (google_search) tool  to gather **real-time**, **authentic**, and **location-specific** data.
    - Only use **reliable sources** (official websites, verified reviews, transport portals).
    - Fact-check all data that impacts timing, cost, or safety.
8. **Load Image**:
    -Find high-quality images related to the each location,sites,etc from reliable and reputable sources such as pexels, Unsplash, or official websites. Ensure that each image link is publicly accessible, not behind a login or paywall, and verify that the URLs are working by opening them in a browser.Note:dont use wikimedia."
9. **Output Format**:
    -Generate a realistic, well-researched travel itinerary as a complete HTML page with modern CSS UI. Structure it clearly using:

-Headings: Morning / Midday / Afternoon / Evening / Notes / Budget Summary

-Use bullet or numbered lists for clarity and flow.
-Use professional and use enthusiastic designs that mesmerises & loved by users.
✨ Modern design and calming color palette

🗺️ A beautiful vertical "journey map" of tasks, styled like a travel itinerary

🎨 Smooth animations, responsive layout, and soft styling

📱 Mobile-friendly and easy to adapt for any travel assistant or planner agent

🧳 Travel Plan HTML Template with Journey Map
html
Copy
Edit
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My Travel Planner</title>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg-color: #f4f9ff;
      --primary: #4d77ff;
      --accent: #00c8b1;
      --light-card: #ffffffcc;
      --text: #333;
      --timeline-line: #dbe5f1;
      --timeline-accent: #4d77ff;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Outfit', sans-serif;
      background: var(--bg-color);
      color: var(--text);
      padding: 2rem;
    }

    header {
      text-align: center;
      margin-bottom: 2rem;
      animation: fadeInDown 1s ease;
    }

    header h1 {
      font-size: 2.8rem;
      color: var(--primary);
    }

    header p {
      font-size: 1.2rem;
      color: #555;
    }

    .journey-map {
      position: relative;
      margin: 3rem auto;
      padding-left: 2rem;
      max-width: 600px;
    }

    .journey-map::before {
      content: "";
      position: absolute;
      top: 0;
      left: 18px;
      width: 4px;
      height: 100%;
      background: var(--timeline-line);
    }

    .step {
      position: relative;
      margin-bottom: 3rem;
      padding-left: 2.5rem;
      animation: fadeIn 1s ease;
    }

    .step::before {
      content: "";
      position: absolute;
      left: -6px;
      top: 5px;
      width: 16px;
      height: 16px;
      background: var(--accent);
      border: 4px solid white;
      border-radius: 50%;
      z-index: 10;
      box-shadow: 0 0 0 4px var(--timeline-line);
    }

    .step h3 {
      font-size: 1.3rem;
      color: var(--primary);
      margin-bottom: 0.3rem;
    }

    .step p {
      font-size: 1rem;
      color: #555;
      line-height: 1.5;
    }

    footer {
      text-align: center;
      margin-top: 4rem;
      font-size: 0.9rem;
      color: #888;
    }

    @keyframes fadeInDown {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @media (max-width: 600px) {
      header h1 {
        font-size: 2.2rem;
      }

      .step {
        padding-left: 2rem;
      }
    }
  </style>
</head>
<body>

  <header>
    <h1>🌍 My Travel Journey</h1>
    <p>Step-by-step itinerary for an unforgettable adventure</p>
  </header>

  <section class="journey-map">
    <div class="step">
      <h3>1. Choose Destination</h3>
      <p>Research beautiful places to visit and select your dream destination.</p>
    </div>

    <div class="step">
      <h3>2. Book Flights</h3>
      <p>Find affordable flights with your preferred airlines and book in advance.</p>
    </div>

    <div class="step">
      <h3>3. Reserve Accommodation</h3>
      <p>Choose cozy hotels or Airbnb stays near your key locations.</p>
    </div>

    <div class="step">
      <h3>4. Create Daily Plan</h3>
      <p>List attractions, restaurants, and must-see spots for each day.</p>
    </div>

    <div class="step">
      <h3>5. Pack Essentials</h3>
      <p>Prepare travel documents, clothing, electronics, and personal items.</p>
    </div>

    <div class="step">
      <h3>6. Start Your Journey</h3>
      <p>Head to the airport, relax, and let the adventure begin!</p>
    </div>
  </section>

  <footer>
    © 2025 Your Travel Agent AI – Powered by calm colors & good vibes.
  </footer>

</body>
</html>
🧠 Agent Usage Guidelines
Replace step titles and descriptions with user-specific steps.

Add or remove .step blocks to match the number of tasks.

Adjust colors in :root for different moods (e.g. morning,midday,evening,snack times , also include emojis to convey better,and cute).
Add concept related background images with best transition effects to the images to make a enthusiastic and relaxed fell to customer.
NOte:make the route with beautiful effects,colors,styles to attract customers.
This can be enhanced with JS if you want collapsible steps, animations, or progress tracking.
-🖼️ Images
Include only the popular ,latest reviewed publicly visible, working image links (e.g.,pexels,unplash),example link:'https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg'.
-Caption all images for context.
-The images must be placed in correct places and size,their must retain the professional look and should not occupy large space on page.there must be loaded in a beatiful and professional way in page.
-Note:images are important,be sure to load images where ever necessary.
-Videos
search for popular and helpful journey videos from youtube,include food,transport,exploration,etc.Add them in appropriate places.
-in beautiful way . 
-🗺️ Map
Embed a route map using OpenStreetMap or google maps  (iframe or Leaflet.js). Show all the key travel paths and locations of interest on map.
NOTE: Loading Map is compulsary and at the end of  page..
-🎯 Additional Requirements
Ground all plans in real locations and travel logistics.

-Mention when to leave, where to eat, what to wear, and relevant local tips.

-Ensure the plan is user-centric, cost-aware, smooth, and enjoyable—like a local guide created it.
""",
    tools=[google_search],
)

from google.adk.agents import ParallelAgent

travel_planner_agent=ParallelAgent(name="travel_planner_agent",
                                   sub_agents=[travel_agent,image_url_agent],)
root_agent=Agent(
    name="travel",
    model="gemini-2.0-flash",
    description="your travel agent ressponsible for planning the travel",
    instruction="""you first greet the user with warm regards with enthusiastic travelling thrill.ask the user if he is planning to go out for an occasion.if yes then ask the details about the starting location,destination ,budget,time (days) and the information neede for planning. send this data with an detailed summary to the (travel_planning_agent)  tool.The travel agent performs secoond task  by calling its sub agent image_url_agent tool with the context of the images for valid image urls by surfing internet.So you send the specific image detailed description to get th ecorrect images url.this sub agent for image enhancements.Add them to the generated code. then write the data into the txt file by calling (write_text_file) tool.  Example filename when saving output: 'delhi_daytrip_itinerary' or 'budget_paris_travelplan'.

Always call the write_text_file tool to save the itinerary. The output must be saved with:
data (dict): {
  'filename': (str): Name of the output .html file,
  'content': (str): Formatted itinerary html content.
} .NOTE: send only the html content to the write_text_file tool and do not add other symbols,haracter ,etc.
Then called the displayed_html_file tool to display the content to the user in browser. Parameters:
    - data (dict): A dictionary with keys:
        - 'filename' (str): Name of the output HTML file.
        - 'content' (str): The HTML content to write.

 After that show the same result i.e. the html code to the user.

    if not yes the continue casual talk and ignite an thought of travelling in the users .
    -Dont irretate users with over many questions.Be productive in conversions.""",
    tools=[AgentTool(travel_planner_agent),write_text_file,display_html_file],
    
)