# data_preprocessor.py

import json
from typing import List, Dict

def prepare_for_finetuning(input_json_path: str, output_jsonl_path: str):
    """
    Loads synthetic data and converts it into a format suitable for LLM fine-tuning.
    We'll use a simple instruction-response format for this example.
    """
    with open(input_json_path, 'r', encoding='utf-8') as f:
        synthetic_data = json.load(f)

    finetuning_examples = []

    for dialogue_entry in synthetic_data:
        dialogue = dialogue_entry["dialogue"]
        issue = dialogue_entry["issue"]
        scenario = dialogue_entry["scenario"]
        style = dialogue_entry["therapist_style"]

        # For each turn in the dialogue, create an instruction-response pair
        # This simulates a user's input and the expected AI's response
        for i in range(len(dialogue) - 1): # Exclude the last turn if it's not a pair
            current_turn = dialogue[i]
            next_turn = dialogue[i+1]

            # Ensure the structure is User -> Therapist -> User -> Therapist...
            if current_turn["speaker"] == "User" and next_turn["speaker"] == "Therapist":
                user_instruction = (
                    f"You are a mental health chatbot guiding a user through a discussion about {issue}. "
                    f"The user initially presented with: '{scenario}'. Respond in a {style} manner."
                    f"\n\nUser: {current_turn['text']}"
                )
                therapist_response = next_turn['text']

                finetuning_examples.append({
                    "instruction": user_instruction,
                    "response": therapist_response
                })
            # You could also include Therapist -> User prompts if you want the model to generate user-like responses
            # but for a chatbot, Therapist responses are usually the target.

    # Save in JSON Lines format, common for LLM fine-tuning
    with open(output_jsonl_path, 'w', encoding='utf-8') as f:
        for example in finetuning_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

    print(f"Prepared {len(finetuning_examples)} fine-tuning examples saved to '{output_jsonl_path}'.")

# --- Example Usage ---
if __name__ == "__main__":
    # Assuming 'all_synthetic_mental_health_data.json' was generated in Phase 1
    prepare_for_finetuning(
        input_json_path="synthetic_data/all_synthetic_mental_health_data.json",
        output_jsonl_path="finetuning_data/mental_health_dataset.jsonl"
    )
    print("Data preparation complete. Ready for LLM fine-tuning.")