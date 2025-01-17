# Aristotle Bot Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture) 
- [Features](#features)
- [Technical Implementation](#technical-implementation)
- [Installation & Setup](#installation--setup)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Overview
Aristotle Bot is an AI-powered chatbot that emulates the teaching style and philosophical approach of Aristotle. The bot engages users in Socratic dialogue, explores philosophical concepts, and provides insights while maintaining Aristotle's persona.

## System Architecture

### Core Components
- **Base Model**: LLaMA 3.3 70B
- **Framework**: phi
- **API Integration**: Groq Cloud API
- **Tools Integration**: DuckDuckGo, YFinance

### Dependencies
```python
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
```

## Features

### 1. Persona Implementation
- Aristotelian teaching methodology
- Socratic questioning approach
- Logical reasoning frameworks
- Integration of classical philosophical concepts

### 2. Conversation Management
- Context-aware responses
- Memory of conversation history
- Dynamic topic adaptation
- Error handling and retry mechanisms

### 3. Knowledge Integration
- Philosophy and ethics
- Logic and reasoning
- Scientific knowledge
- Current events (via DuckDuckGo)
- Financial data (via YFinance)

## Technical Implementation

### Agent Configuration
```python
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(), Symbol],
    instructions=[
        "Use tables to display data",
        "Use Symbol tool for company lookups"
    ],
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Always include sources",
        "Use tables to display data"
    ],
    show_tool_calls=True,
    markdown=True,
)
```

### Error Handling
```python
retry_attempts = 3
for attempt in range(retry_attempts):
    try:
        # Agent execution code
        break
    except Exception as e:
        print(f"API error: {e}, Retrying...")
        time.sleep(3)
```

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aristotle-bot.git
cd aristotle-bot
```

2. Install dependencies:
```bash
pip install phi-agent python-dotenv
```

3. Configure environment variables:
```bash
# .env file
GROQ_API_KEY=your_api_key_here
```

## Usage Examples

### Basic Interaction
```python
response = agent_team.print_response(
    "Share your thoughts on virtue ethics and its modern applications",
    stream=True
)
```

### Financial Analysis
```python
response = agent_team.print_response(
    "Analyze the financial prospects of Company X",
    stream=True
)
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
