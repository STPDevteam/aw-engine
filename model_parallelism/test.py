import torch
from transformers.models.llama import LlamaForCausalLM
from utils import LlamaForCausalLM

model_kwargs = {}
model_kwargs["torch_dtype"] = torch.float16
model_kwargs["device_map"] = "cuda:0"
model_kwargs["cache_dir"] = "../../cache"
model_id = "meta-llama/Llama-2-7b-chat-hf"
model = LlamaForCausalLM.from_pretrained(
    model_id,
    **model_kwargs,
    trust_remote_code=True,
)
import time

start = time.time()
for i in range(10):
    input_ids = torch.randint(0, 30000, (8, 200), dtype=torch.long).to("cuda:0")
    model.generate(input_ids, do_sample=True, max_length=300, num_return_sequences=1)
torch.cuda.synchronize()
end = time.time()
print(end - start)
peak_memory = torch.cuda.max_memory_allocated(device="cuda") / (1024**2)  # 转换为MB单位

print(f"Peak memory usage on GPU: {peak_memory} MB")
