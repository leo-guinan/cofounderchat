"""
Time Dividend Accounting Evaluation Task

Tests if the model correctly distributes Time Dividends across stakeholders.

Evaluation format:
- Question: Hours saved scenario
- Expected: Correct distribution (users 60%, navigators 20%, company 20%)
- Scoring: Check if all stakeholders mentioned with correct proportions
"""

TD_ACCOUNTING_EVAL = [
    {
        "question": "We saved 100 hours. Show the Time Dividend distribution.",
        "expected": {
            "users": 60.0,
            "navigators": 20.0,
            "company": 20.0
        },
        "tolerance": 2.0
    },
    {
        "question": "Project eliminated 50 hours of Time Violence per week. How should Time Dividends be distributed?",
        "expected": {
            "users": 30.0,
            "navigators": 10.0,
            "company": 10.0
        },
        "tolerance": 2.0
    },
    {
        "question": "Automation saves 200 hours per month. Calculate Time Dividend allocation for each stakeholder.",
        "expected": {
            "users": 120.0,
            "navigators": 40.0,
            "company": 40.0
        },
        "tolerance": 5.0
    },
    {
        "question": "Time savings: 75 hours. What portion goes to users?",
        "expected": {
            "users": 45.0,
        },
        "tolerance": 3.0
    },
    {
        "question": "Calculate full TD breakdown for 150 hours saved using standard distribution.",
        "expected": {
            "users": 90.0,
            "navigators": 30.0,
            "company": 30.0
        },
        "tolerance": 5.0
    },
]


class TDAccountingEval:
    """Time Dividend accounting evaluation"""
    
    def __init__(self):
        self.data = TD_ACCOUNTING_EVAL
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def evaluate_response(self, question, response):
        """
        Check if response has correct TD distribution.
        
        Returns: (is_correct, score)
        """
        import re
        
        # Find the test case
        test_case = None
        for item in self.data:
            if any(word in question.lower() for word in item['question'].lower().split()[:5]):
                test_case = item
                break
        
        if not test_case:
            return False, 0.0
        
        # Extract hours for each stakeholder
        # Look for patterns like "Users: 60h" or "Navigators: 20 hours" or "users = 60"
        patterns = {
            'users': r'users?\s*[:=]\s*(\d+\.?\d*)',
            'navigators': r'navigators?\s*[:=]\s*(\d+\.?\d*)',
            'company': r'company\s*[:=]\s*(\d+\.?\d*)',
        }
        
        extracted = {}
        for stakeholder, pattern in patterns.items():
            match = re.search(pattern, response.lower())
            if match:
                extracted[stakeholder] = float(match.group(1))
        
        # Score: count how many stakeholders match
        expected = test_case['expected']
        tolerance = test_case['tolerance']
        
        correct = 0
        total = len(expected)
        
        for stakeholder, expected_value in expected.items():
            if stakeholder in extracted:
                if abs(extracted[stakeholder] - expected_value) <= tolerance:
                    correct += 1
        
        score = correct / total
        is_correct = score >= 0.8  # 80% threshold
        
        return is_correct, score


if __name__ == "__main__":
    eval_task = TDAccountingEval()
    print(f"Time Dividend Accounting Eval: {len(eval_task)} questions")
    print(f"\nSample questions:")
    for i, item in enumerate(eval_task.data[:3]):
        print(f"\n{i+1}. {item['question']}")
        print(f"   Expected: {item['expected']}")

