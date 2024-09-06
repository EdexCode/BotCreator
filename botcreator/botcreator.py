import random
from typing import Optional
from cachetools import TTLCache
from watchdog.observers import Observer
import os
import traceback
from watchdog.events import FileSystemEventHandler

class Bot():
    """
    A more optimized and better way to get bot responses.

    Methods:
        getResponse(prompt: str) -> Optional[str]:
            Optional[str]: 
                The response, Or None if a response cannot be made.

        load_data(filename: str) -> None:
            Loads data from the specified file. This method is automatically called when needed, so manually running it is generally not required.
    """

    class WatchDogHandler(FileSystemEventHandler):
        def __init__(self, botClass: type) -> None:
            super().__init__()
            self.botClass = botClass

        def on_modified(self, event):
            if not event.is_directory:
                self.botClass.load_data()

    def __init__(self, filename: str, CacheTTL: float=300, CacheSize: int=50, reload_onchange: bool=True) -> None:
        """
        Initializes the "Bot" class with the required data.

        Args:
            filename (str): The bot data file.
            CacheTTL (float): Time to live for response cache in seconds. Set to 0 for no cache (useful when you need instant updates).
            CacheSize (int): Maximum size for response cache. Ignored when CacheTTL is set to 0.
            reload_onchange (bool): Reload when the bot data file is updated (useful when you need updates without restarting your code).
            
        Returns:
            None
        """
        if os.path.sep not in filename:
            filename = "." + os.path.sep + filename
        self.filename = filename
        self.load_data()

        self.cache_enabled = False if CacheTTL == 0 else True
        if self.cache_enabled:
            # Initialize the cache with TTLCache.
            self.cache = TTLCache(CacheSize, CacheTTL)
        
        self.ShouldReload = reload_onchange
        if self.ShouldReload:
            # Set up a file system observer to reload data on changes.
            event_handler = self.WatchDogHandler(self)
            observer = Observer()
            observer.schedule(event_handler, os.path.dirname(filename), recursive=True)
            observer.start()

    def load_data(self) -> None:
        """
        Loads data from the specified file. This method is automatically called when needed, so manually running it is generally not required.

        Returns:
            None
        """
        with open(self.filename, 'r', encoding="utf-8", errors="replace") as f:
            self.data = f.readlines()

    def getResponse(self, prompt: str) -> Optional[str]:
        """
        Gets response using prompt, and filename (read documentation for more information).

        Args:
            prompt (str): The prompt.

        Returns:
            Optional[str]: The response, Or None if a response cannot be made.
        
        Examples:
            >>> bot = Bot(filename="path/to/my-data.txt")
            >>> bot.getResponse("Hello")
            "Hi there!"
        """
        try:
            # Check if the result is in cache.
            if self.cache_enabled and prompt in self.cache:
                return random.choice(self.cache[prompt])
            
            return_value: str = None
            
            exact_matches = []
            condition_matches = []

            # Process each line in self.data.
            for line in self.data:
                if '/' not in line or line.startswith('$#'):
                    continue
                
                prompt_part, response_part = line.strip().split('/')
                responses = response_part.split('#')
                
                if '#' not in prompt_part and '&' not in prompt_part:
                    exact_matches.append((prompt_part, responses))
                else:
                    prompt_conditions = prompt_part.split('#')
                    condition_matches.append((prompt_conditions, responses))
            
            # Check for exact matches first.
            for exact_prompt, responses in exact_matches:
                if exact_prompt == prompt:
                    return_value = random.choice(responses)
                    # Save in cache
                    if self.cache_enabled:
                        self.cache[prompt] = responses
            
            # Check for condition matches.
            for prompt_conditions, responses in condition_matches:
                for condition in prompt_conditions:
                    sub_conditions = condition.split('&')
                    if all(sub_condition.strip() in prompt for sub_condition in sub_conditions):
                        return_value = random.choice(responses)
                        # Save in cache
                        if self.cache_enabled:
                            self.cache[prompt] = responses
            
            # Check for partial matches.
            for exact_prompt, responses in exact_matches:
                if exact_prompt in prompt:
                    return_value = random.choice(responses)
                    # Save in cache
                    if self.cache_enabled:
                        self.cache[prompt] = responses

            return return_value
        except Exception as err:
            traceback.print_exc()
            print(err)

def botresponse(prompt: str, filename: str) -> Optional[str]:
    """
    Gets response using prompt, and filename (read documentation for more information).
    This function is super unoptimized compared to using the "Bot" class and is included solely for backward compatibility. For improved performance and functionality, use the "Bot" class instead.

    Args:
        prompt (str): The prompt.
        filename (str): The bot data file.

    Returns:
        Optional[str]: The response, Or None if a response cannot be made.
    
    Examples:
        >>> botresponse("Hello", "path/to/my-data.txt")
        "Hi there!"
    """
    exact_matches = []
    condition_matches = []

    with open(filename, 'r') as f:
        lines = f.readlines()

        # Process each line in the file.
        for line in lines:
            if '/' not in line or line.startswith('$#'):
                continue
            
            prompt_part, response_part = line.strip().split('/')
            responses = response_part.split('#')
            
            if '#' not in prompt_part and '&' not in prompt_part:
                exact_matches.append((prompt_part, responses))
            else:
                prompt_conditions = prompt_part.split('#')
                condition_matches.append((prompt_conditions, responses))
    
    # Check for exact matches first.
    for exact_prompt, responses in exact_matches:
        if exact_prompt == prompt:
            return random.choice(responses)
    
    # Check for condition matches.
    for prompt_conditions, responses in condition_matches:
        for condition in prompt_conditions:
            sub_conditions = condition.split('&')
            if all(sub_condition.strip() in prompt for sub_condition in sub_conditions):
                return random.choice(responses)
    
    # Check for partial matches.
    for exact_prompt, responses in exact_matches:
        if exact_prompt in prompt:
            return random.choice(responses)
    
    return None