import sys
import json

convo_keys = "next in the conversation? And did it end the conversation?"
convo_relationship = "relationship. What do they feel or know about each other?"

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python parse_traces.py traces")
    traces = json.load(open(sys.argv[1]))

    convo_actions = {}

    for step, trace in traces.items():
        for persona, actions in trace.items():
            convo_count = 0
            for i, action in enumerate(actions):
                if convo_relationship in action["prompt"]:
                    convo_count += 1
                    assert convo_keys in actions[i + 1]["prompt"]
                    if persona not in convo_actions:
                        convo_actions[persona] = {}
                    new_step = str(int(step) + convo_count)
                    if new_step not in convo_actions[persona]:
                        convo_actions[persona][new_step] = []
                    # print(convo_count)
                    # print(new_step)
                    convo_actions[persona][new_step].extend(actions[i:i + 2])

    # print(convo_actions)
    new_teaces = {step: {persona: [] for persona in trace} for step, trace in traces.items()}

    for persona, steps in convo_actions.items():
        for step, actions in steps.items():
            if step not in new_teaces:
                new_teaces[step] = {}
            if persona not in new_teaces[step]:
                new_teaces[step][persona] = []
            new_teaces[step][persona] = actions

    for step, trace in traces.items():
        for persona, actions in trace.items():
            for i, action in enumerate(actions):
                if convo_relationship in action["prompt"] or convo_keys in action["prompt"]:
                    continue
                new_teaces[step][persona].append(action)

    sorted_teaces = {k: new_teaces[k] for k in sorted(new_teaces)}
    open("new_traces.json", "w").write(json.dumps(sorted_teaces, indent=4))
