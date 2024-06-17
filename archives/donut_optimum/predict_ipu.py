import re

from transformers import DonutProcessor, AutoTokenizer
from optimum.onnxruntime import ORTModelForVision2Seq
from datasets import load_dataset
from PIL import Image

# Load processor, tokenizer
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
tokenizer = AutoTokenizer.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

#Config file path
config_file_path = "Path\\to\\vaip_config.json"
aie_options = onnxruntime.SessionOptions()

#Run on IPU
model = ORTModelForVision2Seq.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2", 
                                              export=True, 
                                              provider="VitisAIExecutionProvider", 
                                              session_option = aie_options,
                                              provider_options = [{'config_file': config_file_path}]       
                                              )

#save as .onnx
save_directory = "C:\\Users\\EndUser\\Desktop\\repos\\vegi\\donut_optimum\\models"
model.save_pretrained(save_directory)
# tokenizer.save_pretrained(save_directory)

# Load document image
dataset = load_dataset("hf-internal-testing/example-documents", split="test")
# image = Image.fromarray(dataset[2]["image"])
image = dataset[2]["image"]

# Prepare decoder inputs
task_prompt = "<s_cord-v2>"
decoder_input_ids = tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

# Preprocess the image
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generate output using ORTModel (Assuming use_cache and other parameters are supported by ORTModelForVision2Seq)
outputs = model.generate(
    pixel_values=pixel_values,
    decoder_input_ids=decoder_input_ids,
    # max_length=model.decoder.config.max_position_embeddings,
    max_length=512,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
    use_cache=True,
    bad_words_ids=[[tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

# Decode the output
sequence = tokenizer.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(tokenizer.eos_token, "").replace(tokenizer.pad_token, "")
sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
print(processor.token2json(sequence))
