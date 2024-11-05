# abc_boot_final
abc_bootcamp_submission


**project scope**:
    To identify potential reviewers for any given proposal title / proposal summary 
    
    **objectives**:
    To serve as an additional tool for grants officers to identify potential reviewers, especially when the proposals are technical
    
    **data sources**:
    Self-curated excel sheet contatin the reviewer's info and expertise, saved as vector_store using Chroma
    200+ reviewers across a wide range of disciplines 
    
    **features**:
    LLM is able to provide suggestions on the potential fields/ sub-discipline a proposal would be in 
    Using embedding relevant reviewers can be identified
    From the pool of relevant reviewers, the LLM will recommend the top 3 reviewers

**Process Flow**:
    
    1. **Start**
    2. **Step 1**: User types in proposal title or proposal summary 
    3. **Step 2**: LLM will summarise proposal and list down all related disciplines to supplement the search query
    4. **Step 3**: retrieve relevant reviewer from chroma vector_store with MMR
    5. **Step 4**: convert output to markdown table to preserve metadata
    6. **Step 5**: LLM to summarise and choose the top 3 relevant reviewers
    7. **End**
