import os

from agent import get_graph
from inputs import from_github
from langchain_core.messages import HumanMessage
from tools import get_pr_metadata
import traceback
from composio import Action, ComposioToolSet
from composio.utils.logging import get_logger

listener = ComposioToolSet().create_trigger_listener()
logger = get_logger(__name__)

# Triggers when a new event takes place
@listener.callback(filters={"trigger_name": "GITHUB_PULL_REQUEST_EVENT"})
def callback_function(event):
    try: 
        logger.info("Received trigger GITHUB_PULL_REQUEST_EVENT")
        payload = event.payload
        action = payload.get("action")
        if action not in ["opened", "reopened"]:
            return
        
        url = payload.get("url")
        split_url = url.split("/")
        owner = split_url[-4]
        repo_name = split_url[-3]
        pull_number = payload.get("number")

        logger.info(f"Running PR Review agent for pull request {url}")

        run_agent(owner, repo_name, pull_number)

    except Exception as e:
        traceback.print_exc()


def run_agent(owner, repo_name, pull_number) -> None:
    repo_path = f"/home/user/{repo_name}"

    graph, composio_toolset = get_graph(repo_path)

    composio_toolset.execute_action(
        action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
        params={"path": "/home/user/"},
    )

    composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_CLONE,
        params={"repo_name": f"{owner}/{repo_name}"},
    )
    composio_toolset.execute_action(
        action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
        params={"path": repo_path},
    )

    response = composio_toolset.execute_action(
        action=get_pr_metadata,
        params={
            "owner": owner,
            "repo": repo_name,
            "pull_number": str(pull_number),
            "thought": "Get the metadata for the PR",
        },
    )
    base_commit = response["data"]["metadata"]["base"]["sha"]

    composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_CLONE,
        params={
            "repo_name": f"{owner}/{repo_name}",
            "just_reset": True,
            "commit_id": base_commit,
        },
    )

    composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_CREATE_CODE_MAP,
        params={},
    )

    graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"You have {owner}/{repo_name} cloned at your current working directory. Review PR {pull_number} on this repository and create comments on the same PR"
                )
            ]
        },
        {"recursion_limit": 70},
    )

if __name__ == "__main__":
    listener.wait_forever()
