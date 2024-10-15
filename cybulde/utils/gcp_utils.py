from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id:str="1") -> str:
    """
    Access the payload for the given secret if one exists.
    The version can be a version number as string (e.g. "S or an alias (e.g. "latest"))

    Args:
        project_id (str): _description_
        secret_id (str): _description_
        version_id (str): _description_

    Returns:
        str: _description_
    """



    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name":name})

    # Return the decoded payload.
    payload = response.payload.data.decode('UTF-8')
    return payload
