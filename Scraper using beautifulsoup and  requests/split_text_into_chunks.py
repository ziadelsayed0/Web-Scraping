import pandas as pd

def split_text_into_chunks(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    chunks = []
    chunk = []
    for line in lines:
        if line.strip():  # Check if line is not empty
            chunk.append(line.strip())
        elif chunk:  # If chunk is not empty
            chunks.append(chunk)
            chunk = []

    # Append the last chunk if it exists
    if chunk:
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    filename = "storesInput.txt"
    chunks = split_text_into_chunks(filename)

    # Save chunks to Excel
    max_lines = max(len(chunk) for chunk in chunks)
    chunk_columns = {f"Line {i+1}": [] for i in range(max_lines)}
    for chunk in chunks:
        for i, line in enumerate(chunk):
            chunk_columns[f"Line {i+1}"].append(line)
        # Fill empty lines if needed
        for i in range(len(chunk), max_lines):
            chunk_columns[f"Line {i+1}"].append("")

    df = pd.DataFrame(chunk_columns)
    df.to_excel('chunks.xlsx', index=False)
    print("Chunks saved to 'chunks.xlsx' successfully!")
