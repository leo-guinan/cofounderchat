"""
Founder Time Violence Evaluation Task

Tests if the model can correctly calculate Time Violence metrics.

Evaluation format:
- Question: Scenario with parameters
- Expected: Correct TV calculation
- Scoring: Exact match on calculation (within tolerance)
"""

FOUNDER_TV_EVAL = [
    {
        "question": "Calculate Operational Time Violence: arrival rate 10 req/hr, service rate 12 req/hr, arrival variance 4, service variance 2, time horizon 8 hours.",
        "answer": "16.33",  # tv_ops(10, 12, 4, 2, 8) = 16.33
        "tolerance": 0.5,
        "metric": "ops_score"
    },
    {
        "question": "A support system has 15 hours of human time violence and 25 hours of total time violence. What is the Consciousness Index C(S)?",
        "answer": "0.40",  # conscious_index(15, 25) = 0.40 or 40%
        "tolerance": 0.05,
        "metric": "consciousness_index"
    },
    {
        "question": "Calculate Informational Time Violence: KL divergence 2.5, decision entropy 3.2, redundancy MI 1.1.",
        "answer": "6.8",  # tv_info(2.5, 3.2, 1.1) = 6.8
        "tolerance": 0.2,
        "metric": "info_score"
    },
    {
        "question": "If we save 100 hours of time violence, how many hours go to users using the default Time Dividend distribution?",
        "answer": "60",  # time_dividends(100) -> users get 60%
        "tolerance": 1.0,
        "metric": "time_dividend_users"
    },
    {
        "question": "Calculate shadow price value: 50 hours saved, shadow price $35/hour.",
        "answer": "1750",  # 50 * 35 = 1750
        "tolerance": 10,
        "metric": "time_value"
    },
    {
        "question": "System has ops TV of 12 hours and info TV of 8 hours. What is total TV?",
        "answer": "20",  # tv_total(12, 8) = 20
        "tolerance": 0.5,
        "metric": "tv_total"
    },
    {
        "question": "Conscious ROI: revenue $5000, hours saved 15, shadow price $35/hr. What is the time value component?",
        "answer": "525",  # 15 * 35 = 525
        "tolerance": 10,
        "metric": "time_value"
    },
    {
        "question": "If a system goes from 80% human time violence to 30% human time violence, by how much did the Consciousness Index improve?",
        "answer": "0.50",  # 0.70 - 0.20 = 0.50 improvement
        "tolerance": 0.05,
        "metric": "consciousness_delta"
    },
]


class FounderTVEval:
    """Time Violence calculation accuracy evaluation"""
    
    def __init__(self):
        self.data = FOUNDER_TV_EVAL
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def evaluate_response(self, question, response):
        """
        Check if response contains correct calculation.
        
        Returns: (is_correct, extracted_value)
        """
        import re
        
        # Find the test case
        test_case = None
        for item in self.data:
            if question in item['question']:
                test_case = item
                break
        
        if not test_case:
            return False, None
        
        # Extract numerical answer from response
        # Look for patterns like "16.33", "= 16.33", "16.33 hours", etc.
        numbers = re.findall(r'(\d+\.?\d*)', response)
        
        if not numbers:
            return False, None
        
        # Try to find answer close to expected
        expected = float(test_case['answer'])
        tolerance = test_case['tolerance']
        
        for num_str in numbers:
            try:
                value = float(num_str)
                if abs(value - expected) <= tolerance:
                    return True, value
            except:
                continue
        
        return False, None


if __name__ == "__main__":
    eval_task = FounderTVEval()
    print(f"Founder Time Violence Eval: {len(eval_task)} questions")
    print(f"\nSample questions:")
    for i, item in enumerate(eval_task.data[:3]):
        print(f"\n{i+1}. {item['question']}")
        print(f"   Expected: {item['answer']} (±{item['tolerance']})")
        print(f"   Metric: {item['metric']}")

