"""
Compliance Drills Task

Trust, evidence, and constraint checking for responsible AI co-founder.

Current: Uses validation data (5 examples)
Future: Will scale to 20K+ examples when data generation is complete
"""

from tasks.conscious_validation_data import VALIDATION_EXAMPLES


class ComplianceDrills:
    """
    Compliance Drill dataset.
    
    Teaches models to:
    1. Demand evidence for claims (trust factor T)
    2. Check constraint compliance (X factor)
    3. Flag legal/ethical risks
    4. Propose falsifiable tests instead of assertions
    
    Current implementation: Uses subset of validation data (5 examples)
    Future: Will be 20K+ generated examples
    """
    
    def __init__(self, split="train", stop=None):
        self.split = split
        
        # Filter for Compliance Drill examples (examples 15-19 in validation set)
        if split == "train":
            # TODO: Replace with full dataset when generated
            # For now, use Compliance examples from validation set
            all_examples = VALIDATION_EXAMPLES[15:20]  # Examples 15-19 are compliance drills
            self.data = all_examples if stop is None else all_examples[:stop]
        else:
            self.data = []  # No val split for now
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx % len(self.data)]  # Loop if we run out


if __name__ == "__main__":
    dataset = ComplianceDrills(split="train")
    print(f"ComplianceDrills dataset: {len(dataset)} examples")
    print(f"\nFirst example:")
    ex = dataset[0]
    print(f"  User: {ex['messages'][0]['content'][:100]}...")
    compliance_blocks = ['<|trust_evidence|>', '<|compliance|>', '<|risks|>']
    found = [b for b in compliance_blocks if b in ex['messages'][1]['content']]
    print(f"  Compliance blocks: {', '.join(found)}")

