from transformers import pipeline
import json
from collections import defaultdict

# Load the NER pipeline (uses a good default model like dbmdz/bert-large-cased-finetuned-conll03-english)
ner = pipeline("ner", aggregation_strategy="simple")  # "simple" groups subwords into full entities

input_file = "input.txt"
output_file = "entities_output.txt"
output_json = "entities_detailed.json"  # optional: save full details

# Container to hold all results
all_entities = []
line_entities_summary = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue  # skip empty lines

    # Run NER on the line
    entities = ner(line)

    # Collect clean entities (without scores if you don't want them)
    clean_entities = [
        {
            "text": ent["word"],
            "label": ent["entity_group"],
            "score": round(ent["score"], 4),
            "start": ent["start"],
            "end": ent["end"]
        }
        for ent in entities
    ]

    all_entities.extend(clean_entities)

    # Summary per line (optional)
    summary = f"Line {i+1}: " + " | ".join([f"{e['text']} ({e['label']})" for e in clean_entities])
    line_entities_summary.append(summary if clean_entities else f"Line {i+1}: No entities found")

# Write simple readable output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(line_entities_summary))

# Optional: Save full structured data as JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(all_entities, f, indent=2, ensure_ascii=False)

print(f"NER completed! Results saved to {output_file} and {output_json}")