def crear_chunk(text, max_length= 300, overlap= 30):
    words= text.split()
    chunks =[]

    start= 0
    while start < len(words):
        end = start + max_length
        chunk = " ".join(words[start:end]) #Esta linea une las palabras desde start hasta end con espacios
        chunks.append(chunk)
        start = end - overlap

    return chunks