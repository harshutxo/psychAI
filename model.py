import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class TextGenerator:
    def __init__(self, model_name='gpt2'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(self.device)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.resize_token_embeddings(len(self.tokenizer))

    def train_model(self, train_file_path, output_dir="./model_output"):
        # Prepare the dataset
        train_dataset = TextDataset(
            tokenizer=self.tokenizer,
            file_path=train_file_path,
            block_size=128
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        # Set up training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            save_steps=10_000,
            save_total_limit=2,
            learning_rate=5e-5,
            warmup_steps=1000,
            logging_dir='./logs',
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
        )

        # Train the model
        trainer.train()

        # Save the model
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

    def generate_text(self, seed_text, max_length=100):
        input_ids = self.tokenizer.encode(seed_text, return_tensors='pt', add_special_tokens=True).to(self.device)
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=self.device)
        
        output = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

if __name__ == "__main__":
    # Create a therapy conversation dataset
    therapy_conversations = """
    Therapist: Hello, how are you feeling today?
    Client: I've been feeling really anxious lately.
    Therapist: I'm sorry to hear that you're feeling anxious. Can you tell me more about what's been causing your anxiety?
    Client: I have a big presentation at work next week, and I'm worried I'll mess it up.
    Therapist: It's understandable to feel nervous about an important presentation. Let's talk about some strategies to help manage your anxiety and prepare for the presentation.
    Client: That would be helpful, thank you.
    Therapist: First, let's focus on your thoughts. Are you having any specific worries or negative thoughts about the presentation?
    Client: I keep thinking that I'll forget what to say or that people will think I'm not competent.
    Therapist: Those are common concerns. Let's work on reframing those thoughts. Instead of focusing on what might go wrong, try to think about your preparation and past successes. Can you recall a time when you did well in a similar situation?
    Client: Well, I did give a smaller presentation last month, and it went pretty well.
    Therapist: That's great! Let's build on that success. What did you do to prepare for that presentation that worked well?
    Client: I practiced a lot and made sure I knew my material inside and out.
    Therapist: Excellent. We can use those same strategies for this presentation. Let's also add some relaxation techniques to help manage your anxiety. Have you ever tried deep breathing exercises?
    Client: No, I haven't.
    Therapist: Deep breathing can be very effective in reducing anxiety. Let's practice a simple technique right now. Take a slow, deep breath in through your nose for 4 counts, hold it for 4 counts, then exhale slowly through your mouth for 6 counts. Let's try it together.
    Client: Okay, that does feel calming.
    Therapist: Great! Practice this technique regularly, especially when you feel anxious about your presentation. Remember, it's normal to feel some nervousness, but you have the skills and experience to do well. Shall we discuss some more strategies to help you prepare and feel confident?
    Client: Yes, please. That would be very helpful.
    """

    # Save the therapy conversations to a file
    with open("therapy_dataset.txt", "w") as f:
        f.write(therapy_conversations)

    # Train the model on the therapy dataset
    text_gen = TextGenerator()
    text_gen.train_model("therapy_dataset.txt")

    # Generate some text based on a prompt
    generated_text = text_gen.generate_text("Therapist: How can I help you today?", 100)
    print(generated_text)
