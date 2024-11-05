## App purpose
Plotly Dash app implementing AI feature and intractive visz on arms trade between countries as well as countries military expenditures.<br>
Original Data Source from SIPRI databases.
[SIPRI Arms Transfers Database](https://www.sipri.org/databases/armstransfers)
[SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)
<br>
Data post-processed and used for interactive Plotly visualization design.
User experience AI assisted. AI assistant w/ Memory implemented to support the user to navigate in the dashboard section and get insights from the data.
The assistant show different dashboard section according to the user questions and interests. 
Each agent action is properly documented with a short explanation (max 150 words) shown in a dedicated panel app.
Assistant can access to the web and embedded data (RAG) to expand the user learing experience.
User can download the chat history.

#### App section implemented so far:
1. input panel to submit user query and end the conversation/export the chat history
2. output panel visualizing the brief explanation of the agent action and generated output
3. main panel showing the requested dashboard section:
> Countries military expense:
>> countries Military expenditures per years in constant (2022) US Dollars and in terms of their GDP Shares.
>> Available visualization: animated map showing the evolution of the selected metric. Interactive line chart allows countries trend comparison.

> Country military trading and value flow.
>> Arms trasfer with focus on the value flow (from recipents to suppliers). Data are grouped per year and limited to the top 10 coutries trading.
>> Available visualization: Sankey plot showing the value flow from the arms recipients to their suppliers. Dash ag-grid  summarytable.
   
#### Agent implementation:  <br>
Implementation of a LangGraph react agent executor using the create_react_agent. This is to easy  manage the agent's cycles and tracks the scratchpad as messages within its state.
Prompt with System instruction passed as agent modifier state parameter, and MemorySaver object assigned to the agent checkpointer for chat history persistence 
 
#### Avaialable Tools:
1.    Langchain Wikipedia tool
2.    retriever tool as RAG tool. Chroma db vector store as retriever. [SIRPI database](https://www.sipri.org/databases) page content embedded and store
3.    Langhchain DuckDuckGoSearch tool
4.    Set of custom tools called to navigate in the proper section of the dashboard. when the agent select the section on the bases of the user query, Dash store value component is updated. This trigger a callback that update the visualization.

Under development-to join the [Charming Data Community](https://charming-data.circle.so/) Project initiative <br>
Original Data Source from SIPRI databases.
[SIPRI Arms Transfers Database](https://www.sipri.org/databases/armstransfers)
[SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)
Data post-processed, filtered to get the proper format to design the interactive Plotly visualization

## Video Demo
[![WIP]()

## Main App features
1. Dash App design. GUI and Interactive Vizs
2. ReAct agent  with LangGraph
3. Custom tool development to implement agents tasks <br>

## AI features details
1. langgraph react_agent with memory and prompt as state_modifier
2. Langchain framework (Python AI packages) for agent custom tools implementation
3. Langchain predefined tools  - wikipedia and web search, retriever tool
4. Chroma db as vector store for embeddings data 
5. Openai gpt-4o

## Known Code Limitations, potential improvements and  other important notes
1. Still under development to manage exceptions, improve agent prompt to increase the output results quality<br>
2. Improve vizs and expand the dashboards sections
3. Extend the list of tools available for the agents operations.


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
