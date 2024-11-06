## App purpose
This Plotly Dash application integrates AI-driven functionality and interactive visualizations to analyze global arms trade and military expenditure by country. The data originates from the Stockholm International Peace Research Institute (SIPRI) databases, specifically the
[SIPRI Arms Transfers Database](https://www.sipri.org/databases/armstransfers)
[SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)
<br>
The application includes an AI-powered assistant with memory capabilities, designed to enhance the user experience by dynamically adapting dashboard content based on user queries and interests. Each agent action is documented with concise descriptions (up to 150 words) in a dedicated panel within the application. Additionally, the assistant supports Retrieval-Augmented Generation (RAG) by leveraging both web and embedded data, providing a comprehensive user learning experience. Users have the option to download their full chat history for later reference.

#### Current App Sections Implemented:

1. **Input Panel**: 
   - Allows users to submit queries.
   - Supports options to end the conversation and export the chat history.

2. **Output Panel**: 
   - Displays a brief summary of agent actions.
   - Presents generated outputs based on user queries.

3. **Main Panel**:
   - Shows the requested dashboard section, including visualizations and data insights.

   - **Countries Military Expenditures**:
     - Displays annual military expenditures per country in constant 2022 USD and as a share of GDP.
     - **Available Visualizations**:
       - Animated map illustrating the evolution of selected metrics over time.
       - Interactive line chart for comparing expenditure trends across countries.

   - **Country Military Trade and Value Flow**:
     - Focuses on arms trade, emphasizing value flow from recipients to suppliers.
     - Data is grouped by year and limited to the top 10 trading countries.
     - **Available Visualizations**:
       - Sankey plot representing value flows from arms recipients to suppliers.
       - Summary table using Dash AG-Grid for additional details.
   

markdown
Copia codice
#### Agent Implementation

Implementation of a `LangGraph` ReAct agent executor using the `create_react_agent` function. This structure facilitates efficient management of agent cycles, tracking the scratchpad as messages within the agent’s state. System instructions are embedded in the agent as state-modifying parameters, with a `MemorySaver` object assigned to the agent’s checkpointer to ensure chat history persistence.

#### Available Tools
1. **LangChain Wikipedia Tool**
2. **Retriever Tool (RAG)**: Uses Chroma DB as a vector store retriever with embedded content from the [SIPRI database](https://www.sipri.org/databases).
3. **LangChain DuckDuckGoSearch Tool**
4. **Custom Tools for Dashboard Navigation**: 
   - Enables targeted navigation within the dashboard. When the agent selects a section based on the user query, the Dash store value component is updated, triggering a callback to refresh the visualization.

*Development Note*: Part of the [Charming Data Community](https://charming-data.circle.so/) project initiative. 

**Original Data Sources**:
- [SIPRI Arms Transfers Database](https://www.sipri.org/databases/armstransfers)
- [SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)

Data has been post-processed and filtered to a format optimized for interactive Plotly visualizations.

## Video Demo
[![WIP](link_here)]()

## Main App Features
1. **Dash App Design**: Includes GUI components and interactive visualizations.
2. **ReAct Agent with LangGraph**: Enhanced agent functionality with memory and adaptive prompts.
3. **Custom Tool Development**: For targeted agent task execution.

## AI Feature Details
1. `LangGraph` ReAct agent with memory and state-based prompt modifiers.
2. **LangChain Framework**: Utilized for custom agent tool implementations.
3. **LangChain Predefined Tools**: Includes Wikipedia, web search, and retriever tools.
4. **Chroma DB as Vector Store**: For managing embedding data.
5. **OpenAI GPT-4**: Primary model for NLP tasks.

## Known Limitations and Potential Improvements
1. Ongoing development to handle exceptions and refine prompts for better output quality.
2. Enhanced visualizations and expanded dashboard sections.
3. Further expansion of toolsets available for agent operations.


## App structure

```bash
dash-app-structure

|-- .env
|-- .gitignore
|-- License
|-- README.md
|-- assets
|   |-- style files
|-- components
|   |-- <name>Panel.py
|-- data
|   |-- input datasets
|-- data_embed
|   |-- Chroma vectorStore
|-- output
|   |-- exported chat history
|-- utils
|   |-- support.py
|-- tools
|   |-- tool.py
|-- app.py
|-- requirements.txt
|-- demoQA.txt


```

<br>

## Subfolders and Files Details
### utils
code to retrieve the environment vars
### components
python files collections. Dedicated files for the app panels design. 
Modular approach. One file per panel, app section.
### data
input datasets. Post-processed data. Original data from SIPRI dabases
### data_embed
Chroma vectorStore with embedded data from [SIPRI website](https://www.sipri.org/databases).
Used by the agent to provide info about the original data source
### output
exported chat history
### tools
langchain predefined and custom tools definition.
### demoQA.txt
list of samples user query for assistant demo pupose
### python version
python311
