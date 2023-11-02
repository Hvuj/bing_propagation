import time
from typing import Optional, Final, Any
import functions_framework
from src.models.service import Service


@functions_framework.http
def run(request: Optional[Any]) -> str:
    """
    Runs the udf.

    Parameters
    ----------
    request : Optional[Any]
        The payload received that can be used to get dynamic data from outside the function.

    Returns
    -------
    logic: str
        On success - 'True'.
        On failure - 'False'.
    """
    project_id: Final[str] = str(request.get_json().get("project_id"))
    dataset_id: Final[str] = str(request.get_json().get("dataset_id"))
    table_name: Final[str] = str(request.get_json().get("table_name"))

    start = time.time()

    service = Service(
        project_id=project_id, dataset_id=dataset_id, table_name=table_name
    )
    data = service.read_data()
    splitted_data = service.transform_data(data)

    loader = service.load_data(splitted_data)
    print(loader)
    end = time.time()

    print(end - start)
    return str(loader)
