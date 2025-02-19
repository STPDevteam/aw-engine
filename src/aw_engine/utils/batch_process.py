import json

import parse_traces
import parse_movements

traces = [
    "chatgpt_llm_data_8kstep.json", "chatgpt_llm_data_8kstep_2.json", "chatgpt_llm_data_8kstep_3.json",
    "chatgpt_llm_data_4.json", "chatgpt_llm_data_5.json", "chatgpt_llm_data_6.json", "chatgpt_llm_data_7.json",
    "chatgpt_llm_data_8.json", "chatgpt_llm_data_9.json", "chatgpt_llm_data_10.json", "chatgpt_llm_data_11.json",
    "chatgpt_llm_data_12.json", "chatgpt_llm_data_13.json", "chatgpt_llm_data_14.json", "chatgpt_llm_data_15.json",
    "chatgpt_llm_data_16.json", "chatgpt_llm_data_17.json", "chatgpt_llm_data_18.json", "chatgpt_llm_data_19.json",
    "chatgpt_llm_data_20.json"
]

movements = [
    "chatgpt_location_data_8kstep.json", "chatgpt_location_data_8kstep_2.json", "chatgpt_location_data_8kstep_3.json",
    "chatgpt_location_data_4.json", "chatgpt_location_data_5.json", "chatgpt_location_data_6.json",
    "chatgpt_location_data_7.json", "chatgpt_location_data_8.json", "chatgpt_location_data_9.json",
    "chatgpt_location_data_10.json", "chatgpt_location_data_11.json", "chatgpt_location_data_12.json",
    "chatgpt_location_data_13.json", "chatgpt_location_data_14.json", "chatgpt_location_data_15.json",
    "chatgpt_location_data_16.json", "chatgpt_location_data_17.json", "chatgpt_location_data_18.json",
    "chatgpt_location_data_19.json", "chatgpt_location_data_20.json"
]
num_traces = len(traces)
assert num_traces == len(movements)

for i in range(14, num_traces):
    trace = json.load(open("raw_traces/" + traces[i]))
    movement = json.load(open("raw_traces/" + movements[i]))

    for (base_step, target_step, status) in [(2160, 2520, "quiet"), (4320, 4680, "busy")]:
        new_traces = parse_traces.change_format(trace, base_step, target_step,
                                                f"raw_traces/excerpt_traces/{status}/{i}_trace.json")
        new_movement, num_steps = parse_movements.change_format(movement, 0, target_step)
        parse_movements.validation(new_movement, f"raw_traces/excerpt_traces/{status}/{i}_movement.json")
