# thought_record_bot_final.py (incorporating fine-tuned LLM)

import os
# from transformers import AutoModelForCausalLM, AutoTokenizer # For actual LLM integration

# --- CRISIS PROTOCOL CONFIGURATION (NON-NEGOTIABLE) ---
CRISIS_KEYWORDS = ["kill myself", "want to die", "ending it all", "suicide", "self-harm", "goodbye", "no point in living"]
CRISIS_HOTLINE_NUMBER = "988" # Or your local equivalent
CRISIS_TEXT_LINE = "HOME to 741741" # Or your local equivalent

class ThoughtRecordBot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = "START"
        self.data = {} # Stores the 7 columns of the thought record
        self.conversation_history = [] # To provide context to the LLM
        
        # --- Load Fine-Tuned LLM ---
        # This would load your fine-tuned model and tokenizer
        # self.llm_tokenizer = AutoTokenizer.from_pretrained("fine_tuned_mental_health_bot")
        # self.llm_model = AutoModelForCausalLM.from_pretrained("fine_tuned_mental_health_bot")
        # self.llm_model.eval() # Set to evaluation mode

        print("T-Bot initialized. Ready for interaction.")

    def get_response(self, user_input: str) -> str:
        # --- 1. CORE SAFETY PROTOCOL (RULE-BASED - FIRST EXECUTION) ---
        if self._check_for_crisis(user_input):
            return self._crisis_response()
            
        # --- 2. DIALOGUE LOGIC (HYBRID: RULES + LLM) ---
        response = ""
        
        # Add current user input to history
        self.conversation_history.append({"role": "user", "content": user_input})

        if self.state == "START":
            response = "Welcome. I'm T-Bot. Ready to work through a negative thought? (Yes/No)"
            self.state = "AWAIT_CONSENT"
            
        elif self.state == "AWAIT_CONSENT":
            if "yes" in user_input.lower():
                self.state = "GET_SITUATION"
                response = "Great. Let's start the Thought Record.\n\n**Column 1: Situation.** What happened? Where were you, and who was with you?"
            else:
                response = "No problem. Let me know when you're ready. (Type 'Start' to begin)."
                self.state = "START"

        # --- Column 1: Situation (Rules-based) ---
        elif self.state == "GET_SITUATION":
            self.data['situation'] = user_input
            self.state = "GET_EMOTION"
            response = "**Column 2: Emotion.** How did you feel? Choose an emotion and rate its intensity (0-100%). (e.g., Anxious 80)"

        # --- Column 2: Emotion (Rules-based with potential LLM parsing) ---
        elif self.state == "GET_EMOTION":
            self.data['emotion'] = user_input
            self.state = "GET_THOUGHT"
            response = "**Column 3: Automatic Thought.** What thought went through your mind *right before* you felt that emotion? What did you believe?"
            
        # --- Column 3: Automatic Thought (LLM-Enhanced) ---
        elif self.state == "GET_THOUGHT":
            self.data['thought'] = user_input
            self.state = "GET_EVIDENCE_FOR"
            
            # --- This is where the fine-tuned LLM generates a more nuanced response ---
            # Instead of a simple fixed response, it can acknowledge and validate the thought.
            context_for_llm = self._format_conversation_for_llm()
            llm_prompt = f"{context_for_llm}\n\n### Instruction:\nYour thought: '{user_input}'. Now, let's move to **Column 4: Evidence FOR.** What facts, evidence, or information supports this thought? Be honest.\n\n### Response:\n"
            
            # Simulated LLM call (replace with actual model inference)
            # llm_output = self._generate_llm_response(llm_prompt)
            # response = llm_output.split("### Response:\n")[-1].strip() # Extract response part

            # For demonstration, a mixed approach:
            response = f"I hear you. You're identifying the thought: '{user_input}'. " \
                       f"Now, let's explore that. **Column 4: Evidence FOR.** What facts, evidence, " \
                       f"or information supports this thought? Be honest."

        # ... (Remaining 4 columns would follow similar structured logic, potentially
        #      using the LLM for more empathetic or nuanced guiding questions)
        
        # --- 3. LOGGING AND HISTORY UPDATE ---
        self.conversation_history.append({"role": "assistant", "content": response})
        self._log_interaction(user_input, response)
        return response

    # -----------------------------------------------------
    # Helper Functions
    # -----------------------------------------------------

    def _check_for_crisis(self, text: str) -> bool:
        """1.1 Core Safety Protocol: Detects crisis indicators."""
        if any(keyword in text.lower() for keyword in CRISIS_KEYWORDS):
            return True
        # Future: Integrate a fine-tuned safety classifier LLM here for nuanced crisis detection
        return False
        
    def _crisis_response(self) -> str:
        """Immediate, life-saving response."""
        self.state = "CRISIS_HALTED"
        # Log to database for audit (including user_id, timestamp, crisis input)
        # In a real app, this might also trigger an alert to an internal monitoring system
        return (
            f"**STOP.** I am an AI and cannot handle a life-threatening crisis. "
            f"Your safety is paramount. **Please immediately call or text {CRISIS_HOTLINE_NUMBER}** "
            f"or text **{CRISIS_TEXT_LINE}** to connect with trained crisis counselors. "
            f"Alternatively, go to the nearest emergency room. "
            f"I will be here when you are safe, but please seek human help now."
        )

    def _log_interaction(self, user_input: str, bot_response: str):
        """Securely log the conversation for auditing and review."""
        # This is where database (e.g., PostgreSQL) insertion code would go,
        # ensuring user_input is encrypted, anonymized, and timestamped.
        # Example: insert into conversation_logs (user_id, timestamp, user_message, bot_message) values (...)
        pass

    def _format_conversation_for_llm(self) -> str:
        """Formats the conversation history into a prompt for the fine-tuned LLM."""
        formatted_history = []
        for turn in self.conversation_history:
            if turn["role"] == "user":
                formatted_history.append(f"User: {turn['content']}")
            elif turn["role"] == "assistant":
                formatted_history.append(f"Assistant: {turn['content']}")
        return "\n".join(formatted_history)

    def _generate_llm_response(self, prompt: str) -> str:
        """
        Simulates calling the fine-tuned LLM for a response.
        In a real scenario, this would involve tokenizing the prompt,
        running inference on self.llm_model, and decoding the output.
        """
        print(f"DEBUG: LLM generating response for prompt (first 100 chars): {prompt[:100]}...")
        # inputs = self.llm_tokenizer(prompt, return_tensors="pt").to(self.llm_model.device)
        # outputs = self.llm_model.generate(**inputs, max_new_tokens=200, temperature=0.7)
        # return self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return "Simulated LLM response based on context." # Placeholder

# --- Example of running the T-Bot ---
if __name__ == "__main__":
    bot = ThoughtRecordBot(user_id="test_user_123")
    print(bot.get_response("Hello"))
    print(bot.get_response("Yes"))
    print(bot.get_response("I had a disagreement with my boss this morning."))
    print(bot.get_response("Anxious 70"))
    print(bot.get_response("My boss thinks I'm incompetent."))
    print(bot.get_response("I want to die")) # Test crisis detection