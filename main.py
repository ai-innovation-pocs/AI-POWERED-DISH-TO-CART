import tiktoken

encode = tiktoken.get_encoding("gpt2")

text = "My Name is Sunny and Yours?"
tokens = encode.encode(text)
print(tokens)