import torch
import json
import argparse
import threading

from accelerate import init_empty_weights, infer_auto_device_map
import transformers
from transformers import AutoConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from transformers import StoppingCriteria, StoppingCriteriaList
from loguru import logger
from typing import List, Union


def get_device_map(model_name, device, do_int8):
    if device == "a100-40g":
        return "auto"

    with init_empty_weights():
        config = AutoConfig.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_config(config)

    d = {0: "18GiB"}
    for i in range(1, 6):
        d[i] = "26GiB"
    device_map = infer_auto_device_map(
        model, max_memory=d, dtype=torch.int8 if do_int8 else torch.float16, no_split_module_classes=["BloomBlock", "OPTDecoderLayer", "LLaMADecoderLayer"]
    )
    print(device_map)
    del model
    return device_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="/data/llama/hf/")
    parser.add_argument("--variant", type=str, default="65b", choices=["7b", "13b", "33b", "65b"])
    parser.add_argument(
        "--device", type=str, choices=["a100-40g", "v100-32g"], default="a100-40g"
    )
    parser.add_argument("--do_int8", action="store_true")
    parser.add_argument("--low_cpu_mem_usage", action="store_true")
    parser.add_argument("--port", type=int, default=12333)
    args = parser.parse_args()

    model_id = f"{args.model_path}{args.variant}/llama-{args.variant}"
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map=get_device_map(model_id, args.device, args.do_int8),
        torch_dtype=torch.int8 if args.do_int8 else torch.float16,
        low_cpu_mem_usage=args.low_cpu_mem_usage,
        load_in_8bit=args.do_int8,
    )
    tokenizer = AutoTokenizer.from_pretrained(f"{args.model_path}{args.variant}/tokenizer/", use_fast="/opt" not in model_id)
    #tokenizer.pad_token_id = -1

    generate_kwargs = {
        "max_new_tokens": 200,
        "min_new_tokens": 100,
        "temperature": 0.1,
        "do_sample": False, # The three options below used together leads to contrastive search
        "top_k": 4,
        "penalty_alpha": 0.6,
        #"no_repeat_ngram_size": no_repeat_ngram_size,
        #**generation_config,
    }
    prompt = "Puma is a "
    with torch.no_grad():
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        assert len(input_ids) == 1, len(input_ids)
        if input_ids[0][-1] == 2: # 2 is EOS, hack to remove. If the prompt is ending with EOS, often the generation will stop abruptly.
            input_ids = input_ids[:, :-1]
        input_ids = input_ids.to(0)
        #input_ids = tokenizer(prompt, padding=True, truncation=True, return_tensors="pt").input_ids.to(0)
        generated_ids = model.generate(
            input_ids,
            #stopping_criteria=stopping_criteria,
            **generate_kwargs
        )
        result = tokenizer.batch_decode(generated_ids.cpu(), skip_special_tokens=True)
        print(result)
        from IPython import embed; embed()


