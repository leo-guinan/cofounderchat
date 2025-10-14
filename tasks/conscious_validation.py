"""
Conscious Economics Validation Task

Wrapper to integrate validation examples with cofounderchat's training infrastructure.
"""

from tasks.conscious_validation_data import VALIDATION_EXAMPLES


class ConsciousValidation:
    """
    Validation dataset for testing Conscious Economics pattern learning.
    
    20 carefully curated examples teaching:
    - Conscious-BizMath (10): LTV/CAC + Time Violence calculations
    - Experiment Cards (5): Hypothesis → Test → C-ROI workflow
    - Compliance Drills (5): Trust/evidence/constraint checking
    """
    
    def __init__(self, split="train"):
        self.split = split
        if split == "train":
            self.data = VALIDATION_EXAMPLES
        else:
            # No validation split for this tiny dataset
            self.data = []
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]


if __name__ == "__main__":
    # Test that the dataset loads
    dataset = ConsciousValidation(split="train")
    print(f"✓ Loaded {len(dataset)} examples")
    
    # Show first example
    example = dataset[0]
    print(f"\nFirst example:")
    print(f"  User: {example['messages'][0]['content'][:100]}...")
    print(f"  Assistant preview: {example['messages'][1]['content'][:200]}...")
    
    # Verify all examples have correct structure
    errors = []
    for i, ex in enumerate(dataset):
        if not isinstance(ex, dict):
            errors.append(f"Example {i}: not a dict")
        elif 'messages' not in ex:
            errors.append(f"Example {i}: missing 'messages' key")
        elif len(ex['messages']) != 2:
            errors.append(f"Example {i}: expected 2 messages, got {len(ex['messages'])}")
        elif ex['messages'][0]['role'] != 'user':
            errors.append(f"Example {i}: first message should be 'user'")
        elif ex['messages'][1]['role'] != 'assistant':
            errors.append(f"Example {i}: second message should be 'assistant'")
        else:
            # Check that assistant response includes conscious economics blocks
            content = ex['messages'][1]['content']
            if '<|assumptions|>' not in content and '<|tests|>' not in content and '<|compliance|>' not in content:
                errors.append(f"Example {i}: missing conscious economics blocks")
    
    if errors:
        print(f"\n❌ Found {len(errors)} errors:")
        for error in errors:
            print(f"  {error}")
    else:
        print(f"\n✓ All {len(dataset)} examples have correct structure")
        print(f"\nConscious economics blocks found:")
        
        block_counts = {
            '<|assumptions|>': 0,
            '<|risks|>': 0,
            '<|tests|>': 0,
            '<|time_violence|>': 0,
            '<|time_dividend|>': 0,
            '<|metrics|>': 0,
            '<|trust_evidence|>': 0,
            '<|compliance|>': 0,
        }
        
        for ex in dataset:
            content = ex['messages'][1]['content']
            for block in block_counts:
                if block in content:
                    block_counts[block] += 1
        
        for block, count in block_counts.items():
            print(f"  {block}: {count}/{len(dataset)} examples ({100*count//len(dataset)}%)")

