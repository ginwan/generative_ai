import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hey there, My name is Ginwan Elgasim"
# Tokens: [25216, 1354, 11, 3673, 1308, 382, 69322, 10091, 3241, 22970, 321]
tokens = enc.encode(text)
print(f"Tokens: {tokens}")

decoded = enc.decode([25216, 1354, 11, 3673, 1308, 382, 69322, 10091, 3241, 22970, 321])
print(f"Decoded: {decoded}")
