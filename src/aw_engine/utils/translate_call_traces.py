import time
import json
import pandas as pd
import matplotlib.pyplot as plt

TRACES = {}
TRACE_DELIMITER = "__TRACE__"
BASE_TIMESTAMP = 0xFFFFFFFF

agent_dict = {
    "Latoya Williams": 0,
    "Rajiv Patel": 1,
    "Abigail Chen": 2,
    "Francisco Lopez": 3,
    "Hailey Johnson": 4,
    "Arthur Burton": 5,
    "Ryan Park": 6,
    "Isabella Rodriguez": 7,
    "Giorgio Rossi": 8,
    "Carlos Gomez": 9,
    "Klaus Mueller": 10,
    "Maria Lopez": 11,
    "Ayesha Khan": 12,
    "Wolfgang Schulz": 13,
    "Mei Lin": 14,
    "John Lin": 15,
    "Eddy Lin": 16,
    "Tom Moreno": 17,
    "Jane Moreno": 18,
    "Tamara Taylor": 19,
    "Carmen Ortiz": 20,
    "Sam Moore": 21,
    "Jennifer Moore": 22,
    "Yuriko Yamamoto": 23,
    "Adam Smith": 24,
}


def instrumentation_calibrate():
    TRACES.clear()
    global BASE_TIMESTAMP
    BASE_TIMESTAMP = time.time()


def trace_point(key, func, time_start, time_end):
    info_tuple = (func, time_start, time_end)
    if key not in TRACES:
        TRACES[key] = [info_tuple]
    else:
        TRACES[key].append(info_tuple)


# def get_step_time_mapping(env_traces):
#     start_time = 0xffffffff
#     end_time = 0
#     agent_dict = {}
#     steps = {360 * i: 0xffffffff for i in range(24)}
#     for key, value_str in env_traces.items():
#         if "action:" in key:
#             value = json.loads(value_str)
#             assert value["type"] == "AgentMove"
#             persona = value["persona"]
#             if persona not in agent_dict:
#                 agent_dict[persona] = {}
#             effective_time = value["effective_time"]
#             start_time = min(start_time, effective_time)
#             end_time = max(end_time, effective_time)
#             async_step = int(value["step"])
#             base_step = int(key.split(":")[-1])
#             assert async_step - base_step == 1
#             if base_step in steps:
#                 steps[base_step] = min(steps[base_step], effective_time)
#             assert async_step not in agent_dict[persona]
#             agent_dict[persona][async_step] = effective_time
#     for p in agent_dict:
#         for s in agent_dict[p]:
#             agent_dict[p][s] -= start_time
#     for s in steps:
#         steps[s] -= start_time

#     intervals = [steps[i * 360] for i in range(24)] + [end_time - start_time]
#     print(intervals)
#     return intervals


def translate_traces(filename):
    BASE_TIMESTAMP = 0xFFFFFFFF

    traces_list = []
    with open(filename, "r") as f:
        traces = json.load(f)
    for key, _trace in traces.items():
        agent = key.split(":")[0]
        trace = [json.loads(t) for t in _trace.split(TRACE_DELIMITER)]
        # print(agent, trace)
        # trace = json.loads(trace)
        for t in trace:
            BASE_TIMESTAMP = min(BASE_TIMESTAMP, t["start_time"])

    time_spans = []
    for key, _trace in traces.items():
        agent = key.split(":")[0]
        agent = agent.split("_")[0]
        trace = [json.loads(t) for t in _trace.split(TRACE_DELIMITER)]
        for t in trace:
            event = {
                "name": t["label"] if "label" in t["config"] else "NA",
                "ph": "X",
                "ts": (t["start_time"] - BASE_TIMESTAMP) * 1e6,
                "dur": t["duration"] * 1e6,
                "pid": 1,
                "tid": agent_dict[agent] if agent in agent_dict else 99
            }
            traces_list.append(event)
            time_spans.append((event["ts"], event["ts"] + event["dur"]))
    with open("translated_" + "_".join(filename.split("/")), "w") as fout:
        json.dump(traces_list, fout, indent=4)

    df = pd.DataFrame(time_spans, columns=["start", "end"])
    df["start"] = df["start"] / 1e6
    df["end"] = df["end"] / 1e6
    timeline = pd.concat(
        [pd.DataFrame({
            'time': df['start'],
            'change': 1
        }), pd.DataFrame({
            'time': df['end'],
            'change': -1
        })])

    # Sort by time
    timeline = timeline.sort_values('time').reset_index(drop=True)

    # Calculate the number of active instances over time
    timeline['outstanding_requests'] = timeline['change'].cumsum()
    if timeline.time.empty:
        return 0
    else:
        duration = max(timeline.time)
    average_active_instances = sum([
        timeline['outstanding_requests'][i - 1] * (timeline['time'][i] - timeline['time'][i - 1])
        for i in range(1, len(timeline['outstanding_requests']))
    ]) / duration

    # for i in range(len(intervals) - 1):
    #     t, t_ = intervals[i], intervals[i + 1]
    #     duration = t_ - t
    #     factor = 0
    #     for j in range(1, len(timeline['outstanding_requests'])):
    #         if timeline['time'][j] <= t_ and timeline['time'][j - 1] >= t:
    #             factor += timeline['outstanding_requests'][j - 1] * (timeline['time'][j] - timeline['time'][j - 1])
    #         if timeline['time'][j] > t_:
    #             break
    #     average_parallelism = factor / duration
    #     print(f"Average parallelism for interval {i}: {average_parallelism}")

    # Plot
    plt.figure(figsize=(20, 10))
    plt.step(timeline['time'], timeline['outstanding_requests'], where='post')
    plt.axhline(y=average_active_instances, color='r', linestyle='--', label=f'Average: {average_active_instances}')
    # for i in intervals:
    #     plt.axvline(x=i, color='g', linestyle='--')

    plt.xlabel('Execution Time (s)')
    plt.ylabel('# Outstanding Requests')
    plt.title('# Outstanding Requests During Execution')
    plt.grid(True)
    plt.legend()
    plt.savefig("_".join(filename.split("/")) + "_outstanding_requests.png")
    # plt.show()

    # print(f"durations: {duration}")
    return duration


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python translate_call_traces.py traces")
        sys.exit(1)
    trace_file = sys.argv[1]
    translate_traces(trace_file)
