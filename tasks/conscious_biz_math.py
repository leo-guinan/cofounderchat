"""
Conscious-BizMath Task

Unit economics (LTV/CAC/payback) combined with Time Violence calculations.

Current: Uses validation data (20 examples subset)
Future: Will scale to 100K+ examples when data generation is complete
"""

from tasks.conscious_validation_data import VALIDATION_EXAMPLES


class ConsciousBizMath:
    """
    Conscious Business Math dataset.
    
    Teaches models to calculate traditional metrics (LTV, CAC, payback)
    PLUS Time Violence metrics (ΔTVH, vₜ, C-ROI*).
    
    Current implementation: Uses subset of validation data (10 examples)
    Future: Will be 100K+ generated examples
    """
    
    def __init__(self, split="train", stop=None):
        self.split = split
        
        # Filter for BizMath examples (first 10 in validation set)
        if split == "train":
            # TODO: Replace with full dataset when generated
            # For now, use BizMath examples from validation set
            all_examples = VALIDATION_EXAMPLES[:10]  # First 10 are BizMath
            self.data = all_examples if stop is None else all_examples[:stop]
        else:
            self.data = []  # No val split for now
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx % len(self.data)]  # Loop if we run out


if __name__ == "__main__":
    dataset = ConsciousBizMath(split="train")
    print(f"ConsciousBizMath dataset: {len(dataset)} examples")
    print(f"\nFirst example:")
    ex = dataset[0]
    print(f"  User: {ex['messages'][0]['content'][:100]}...")
    print(f"  Assistant: {ex['messages'][1]['content'][:200]}...")

