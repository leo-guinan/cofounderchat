"""
Experiment Cards Task

Hypothesis → Test → C-ROI workflow for founders.

Current: Uses validation data (5 examples)
Future: Will scale to 50K+ examples when data generation is complete
"""

from tasks.conscious_validation_data import VALIDATION_EXAMPLES


class ExperimentCards:
    """
    Experiment Card dataset.
    
    Teaches models the structured experiment design pattern:
    1. State assumptions
    2. Design falsifiable test (1-week timeline)
    3. Define success metrics
    4. Calculate C-ROI (revenue + time value)
    
    Current implementation: Uses subset of validation data (5 examples)
    Future: Will be 50K+ generated examples
    """
    
    def __init__(self, split="train", stop=None):
        self.split = split
        
        # Filter for Experiment Card examples (examples 10-14 in validation set)
        if split == "train":
            # TODO: Replace with full dataset when generated
            # For now, use Experiment Card examples from validation set
            all_examples = VALIDATION_EXAMPLES[10:15]  # Examples 10-14 are experiment cards
            self.data = all_examples if stop is None else all_examples[:stop]
        else:
            self.data = []  # No val split for now
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx % len(self.data)]  # Loop if we run out


if __name__ == "__main__":
    dataset = ExperimentCards(split="train")
    print(f"ExperimentCards dataset: {len(dataset)} examples")
    print(f"\nFirst example:")
    ex = dataset[0]
    print(f"  User: {ex['messages'][0]['content'][:100]}...")
    print(f"  Assistant has blocks: {', '.join([b for b in ['<|assumptions|>', '<|tests|>', '<|metrics|>'] if b in ex['messages'][1]['content']])}")

