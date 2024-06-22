# BotCreator by EdexCode
Easy chatbot development with Python. Create your own chatbots with just a few lines of code.
## How To Use?
### Syntax
#### Python
```python
import botcreator as bc

bc.filename = 'TXT_FILE_PATH'
prompt = input("Prompt: ")
print(bc.botresponse(prompt.lower()))
```
#### TXT File
```
hi#hello/Hi there!
```

### Symbols
#### 1. / - Separator or Divider:
#### Separates the expected prompt (or conditions) from the response. It divides the rule into two parts: what the bot should recognize or react to (left side) and how it should respond (right side).
#### Example:
```
hi/Hi there!
```
#### Here, 'hi' represents condition or expected input, and 'Hi there' represents response. The / separates the conditions from the responses.

#### 2. # - OR Operator:
#### Indicates multiple possible responses within a single rule. When used after a response, it signifies that the bot can randomly select one of the responses listed.
#### Example:
```
hi#hello#sup/Hi there#How can I help you
```
#### Here, The # symbol in the rule hi#hello#sup/Hi there#How can I help you separates multiple alternative inputs (hi, hello, sup), indicating that the bot should respond to any of these inputs with randomly chosen responses (Hi there or How can I help you).

#### 3. # - AND Operator:
#### Connects multiple conditions within the expected prompt. It indicates that all specified conditions must be present for the rule to trigger a response.
#### NOTE: Only works in expected prompt (or condition)
#### Example:
```
my&name&is/Nice to meet you!
```
#### Here, The & symbol in my&name&is/Nice to meet you! signifies that the bot expects all three words (my, name, is) to appear together in the user's input. When this condition is met, the bot will respond with Nice to meet you!.

## Example
#### words.txt
```
my&name&is/Nice to meet you!
hi#hello#sup/Hi there#How can i help you?
are&you&a&bot#your&a&chatbot/Yes
&help/How can i help you?
```
#### main.py
```python
import botcreator as bc

bc.filename = 'words.txt'
prompt = input("Prompt: ")
print(bc.botresponse(prompt.lower()))
```
### Outputs:
#### my&name&is/Nice to meet you!
```
Prompt: my name is edex
Nice to meet you!
```
#### hi/hello/sup/Hi there#How can i help you?
```
Prompt: hi
Hi there
```
```
Prompt: hello
How can i help you?
```
```
Prompt: sup
How can i help you?
```
#### are&you&a&bot#your&a&chatbot/Yes
```
Prompt: are you a bot?
Yes
```
```
Prompt: your a chatbot
Yes
```
#### &help/How can i help you?
```
Prompt: can you help me
How can i help you?
```
