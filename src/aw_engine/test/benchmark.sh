#!/bin/bash

# Configuration
NUM_GPUS=("1" "2" "4" "8")
NUM_AGENTS=("25" "200" "500" "2000")
MODE=("async", "sync")
PRIORITY=("true" "false")
SESSION_NAME="bench"
SERVER_PANE_ID="1"
SIMULATION_PANE_ID="2"
MODEL_PATH="meta-llama/Meta-Llama-3-8B-Instruct"
PORT="30000"

# Function to launch the serving engine
launch_server() {
  local num_gpus=$1
  echo "Launching serving engine with $num_gpus GPUs..."
  tmux send-keys -t "${SESSION_NAME}.${SERVER_PANE_ID}" \
    "HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN} python3 -m sglang.launch_server --model-path ${MODEL_PATH} --port ${PORT} --disable-radix-cache --num-workers ${num_gpus}" C-m
  sleep 60
}

# Function to run the simulation
run_simulation() {
  local num_agents=$1
  local mode=$2
  local priority=$3
  local priority_flag=""
  if [ "$priority" == "true" ]; then
    priority_flag="--priority"
  fi
  echo "Running simulation for NUM_GPUs=${gpu} and NUM_AGENTS=${agents} with mode=${mode}..."
  tmux send-keys -t "${SESSION_NAME}.${SIMULATION_PANE_ID}" \
    "python simulation.py --num-agents ${num_agents} --mode ${mode} --cache ${priority_flag} | tee -a simulation.log; tmux wait-for -S simulation_done" C-m
  tmux wait-for simulation_done
}

# Function to collect data
collect_data() {
  local gpu=$1
  local agents=$2
  local mode=$3
  local priority=$4
  local output_dir="Llama-3-8B-Instruct-${gpu}-${agents}-${mode}-${priority}"
  echo "Collecting data..."
  python dump_redis.py "${output_dir}"
  mv ../generative_agents_simple/instrumentation_trace.csv "${output_dir}/"
}

# Main script
for gpu in "${NUM_GPUS[@]}"; do
  launch_server "${gpu}"

  for agents in "${NUM_AGENTS[@]}"; do
    for mode in "${MODE[@]}"; do
      for priority in "${PRIORITY[@]}"; do
        tmux wait-for -U simulation_done
        python dump_redis.py reuse
        run_simulation "${agents}" "${mode}" "${priority}"
        collect_data "${gpu}" "${agents}" "${mode}" "${priority}"
        echo "Completed run for NUM_GPUs=${gpu}, NUM_AGENTS=${agents}, mode=${mode}, priority=${priority}"
      done
    done
  done

  tmux send-keys -t "${SESSION_NAME}.${SERVER_PANE_ID}" C-c
  sleep 10
done

echo "All experiments completed."
