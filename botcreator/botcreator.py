import random

def botresponse(prompt, filename):
    exact_matches = []
    condition_matches = []

    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            if '/' not in line:
                continue
            
            prompt_part, response_part = line.strip().split('/')
            responses = response_part.split('#')
            
            if '#' not in prompt_part and '&' not in prompt_part:
                exact_matches.append((prompt_part, responses))
            else:
                prompt_conditions = prompt_part.split('#')
                condition_matches.append((prompt_conditions, responses))
    
    for exact_prompt, responses in exact_matches:
        if exact_prompt == prompt:
            return random.choice(responses)
    
    for prompt_conditions, responses in condition_matches:
        for condition in prompt_conditions:
            sub_conditions = condition.split('&')
            if all(sub_condition.strip() in prompt for sub_condition in sub_conditions):
                return random.choice(responses)
    
    for exact_prompt, responses in exact_matches:
        if exact_prompt in prompt:
            return random.choice(responses)
    
    return None
