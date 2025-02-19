import os
import sys
import tempfile
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import torch.multiprocessing as mp
from utils import LlamaForCausalLM
from torch.nn.parallel import DistributedDataParallel as DDP
from transformers import GPT2TokenizerFast, AutoTokenizer

from utils import ToyLlama
import torch
from datasets import load_dataset


def setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"

    # initialize the process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)


def cleanup():
    dist.destroy_process_group()


def demo_basic(rank, world_size):
    print(f"Running basic DDP example on rank {rank}.")
    setup(rank, world_size)
    prefill_length = 500
    batchsize = 40
    genearte_length = 50
    iteration = 5
    model = ToyLlama(4096, 4096, 8192, 16).to(rank)
    # 200/102s
    input_ids = torch.rand(batchsize, prefill_length, 4096).to(rank)
    with torch.no_grad():
        import time

        start = time.time()
        if rank == 0:
            for i in range(iteration):
                print("rank 0, iteration", i)
                input_ids = torch.rand(batchsize, prefill_length, 4096).to(rank)
                for j in range(genearte_length):
                    if j != 0:

                        dist.recv(tensor=input_ids, src=1)

                    if j == 0:
                        kvcache = None
                        input_ids, kvcache = model.forward(input_ids, kvcache)
                    else:
                        input_ids, kvcache = model.forward(input_ids, kvcache)
                    dist.isend(tensor=input_ids, dst=1)
                    if j == 0:
                        input_ids = (
                            input_ids[:, -1, :].reshape(batchsize, 1, 4096).contiguous()
                        )
        elif rank == 1:
            for i in range(iteration):
                print("rank 1, iteration", i)
                input_ids = torch.rand(batchsize, prefill_length, 4096).to(rank)
                for j in range(genearte_length):
                    dist.recv(tensor=input_ids, src=0)
                    if j == 0:
                        kvcache = None
                        input_ids, kvcache = model.forward(input_ids, kvcache)
                    else:
                        input_ids, kvcache = model.forward(input_ids, kvcache)
                    if j == 0:
                        input_ids = (
                            input_ids[:, -1, :].reshape(batchsize, 1, 4096).contiguous()
                        )
                    if j != genearte_length - 1:
                        dist.isend(tensor=input_ids, dst=0)

        torch.cuda.synchronize()
        end = time.time()
        print(end - start)
    peak_memory = torch.cuda.max_memory_allocated(device="cuda:" + str(rank)) / (
        1024**2
    )  # 转换为MB单位

    print(f"Peak memory usage on GPU: {peak_memory} MB")
    cleanup()


def run_demo(demo_fn, world_size):
    mp.spawn(demo_fn, args=(world_size,), nprocs=world_size, join=True)


if __name__ == "__main__":
    n_gpus = torch.cuda.device_count()
    torch.cuda.manual_seed_all(2345)
    assert n_gpus >= 2, f"Requires at least 2 GPUs to run, but got {n_gpus}"
    world_size = n_gpus
    run_demo(demo_basic, world_size)
