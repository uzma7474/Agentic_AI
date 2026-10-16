from agents import function_tool
import logging
import httpx

# get loggin instance
logger = logging.getLogger(__name__)

def validate_pr_url(pr_url: str) -> bool:
    # https://github.com/pythoncpp/test-code/pull/1

    # split the url into different parts
    parts = pr_url.split("/")

    # check if all the components are available
    if len(parts) != 7 or parts[5] not in ['pull', 'pulls']:
        raise Exception("invalid pr url detected")

    # extract the components from the url
    owner = parts[3]
    repo = parts[4]
    pr_number = parts[6]
    return owner, repo, pr_number

@function_tool
def fetch_pull_request_diff(pr_url: str):
    """
    Description: Fetch the diff from the pull request.
    Args:
        pr_url: the PR url used to fetch the details from

    Returns: the consolidated diff from the PR
    """
    # verify if the url is valid
    owner, repo, pr_number = validate_pr_url(pr_url=pr_url)
    logger.info(f"owner: {owner}, repo: {repo}, pr_number: {pr_number}")

    # build the url to download the files from the PR
    file_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    # fetch all the files from the PR
    response = httpx.get(file_url)
    if response.status_code == 200:

        # get the files from the PR
        files = response.json()
        if not files:
            raise Exception(f"the PR {pr_number} does not have any file")

        # collect all the diffs
        diffs = []
        for file in files:
            # extract the diff metadata
            filename = file.get("filename")
            patch = file.get("patch")
            deletions = file.get("deletions")
            additions = file.get("additions")
            status = file.get("status")

            diff_header = f"-- {filename} ({status}, +{additions}/-{deletions}) --"            
            diffs.append(f"{diff_header}\n{patch}")

        return "\n\n".join(diffs)
    else:
        raise Exception("error while loading the files from the PR")
