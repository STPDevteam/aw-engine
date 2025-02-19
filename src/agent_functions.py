import sglang as sgl
import openai
import re
# here are the top ten agent functions contributing >90% LLM calls
# reference: https://github.com/joonspk-research/generative_agents/
def return_first_digit(s):
    return re.search(r'\d', s).group()

def get_embedding(text, model="text-embedding-ada-002"):
  text = text.replace("\n", " ")
  if not text: 
    text = "this is blank"
  return openai.Embedding.create(
          input=[text], model=model)['data'][0]['embedding']

def run_gpt_prompt_wake_up_hour(persona):
    #### TODO need to implement this
    pass
def run_gpt_prompt_daily_plan(persona, wake_up_hour):
    #### TODO need to implement this
    pass
def ChatGPT_single_request(prompt):
    #### TODO need to implement this
    pass
def run_gpt_prompt_task_decomp(persona, 
                               task, 
                               duration, 
                               test_input=None, 
                               verbose=False):
    pass
@sgl.function
def poignancy_event(s, persona_name, persona_iss, event):
    s += "Here is a brief description of " + persona_name + ".\n"
    s += persona_iss + "\n"
    s += "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following event for"
    s += persona_name + ".\n\n"
    s += "Event: " + event
    s += "Rate (return a number between 1 to 10):"
    s += sgl.gen(name="Rate", max_tokens=2)


def poignancy_chat_prompt(persona_name, persona_iss, event):
    # return prompt and max_tokens
    s = ""
    s += "Here is a brief description of " + persona_name + ".\n"
    s += persona_iss + "\n"
    s += "On the scale of 1 to 10, where 1 is purely mundane (e.g., routine morning greetings) and 10 is extremely poignant (e.g., a conversation about breaking up, a fight), rate the likely poignancy of the following event for"
    s += persona_name + ".\n\n"
    s += "Event: " + event
    s += "Rate (return a number between 1 to 10):"
    return {"prompt": s, "max_tokens": 2, "stop": None}

def poignancy_event_prompt(persona_name, persona_iss, event):
    # return prompt and max_tokens
    s = ""
    s += "Here is a brief description of " + persona_name + ".\n"
    s += persona_iss + "\n"
    s += "On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following event for"
    s += persona_name + ".\n\n"
    s += "Event: " + event
    s += "Rate (return a number between 1 to 10):"
    return {"prompt": s, "max_tokens": 2, "stop": None}

@sgl.function
def generate_event_triple(s, persona_name, action):
    s += """Task: Turn the input into (subject, predicate, object).
Input: Sam Johnson is eating breakfast. 
Output: (Dolores Murphy, eat, breakfast) 
--- 
Input: Joon Park is brewing coffee.
Output: (Joon Park, brew, coffee)
---
Input: Jane Cook is sleeping. 
Output: (Jane Cook, is, sleep)
---
Input: Michael Bernstein is writing email on a computer. 
Output: (Michael Bernstein, write, email)
---
Input: Percy Liang is teaching students in a classroom. 
Output: (Percy Liang, teach, students)
---
Input: Merrie Morris is running on a treadmill. 
Output: (Merrie Morris, run, treadmill)
---"""
    s += persona_name + "is" + action + ".\n"
    s += "(" + persona_name + ","
    s += sgl.gen(name="Triple", max_tokens=20, stop=")")


def generate_event_triple_prompt(persona_name, action):
    s = ""
    s += """Task: Turn the input into (subject, predicate, object).
Input: Sam Johnson is eating breakfast. 
Output: (Dolores Murphy, eat, breakfast) 
--- 
Input: Joon Park is brewing coffee.
Output: (Joon Park, brew, coffee)
---
Input: Jane Cook is sleeping. 
Output: (Jane Cook, is, sleep)
---
Input: Michael Bernstein is writing email on a computer. 
Output: (Michael Bernstein, write, email)
---
Input: Percy Liang is teaching students in a classroom. 
Output: (Percy Liang, teach, students)
---
Input: Merrie Morris is running on a treadmill. 
Output: (Merrie Morris, run, treadmill)
---"""
    s += persona_name + "is" + action + ".\n"
    s += "(" + persona_name + ","
    return {"prompt": s, "max_tokens": 20, "stop": ")"}


@sgl.function
def generate_pronunciatio(s, action):
    s += "Convert an action description to an emoji (important: use two or less emojis).\n"
    s += "Action description: " + action + ".\n"
    s += "Emoji:" + sgl.gen(name="Emoji", max_tokens=6)


def generate_pronunciatio_prompt(action):
    s = ""
    s += "Convert an action description to an emoji (important: use two or less emojis).\n"
    s += "Action description: " + action + ".\n"
    s += "Emoji:"
    return {"prompt": s, "max_tokens": 6, "stop": None}


@sgl.function
def action_location_sector(
    s,
    persona_name,
    living_sector,
    living_sector_areas,
    current_sector,
    current_sector_areas,
    daily_plan,
    sector_options,
    current_action,
    next_action,
):
    s += """Task -- choose an appropriate area  from the area options for a task at hand. 
Sam Kim lives in {Sam Kim's house} that has Sam Kim's room, bathroom, kitchen.
Sam Kim is currently in {Sam Kim's house} that has Sam Kim's room, bathroom, kitchen. 
Area options: {Sam Kim's house, The Rose and Crown Pub, Hobbs Cafe, Oak Hill College, Johnson Park, Harvey Oak Supply Store, The Willows Market and Pharmacy}.
* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.
For taking a walk, Sam Kim should go to the following area: {Johnson Park}
---
Jane Anderson lives in {Oak Hill College Student Dormatory} that has Jane Anderson's room.
Jane Anderson is currently in {Oak Hill College} that has a classroom, library
Area options: {Oak Hill College Student Dormatory, The Rose and Crown Pub, Hobbs Cafe, Oak Hill College, Johnson Park, Harvey Oak Supply Store, The Willows Market and Pharmacy}. 
* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.
For eating dinner, Jane Anderson should go to the following area: {Hobbs Cafe}
---"""
    s += (
        persona_name
        + " lives in "
        + living_sector
        + " that has "
        + living_sector_areas
        + ".\n"
    )
    s += (
        persona_name
        + " is currently in "
        + current_sector
        + " that has "
        + current_sector_areas
        + ".\n"
    )
    s += daily_plan + ".\n"
    s += "Area options: " + sector_options + ".\n"
    s += """* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.\n"""
    s += (
        persona_name
        + " is "
        + current_action
        + ". For "
        + next_action
        + ", "
        + persona_name
        + " should go to the following area: {"
    )
    s += sgl.gen(name="Location", max_tokens=10, stop="}")


def action_location_sector_prompt(
    persona_name,
    living_sector,
    living_sector_areas,
    current_sector,
    current_sector_areas,
    daily_plan,
    sector_options,
    current_action,
    next_action,
):
    s = ""
    s += """Task -- choose an appropriate area  from the area options for a task at hand. 
Sam Kim lives in {Sam Kim's house} that has Sam Kim's room, bathroom, kitchen.
Sam Kim is currently in {Sam Kim's house} that has Sam Kim's room, bathroom, kitchen. 
Area options: {Sam Kim's house, The Rose and Crown Pub, Hobbs Cafe, Oak Hill College, Johnson Park, Harvey Oak Supply Store, The Willows Market and Pharmacy}.
* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.
For taking a walk, Sam Kim should go to the following area: {Johnson Park}
---
Jane Anderson lives in {Oak Hill College Student Dormatory} that has Jane Anderson's room.
Jane Anderson is currently in {Oak Hill College} that has a classroom, library
Area options: {Oak Hill College Student Dormatory, The Rose and Crown Pub, Hobbs Cafe, Oak Hill College, Johnson Park, Harvey Oak Supply Store, The Willows Market and Pharmacy}. 
* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.
For eating dinner, Jane Anderson should go to the following area: {Hobbs Cafe}
---"""
    s += (
        persona_name
        + " lives in "
        + living_sector
        + " that has "
        + living_sector_areas
        + ".\n"
    )
    s += (
        persona_name
        + " is currently in "
        + current_sector
        + " that has "
        + current_sector_areas
        + ".\n"
    )
    s += daily_plan + ".\n"
    s += "Area options: " + sector_options + ".\n"
    s += """* Stay in the current area if the activity can be done there. Only go out if the activity needs to take place in another place.
* Must be one of the "Area options," verbatim.\n"""
    s += (
        persona_name
        + " is "
        + current_action
        + ". For "
        + next_action
        + ", "
        + persona_name
        + " should go to the following area: {"
    )
    return {"prompt": s, "max_tokens": 10, "stop": "}"}


@sgl.function
def action_location_object(
    s, persona_name, target_sector, target_sector_areas, current_action, next_action
):
    s += """
Jane Anderson is in kitchen in Jane Anderson's house.
Jane Anderson is going to Jane Anderson's house that has the following areas: {kitchen,  bedroom, bathroom}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For cooking, Jane Anderson should go to the following area in Jane Anderson's house:
Answer: {kitchen}
---
Tom Watson is in common room in Tom Watson's apartment. 
Tom Watson is going to Hobbs Cafe that has the following areas: {cafe}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For getting coffee, Tom Watson should go to the following area in Hobbs Cafe:
Answer: {cafe}
---"""
    s += (
        persona_name
        + " is going to "
        + target_sector
        + " that has the following areas: {"
        + target_sector_areas
        + "}\n"
    )
    s += """* Stay in the current area if the activity can be done there. 
* NEVER go into other people's rooms unless necessary."""
    s += (
        persona_name
        + " is "
        + current_action
        + ". For "
        + next_action
        + ", "
        + persona_name
        + "should go to the following area in "
        + target_sector
    )
    s += " (MUST pick one of {" + target_sector_areas + "}):\n"
    s += "Answer: {" + sgl.gen(name="Area", max_tokens=5, stop="}")


def action_location_object_prompt(
    persona_name, target_sector, target_sector_areas, current_action, next_action
):
    s = ""
    s += """
Jane Anderson is in kitchen in Jane Anderson's house.
Jane Anderson is going to Jane Anderson's house that has the following areas: {kitchen,  bedroom, bathroom}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For cooking, Jane Anderson should go to the following area in Jane Anderson's house:
Answer: {kitchen}
---
Tom Watson is in common room in Tom Watson's apartment. 
Tom Watson is going to Hobbs Cafe that has the following areas: {cafe}
Stay in the current area if the activity can be done there. Never go into other people's rooms unless necessary.
For getting coffee, Tom Watson should go to the following area in Hobbs Cafe:
Answer: {cafe}
---"""
    s += (
        persona_name
        + " is going to "
        + target_sector
        + " that has the following areas: {"
        + target_sector_areas
        + "}\n"
    )
    s += """* Stay in the current area if the activity can be done there. 
* NEVER go into other people's rooms unless necessary."""
    s += (
        persona_name
        + " is "
        + current_action
        + ". For "
        + next_action
        + ", "
        + persona_name
        + "should go to the following area in "
        + target_sector
    )
    s += " (MUST pick one of {" + target_sector_areas + "}):\n"
    s += "Answer: {"
    return {"prompt": s, "max_tokens": 5, "stop": "}"}


@sgl.function
def summarize_chat_relationship(s, statement, persona_name, target_persona_name):
    s += "[Statements]\n"
    s += (
        statement
        + "Based on the statements above, summarize "
        + persona_name
        + " and "
        + target_persona_name
        + "'s relationship. What do they feel or know about each other?"
    )
    s += sgl.gen(name="relationship", max_tokens=15, stop=None)


def summarize_chat_relationship_prompt(statement, persona_name, target_persona_name):
    s = "[Statements]\n"
    s += (
        statement
        + "Based on the statements above, summarize "
        + persona_name
        + " and "
        + target_persona_name
        + "'s relationship. What do they feel or know about each other?"
    )
    return {"prompt": s, "max_tokens": 15, "stop": None}


@sgl.function
def iterative_convo(
    s,
    persona_iss,
    persona_name,
    memory,
    past_context,
    current_location,
    current_context,
    target_persona_name,
    current_convo,
):
    s += """Context for the task: 

PART 1. 
{persona_iss}

Here is the memory that is in {persona_name}'s head: 
{memory}

PART 2. 
Past Context: 
{past_context}

Current Location: {current_location}

Current Context: 
{current_context}

{persona_name} and {target_persona_name} are chatting. Here is their conversation so far: 
{current_convo}

---
Task: Given the above, what should {persona_name} say to {target_persona_name} next in the conversation? And did it end the conversation?

Output format: Output a json of the following format: 
{{
"{persona_name}": "<{persona_name}'s utterance>",
"Did the conversation end with {persona_name}'s utterance?": "<json Boolean>"
}}
""".format(
        **locals()
    )
    s += sgl.gen(name="convo", max_tokens=50, stop=None)
    # s += "Context for the task:\n"
    # s += "PART 1.\n" + persona_iss + "\nHere is the memory that is in " + persona_name + "'s head:\n" + memory + "\n"
    # s += "PART 2.\nPast Context:\n" + past_context + "\nCurrent Location: " + current_location + "\nCurrent Context:\n" + current_context + "\n"
    # s += persona_name + " and " + target_persona_name + " are chatting. Here is their conversation so far:\n" + current_convo + "\n"
    # s += "---Task: Given the above, what should " + persona_name + " say to " + target_persona_name + " next in the conversation? And did it end the conversation?\n"
    # s += "Output format: Output a json of the following format: \n{\n\"" + \
    #     persona_name + "\": <" + persona_name + "'s utterance>\",\n\"Did the conversation end with " + persona_name + "'s utterance?\": \"<json Boolean>\"\n}"


def iterative_convo_prompt(
    persona_iss,
    persona_name,
    memory,
    past_context,
    current_location,
    current_context,
    target_persona_name,
    current_convo,
):
    s = """Context for the task: 

PART 1. 
{persona_iss}

Here is the memory that is in {persona_name}'s head: 
{memory}

PART 2. 
Past Context: 
{past_context}

Current Location: {current_location}

Current Context: 
{current_context}

{persona_name} and {target_persona_name} are chatting. Here is their conversation so far: 
{current_convo}

---
Task: Given the above, what should {persona_name} say to {target_persona_name} next in the conversation? And did it end the conversation?

Output format: Output a json of the following format: 
{{
"{persona_name}": "<{persona_name}'s utterance>",
"Did the conversation end with {persona_name}'s utterance?": "<json Boolean>"
}}
""".format(
        **locals()
    )
    return {"prompt": s, "max_tokens": 50, "stop": None}


@sgl.function
def generate_object_event(s, object_name, persona_name, persona_action):
    s += """Task: We want to understand the state of an object that is being used by someone. 

Let's think step by step. 
We want to know about {object_name}'s state. 
Step 1. {persona_name} is at/using the {persona_action}.
Step 2. Describe the {object_name}'s state: {object_name} is""".format(
        **locals()
    )
    s += sgl.gen(name="object_event", max_tokens=15, stop=None)


def generate_object_event_prompt(object_name, persona_name, persona_action):
    s = """Task: We want to understand the state of an object that is being used by someone. 

Let's think step by step. 
We want to know about {object_name}'s state. 
Step 1. {persona_name} is at/using the {persona_action}.
Step 2. Describe the {object_name}'s state: {object_name} is""".format(
        **locals()
    )
    return {"prompt": s, "max_tokens": 15, "stop": None}


@sgl.function
def action_object(s, action_seq, available_objects):
    s += """Current activity: sleep in bed
Objects available: {{bed, easel, closet, painting}}
Pick ONE most relevant object from the objects available: bed
---
Current activity: painting
Objects available: {{easel, closet, sink, microwave}}
Pick ONE most relevant object from the objects available: easel
---
Current activity: cooking
Objects available: {{stove, sink, fridge, counter}}
Pick ONE most relevant object from the objects available: stove
---
Current activity: watch TV
Objects available: {{couch, TV, remote, coffee table}}
Pick ONE most relevant object from the objects available: TV
---
Current activity: study
Objects available: {{desk, computer, chair, bookshelf}}
Pick ONE most relevant object from the objects available: desk
---
Current activity: talk on the phone
Objects available: {{phone, charger, bed, nightstand}}
Pick ONE most relevant object from the objects available: phone
---
Current activity: {action_seq}
Objects available: {{{available_objects}}}
Pick ONE most relevant object from the objects available:""".format(
        **locals()
    )
    s += sgl.gen(name="action_object", max_tokens=15, stop=None)


def action_object_prompt(action_seq, available_objects):
    s = """Current activity: sleep in bed
Objects available: {{bed, easel, closet, painting}}
Pick ONE most relevant object from the objects available: bed
---
Current activity: painting
Objects available: {{easel, closet, sink, microwave}}
Pick ONE most relevant object from the objects available: easel
---
Current activity: cooking
Objects available: {{stove, sink, fridge, counter}}
Pick ONE most relevant object from the objects available: stove
---
Current activity: watch TV
Objects available: {{couch, TV, remote, coffee table}}
Pick ONE most relevant object from the objects available: TV
---
Current activity: study
Objects available: {{desk, computer, chair, bookshelf}}
Pick ONE most relevant object from the objects available: desk
---
Current activity: talk on the phone
Objects available: {{phone, charger, bed, nightstand}}
Pick ONE most relevant object from the objects available: phone
---
Current activity: {action_seq}
Objects available: {{{available_objects}}}
Pick ONE most relevant object from the objects available:""".format(
        **locals()
    )
    return {"prompt": s, "max_tokens": 15, "stop": None}


@sgl.function
def generate_hourly_schedule(
    s,
    schedule_format,
    persona_iss,
    prior_schedule,
    intermission,
    intermission_,
    prompt_end,
):
    s += """Hourly schedule format: 
{schedule_format}
===
{persona_iss}
{prior_schedule}
{intermission}{intermission_}
{prompt_end}""".format(
        **locals()
    )
    s += sgl.gen(name="hourly_schedule", max_tokens=50, stop=None)


def generate_hourly_schedule_prompt(
    schedule_format,
    persona_iss,
    prior_schedule,
    intermission,
    intermission_,
    prompt_end,
):
    s = """Hourly schedule format: 
{schedule_format}
===
{persona_iss}
{prior_schedule}
{intermission}{intermission_}
{prompt_end}""".format(
        **locals()
    )
    return {"prompt": s, "max_tokens": 50, "stop": None}


if __name__ == "__main__":
    from inspect import signature
    funcs = [
        poignancy_event_prompt,
        generate_event_triple_prompt,
        generate_pronunciatio_prompt,
        action_location_sector_prompt,
        action_location_object_prompt,
        summarize_chat_relationship_prompt,
        iterative_convo_prompt,
        generate_object_event_prompt,
        action_object_prompt,
        generate_hourly_schedule_prompt,
    ]
    for f in funcs:
        print(f(*["__{}__".format(k) for k, v in signature(f).parameters.items()]))