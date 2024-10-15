from cybulde.config_schemas.config_schema import Config
from cybulde.utils.config_utils import get_config
from cybulde.utils.data_utils import get_raw_data_with_version
from cybulde.utils.gcp_utils import access_secret_version



@get_config(config_path="../configs", config_name="config")
def prepare_dataset(config: Config) -> None:
    version="v1"
    data_local_save_dir ="./dataset/raw"
    dvc_remote_repo = "https://github.com/Nour-B/cybulde-data.git"
    dvc_data_folder="data/raw"
    github_user_name = "Nour-B"
    github_acccess_token = access_secret_version("cybulde-n","cybulde-data-github-access-token")
    
    get_raw_data_with_version(
        version=version,
        data_local_save_dir=data_local_save_dir,
        dvc_remote_repo=dvc_remote_repo,
        dvc_data_folder=dvc_data_folder,
        github_user_name=github_user_name,
        github_acccess_token=github_acccess_token
    )

if __name__ == "__main__":
    prepare_dataset()