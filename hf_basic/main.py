from transformers import pipeline

# Create a pipeline
pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")

# ChatML
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]

# Running the pipeline
pipe(text=messages)
