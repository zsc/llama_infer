# llama_infer
Inference script for Meta's LLaMA models using Hugging Face wrapper

# 7B model
## int8 (seems bad)
### contrastive search
'Puma is a multicolored cat. He has a white face, paws, chest, belly and tail tip. He has green eyes.\nPuma\'s favorite food is tuna.\nRetrieved from "http://thelittlestpetshop.wikia.com/wiki/Puma?oldid=4113"UIVie
w.h" -- Cached in L2 cache -- References recursive data (as author) View all revisions Login/Create account New page: Create a new page on this wiki. Go to Special:NewPage and fill in the form. This will create a n
ew page called "New page name" (or something similar). You can add a link to this page by typing [[New page name]] in any page, and clicking "Show preview" or "Save page".\nThe Little Pet Shop Wiki is a FANDOM TV C
ommunity.'

## float16 (decent)
### contrastive search
'Puma is a multicolored cat. He is about 1 year old (DOB 1/1/18). His color is black and white with red tabby markings. He was found in the parking lot of a Walmart in Tucson, AZ.\nPuma’s owner is a woman named Sh
aron. She has had Puma since he was a kitten. Sharon’s boyfriend was the one who found Puma in the parking lot. He had been missing for a few days and they were worried about him.\nThe first time I met Puma was at 
the Humane Society of Southern Arizona. He was very scared and hid behind a cage. It took a while to get him to come out of his hiding place. I was able to pet him and he purred, but he was not comfortable with bei
ng petted.\nWhen I went to pick him up, he was in a carrier with a l'
