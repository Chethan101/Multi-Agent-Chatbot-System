from typing import List, Tuple, Annotated, TypedDict
import operator
from planner import get_planner, get_replanner
from executor import get_executor
from planner import Response
from langgraph.graph import StateGraph, END

import os
from uuid import uuid4

# Define the State
class State(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str
    

# Create the graph

def get_graph():
    # Create agents
    executor = get_executor()
    planner = get_planner()
    replanner = get_replanner()

    def execute(state: State):
        task = state['plan'][0]
        output = executor.invoke({'input': task, "chat_history" : []})
        return {"past_steps" : (task, output['agent_outcome'].return_values['output'])}

    def plan(state: State):
        plan = planner.invoke({'objective': state['input']})
        return {"plan" : plan.steps}

    def replan(state: State):
        output = replanner.invoke(state)
        # If the output is a response (the plan is complete), then return the response else update the plan
        if isinstance(output, Response):
            return {"response" : output.response}
        else:
            return {"plan" : output.steps}

    def should_end(state: State):
        if (state['response']):
            return True
        else:
            return False
        
    graph = StateGraph(State)
    graph.add_node("planner", plan)
    graph.add_node("executor", execute)
    graph.add_node("replanner", replan)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "replanner")
    graph.add_conditional_edges(
        'replanner',
        should_end,
        {
            True: END,
            False: "executor"
        })
    return graph.compile()


