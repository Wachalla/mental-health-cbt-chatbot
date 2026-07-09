# synthetic_data_generator.py

import json
import os
import time
from typing import List, Dict

# --- Configuration for Synthetic Data Generation ---
# Replace with actual API key and endpoint for your chosen powerful LLM
LLM_API_KEY = os.getenv("YOUR_POWERFUL_LLM_API_KEY")
LLM_API_ENDPOINT = "https://api.your-llm-provider.com/generate" # Example endpoint

def call_powerful_llm_api(prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """
    Simulates an API call to a powerful foundational LLM (e.g., GPT-4, Claude).
    In a real implementation, this would use a library like 'openai', 'anthropic', etc.
    """
    # This is a placeholder for actual API integration.
    # For demonstration, we'll return a simulated response.
    print(f"Calling LLM with prompt (first 100 chars): {prompt[:100]}...")
    time.sleep(0.5) # Simulate API latency

    # In a real scenario, this would be an HTTP POST request to the LLM API
    # response = requests.post(LLM_API_ENDPOINT, headers={"Authorization": f"Bearer {LLM_API_KEY}"}, json={...})
    # return response.json()['choices'][0]['text']

    # Placeholder for actual LLM response
    return (
        "Therapist: It sounds like you're carrying a heavy burden. Can you tell me a bit more about "
        "what 'overwhelmed' feels like for you physically or emotionally? "
        "User: It's like a tight knot in my stomach and my chest feels heavy. "
        "I just can't seem to focus on anything. "
        "Therapist: That physical sensation can be really uncomfortable. "
        "When you notice that knot, what thoughts typically come to mind?"
    )

def generate_synthetic_dialogue(
    mental_health_issue: str,
    user_scenario: str,
    therapist_style: str,
    dialogue_length_turns: int = 5
) -> Dict:
    """
    Generates a synthetic therapeutic dialogue for a specific mental health issue.
    """
    system_prompt = (
        f"You are generating a therapeutic dialogue for a mental health chatbot. "
        f"The user is experiencing **{mental_health_issue}**. "
        f"The therapist should adopt a **{therapist_style}** approach, focusing on empathy, "
        "validation, and guiding the user towards insight or coping strategies. "
        "Generate a natural, multi-turn conversation between a 'Therapist' and a 'User'. "
        "Ensure the dialogue is realistic, safe, and clinically appropriate. "
        "Do NOT offer medical diagnoses or crisis advice. Keep the conversation focused "
        "on the specified issue and therapeutic style. "
        "Format the output as 'Therapist: [response]' and 'User: [response]'."
    )

    user_instruction = (
        f"Start a conversation where the User is describing a scenario related to {mental_health_issue}: "
        f"'{user_scenario}'. The dialogue should be approximately {dialogue_length_turns} turns long."
    )

    full_prompt = f"{system_prompt}\n\n{user_instruction}\n\nTherapist: Hello, thank you for sharing. How are you feeling today?"

    generated_text = call_powerful_llm_api(full_prompt, max_tokens=2048)

    # Post-process the generated text into a structured format for fine-tuning
    dialogue_turns = []
    current_speaker = None
    current_utterance = []

    for line in generated_text.split('\n'):
        if line.startswith("Therapist:"):
            if current_speaker == "User":
                dialogue_turns.append({"speaker": "User", "text": " ".join(current_utterance).strip()})
            current_speaker = "Therapist"
            current_utterance = [line[len("Therapist:"):].strip()]
        elif line.startswith("User:"):
            if current_speaker == "Therapist":
                dialogue_turns.append({"speaker": "Therapist", "text": " ".join(current_utterance).strip()})
            current_speaker = "User"
            current_utterance = [line[len("User:"):].strip()]
        elif current_speaker:
            current_utterance.append(line.strip())

    if current_speaker and current_utterance:
        dialogue_turns.append({"speaker": current_speaker, "text": " ".join(current_utterance).strip()})

    return {
        "issue": mental_health_issue,
        "scenario": user_scenario,
        "therapist_style": therapist_style,
        "dialogue": dialogue_turns
    }

def generate_datasets_for_issues(
    issues_and_scenarios: Dict[str, List[str]],
    therapist_styles: List[str],
    num_dialogues_per_scenario: int = 5,
    output_dir: str = "synthetic_data"
):
    """
    Orchestrates the generation of synthetic datasets for multiple mental health issues.
    """
    os.makedirs(output_dir, exist_ok=True)
    all_generated_data = []

    for issue, scenarios in issues_and_scenarios.items():
        print(f"\n--- Generating data for: {issue} ---")
        for scenario in scenarios:
            for style in therapist_styles:
                for i in range(num_dialogues_per_scenario):
                    print(f"  Generating dialogue {i+1} for scenario '{scenario[:30]}...' with style '{style}'")
                    dialogue_data = generate_synthetic_dialogue(issue, scenario, style)
                    all_generated_data.append(dialogue_data)

                    # Save each dialogue to a separate file for easier review/vetting
                    file_name = f"{issue.replace(' ', '_')}_{style.replace(' ', '_')}_{len(all_generated_data)}.json"
                    with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
                        json.dump(dialogue_data, f, ensure_ascii=False, indent=2)
                    time.sleep(1) # Be mindful of API rate limits

    # Optionally, save all generated data into one large JSON file
    with open(os.path.join(output_dir, "all_synthetic_mental_health_data.json"), 'w', encoding='utf-8') as f:
        json.dump(all_generated_data, f, ensure_ascii=False, indent=2)
    print(f"\nGenerated {len(all_generated_data)} synthetic dialogues in '{output_dir}'.")

# --- Example Usage ---
if __name__ == "__main__":
    mental_health_config = {
        "Anxiety": [
            "User feels overwhelmed by social situations and avoids gatherings.",
            "User experiences frequent worry about future events, impacting sleep.",
            "User has panic attacks when facing public speaking."
        ],
        "Depression": [
            "User reports low mood, lack of energy, and loss of interest in hobbies.",
            "User struggles with feelings of hopelessness and difficulty concentrating.",
            "User feels isolated and withdrawn from friends and family."
        ],
        # Add more mental health issues and varied scenarios here
    }

    therapeutic_styles = [
        "CBT-focused (Cognitive Behavioral Therapy)",
        "ACT-focused (Acceptance and Commitment Therapy)",
        "Validation and active listening",
        "Motivational Interviewing"
    ]

    # Run the data generation process
    generate_datasets_for_issues(
        issues_and_scenarios=mental_health_config,
        therapist_styles=therapeutic_styles,
        num_dialogues_per_scenario=3 # Generate 3 dialogues per scenario/style combination
    )