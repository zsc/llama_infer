# llama_infer
Inference script for Meta's LLaMA models using Hugging Face wrapper as in https://github.com/huggingface/transformers/pull/21955

||fp16|int8(bitsandbytes)|
|--|--|--|
|V100|OK, 5xV100|Bad results, short generated sequences|
|A100|Not tested, should be OK|OK, 3xA100|

## First install from source
```
git clone https://github.com/zphang/transformers.git --branch llama_push --depth=1
cd transformers
python3 setup.py develop --user
```
## Second convert the weights
```
python3 src/transformers/models/llama/convert_llama_weights_to_hf.py \
    --input_dir /path/to/downloaded/llama/weights \
    --model_size 7B \
    --output_dir /data/llama/hf/
```

Here we assume the converted weigths are in `/data/llama/hf/` .

## 7B model

### int8 (decent now after removing extra EOS)
```python3 test_llam.py --do_int8 --low_cpu_mem_usage --variant 7b --model_path /data/llama/hf/```

#### contrastive search
```
Puma is a 1996 film starring Jackie Chan and Leslie Cheung Kwok-wing.
The film's soundtrack was composed by Shigeru Umebayashi, who was nominated for the Golden Horse Award for Best Score at the 24th Golden Horse Awards.boldsquo;s first martial arts film in a decade, PUMA is a remake of the 1976 Shaw Brothers film Fist of Fury. Chan plays Chen Zhen, a Chinese student who travels to Japan to study karate. After being beaten by a group of yakuza, he vows to avenge his friend's death. The Japanese police are unable to stop him, and the yakuza send their best fighters to try to stop him.
Chen Zhen (Jackie Chan) is a Chinese student who has traveled to Japan to study karate. While on
```


### float16 (decent)
```python3 test_llam.py --low_cpu_mem_usage --variant 7b --model_path /data/llama/hf/```

#### contrastive search
```
Puma is a 1980’s classic that has stood the test of time. With its sleek design and sporty look, Puma is a shoe that can be worn with anything and everything.
The Puma Suede is a sneaker that was introduced in 1968 by Adi Dassler and his brother Rudi. The Suede’s design was inspired by the moccasin shoes that Native Americans wore in the 19th century. It was originally called Clyde Court, after Walt Clyde Frazier, a basketball player for the New York Knicks.\nThe first version of the Puma Suede was made of leather and had a rubber sole. Later, the design was changed to a canvas upper and a plastic wedge heel. This version was more popular and is the one that we know today.
Today, the Puma Suede is one of the most popular
```
