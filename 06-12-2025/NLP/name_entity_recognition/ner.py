from transformers import pipeline

ner = pipeline("ner", aggregation_strategy="simple")

with open("input.txt") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            outfile.write("\n")
            continue
        entities = ner(line)
        entity_texts = [e["word"] + f" ({e['entity_group']})" for e in entities]
        outfile.write(" | ".join(entity_texts) + "\n")