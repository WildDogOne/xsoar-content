import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

from CommonServerUserPython import *

"""IMPORTS"""
import warnings
import json
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth


class kibana:
    def __init__(
            self, base_url=None, username=None, password=None, api_key=None, ssl_verify=True
    ):
        """Initialize the Kibana client.

        Args:
            base_url (str): The base URL for the Kibana instance
            username (str, optional): Username for basic authentication
            password (str, optional): Password for basic authentication
            api_key (str, optional): API key for authentication
            ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.

        Raises:
            ValueError: If neither API key nor username/password is provided, or if base_url is not provided
        """
        if not api_key and (not username and not password):
            raise ValueError("No API Key or Username/Password provided")
        if not base_url:
            raise ValueError("No Base URL provided")
        else:
            self.base_url = base_url
        if username:
            self.username = username
        if password:
            self.password = password
        if api_key:
            self.headers = {
                "Authorization": f"ApiKey {api_key}",
                "Accept": "application/json",
            }
            self.api_key = True
        else:
            self.api_key = False
        self.ssl_verify = ssl_verify

    def _get_pagination(self, url, headers=None, params={}):
        """Get paginated results from Kibana API.

        Args:
            url (str): The API endpoint URL
            headers (dict, optional): Custom headers to include in the request
            params (dict, optional): Query parameters for the request

        Returns:
            list: Combined results from all pages, or False if error occurs
        """
        if self.headers is None:
            headers = {"Accept": "application/json"}
        else:
            headers = self.headers
        run = 1
        page = 1
        output = []
        while run == 1:
            params["page"] = page
            if self.api_key:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    params=params,
                    verify=self.ssl_verify,
                )
            else:
                response = requests.request(
                    "GET",
                    url,
                    headers=headers,
                    params=params,
                    verify=self.ssl_verify,
                    auth=HTTPBasicAuth(self.username, self.password),
                )
            if response.status_code != 200:
                return_error("Cannot get")
                logger.info(response)
                return False
            else:
                response = response.json()
                if len(response["data"]) == 0:
                    run = 0
                else:
                    output += response["data"]
                    page += 1
        return output

    def _get(self, url, payload=None, headers=None, params=None):
        """Send a GET request to Kibana API.

        Args:
            url (str): The API endpoint URL
            payload (dict, optional): JSON payload to send with the request
            headers (dict, optional): Custom headers to include in the request
            params (dict, optional): Query parameters for the request

        Returns:
            dict: JSON response if successful, None otherwise
        """
        if payload is None:
            payload = {}
        if self.headers is None:
            headers = {"Accept": "application/json"}
        else:
            headers = self.headers
        if self.api_key:
            response = requests.request(
                "GET",
                url,
                headers=headers,
                json=payload,
                verify=self.ssl_verify,
                params=params,
            )
        else:
            response = requests.request(
                "GET",
                url,
                headers=headers,
                json=payload,
                verify=self.ssl_verify,
                auth=HTTPBasicAuth(self.username, self.password),
                params=params,
            )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return_error(f"Error 404\n{response.url}")
            return_error(response.json())
        else:
            pprint(response.status_code)

    def _put(self, url, payload=None, headers=None):
        """Send a PUT request to Kibana API.

        Args:
            url (str): The API endpoint URL
            payload (dict, optional): JSON payload to send with the request
            headers (dict, optional): Custom headers to include in the request

        Returns:
            dict: JSON response if successful, None otherwise
        """
        if payload is None:
            payload = {}
        if self.headers is None:
            headers = {"Accept": "application/json", "kbn-xsrf": ""}
        else:
            headers = self.headers
        response = requests.request(
            "PUT",
            url,
            headers=headers,
            json=payload,
            verify=self.ssl_verify,
            auth=HTTPBasicAuth(self.username, self.password),
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return_error(f"Error 404\n{response.url}")
            return_error(response.json())
        else:
            pprint(response.status_code)

    def _delete(self, url, headers=None):
        """Send a DELETE request to Kibana API.

        Args:
            url (str): The API endpoint URL
            headers (dict, optional): Custom headers to include in the request

        Returns:
            str: Response text if successful, None otherwise
        """
        if self.headers is None:
            headers = {"Accept": "application/json", "kbn-xsrf": ""}
        else:
            headers = self.headers
        response = requests.request(
            "DELETE",
            url,
            headers=headers,
            verify=self.ssl_verify,
            auth=HTTPBasicAuth(self.username, self.password),
        )
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return_error(f"Error 404\n{response.url}")
            return_error(response.json())
        else:
            return_error(response.status_code)
            return_error(response.json())

    def _post(self, url, payload=None, headers=None, params=None):
        """Send a POST request to Kibana API.

        Args:
            url (str): The API endpoint URL
            payload (dict, optional): JSON payload to send with the request
            headers (dict, optional): Custom headers to include in the request
            params (dict, optional): Query parameters for the request

        Returns:
            Response: Response object if successful, None otherwise
        """
        if payload is None:
            payload = {}
        if self.headers is None:
            headers = {"Accept": "application/json", "kbn-xsrf": ""}
        else:
            headers = self.headers
            headers["kbn-xsrf"] = ""
        if self.api_key:
            response = requests.request(
                "POST",
                url,
                headers=headers,
                json=payload,
                verify=self.ssl_verify,
                params=params,
            )
        else:
            response = requests.request(
                "POST",
                url,
                headers=headers,
                json=payload,
                verify=self.ssl_verify,
                auth=HTTPBasicAuth(self.username, self.password),
                params=params,
            )
        if response.status_code == 200:
            return response
        elif response.status_code == 409:
            return response
        elif response.status_code == 404:
            return_error(f"Error 404\n{response.url}")
            return_error(response.json())
        else:
            return_error(f"Unable to POST\nStatus Code: {response.status_code}")
            return_error(response.json())

    def create_dataview(self, dataview=None, space_id="default"):
        """Create a new data view in Kibana.

        Args:
            dataview (dict, optional): The data view configuration
            space_id (str, optional): The space ID. Defaults to "default"

        Returns:
            Response: Response object from the API call
        """
        if dataview:
            dataview = {"data_view": dataview}
            logger.info(dataview)
            url = self.base_url + "/s/" + space_id + "/api/data_views/data_view"

            payload = dataview
            return self._post(url, payload=payload)
        else:
            return_error("No dataview provided")

    def get_dataview(self, dataview_id=None, space_id="default"):
        """Get a data view by ID or name.

        Args:
            dataview_id (str, optional): The data view ID or name to search for
            space_id (str, optional): The space ID. Defaults to "default"

        Returns:
            str: The data view ID if found, False otherwise
        """
        if dataview_id:
            url = self.base_url + "/s/" + space_id + "/api/data_views"
            dataviews = self._get(url)
            for dataview in dataviews["data_view"]:
                if "name" in dataview and dataview["name"] == dataview_id:
                    return dataview
                elif "title" in dataview and dataview["title"] == dataview_id:
                    return dataview
            return False
        else:
            return_error("No dataview id provided")

    def delete_dataview(self, dataview_id=None, space_id="default"):
        """Delete a data view by ID.

        Args:
            dataview_id (str, optional): The data view ID to delete
            space_id (str, optional): The space ID. Defaults to "default"

        Returns:
            str: Response text from the API call
        """
        if dataview_id:
            url = (
                    self.base_url
                    + "/s/"
                    + space_id
                    + "/api/data_views/data_view/"
                    + dataview_id
            )
            return self._delete(url)
        else:
            return_error("No dataview id provided")

    def install_package(self, package_name=None, package_version=None):
        """Install a package from the Elastic Package Registry.

        Args:
            package_name (str, optional): Name of the package to install
            package_version (str, optional): Version of the package to install

        Returns:
            Response: Response object from the API call
        """
        if package_name:
            url = self.base_url + "/api/fleet/epm/packages/" + package_name.lower()
            if package_version:
                url = url + "/" + package_version
            else:
                package_version = self._get(url)["item"]["version"]
                url = url + "/" + package_version
            return self._post(url)
        else:
            return_error("No Package Name provided")

    def get_install_status(self, package_name=None):
        """Check if a package is installed.

        Args:
            package_name (str, optional): Name of the package to check

        Returns:
            bool: True if package is installed, False otherwise
        """
        if package_name:
            url = self.base_url + "/api/fleet/epm/packages/" + package_name.lower()
            installed = self._get(url)["response"]["status"]
            if installed == "installed":
                return True
            else:
                return False
        else:
            return_error("No Package Name provided")

    def delete_package(self, package_name=None):
        """Delete an installed package.

        Args:
            package_name (str, optional): Name of the package to delete

        Returns:
            str: Response text from the API call
        """
        if package_name:
            url = self.base_url + "/api/fleet/epm/packages/" + package_name.lower()
            package_version = self._get(url)["item"]["version"]
            url = url + "/" + package_version
            return self._delete(url)
        else:
            return_error("No Package Name provided")

    def update_package(self, package_name=None):
        """Update an installed package.

        Args:
            package_name (str, optional): Name of the package to update

        Returns:
            dict: JSON response from the API call
        """
        if package_name:
            url = self.base_url + "/api/fleet/epm/packages/" + package_name.lower()
            package_version = self._get(url)["item"]["version"]
            url = url + "/" + package_version
            return self._put(url)
        else:
            return_error("No Package Name provided")

    def get_package(self, package_name=None):
        """Get package information.

        Args:
            package_name (str, optional): Name of the package to retrieve

        Returns:
            dict: Package information from the API response
        """
        if package_name:
            url = self.base_url + "/api/fleet/epm/packages/" + package_name.lower()
            return self._get(url)["response"]
        else:
            return_error("No Package Name provided")

    def load_prebuilt_rules(self):
        url = self.base_url + "/api/detection_engine/rules/prepackaged"
        return self._put(url)

    def get_prebuilt_rules_status(self, space_id="default"):
        url = self.base_url + f"/s/{space_id}/api/detection_engine/rules/prepackaged/_status"
        return self._get(url)

    def get_rule(self, rule_id, space_id="default"):
        url = self.base_url + f"/s/{space_id}/api/detection_engine/rules"
        params = {"id": rule_id}
        return self._get(url, params=params)

    def get_all_rules(self, title: str = None, space_id="default"):
        page = 1
        output_data = []
        while True:
            url = self.base_url + f"/s/{space_id}/api/detection_engine/rules/_find?per_page=100&page={page}"
            x = self._get(url)
            if len(x["data"]) > 0:
                output_data += x["data"]
                page += 1
                if title:
                    for rule in output_data:
                        if rule["name"] == title:
                            return rule
            else:
                break
        if not title:
            return output_data

    def get_all_exception_lists(self):
        return self._get_pagination(self.base_url + "/api/exception_lists/_find")

    def export_exception_list(self, id=None, list_id=None, namespace_type=None):
        url = self.base_url + "/api/exception_lists/_export"
        params = {"id": id, "list_id": list_id, "namespace_type": namespace_type}
        results = self._post(url, params=params)
        outputs = []
        for result in results.text.split("\n"):
            if len(result) > 0:
                outputs.append(json.loads(result))
        return outputs

    def bulk_change_rules(
            self, rule_ids=None, action="enable", query=None, edit=None, duplicate=None
    ):
        if rule_ids:
            payload = {"ids": rule_ids, "action": action}
            if query:
                payload["query"] = query
            if edit:
                payload["edit"] = edit
            if duplicate:
                payload["duplicate"] = duplicate
            url = self.base_url + "/api/detection_engine/rules/_bulk_action"
            return self._post(url, payload)
        else:
            return_error("No Rules ids provided")

    def get_exception_container(self, container_name=None):
        url = self.base_url + "/api/exception_lists/_find"
        if container_name:
            exception_containers = self._get_pagination(url)
            for exception_container in exception_containers:
                if container_name in exception_container["name"]:
                    return exception_container
            return False
            # return exception_containers
        else:
            return_error("No Container Name provided")

    def create_exception_container(
            self, container_name=None, container_type="detection", description=None
    ):
        url = self.base_url + "/api/exception_lists"
        if container_name:
            payload = {
                "name": container_name,
                "type": container_type,
                "list_id": container_name.replace(" ", "_").lower(),
            }
            if description:
                payload["description"] = description
            else:
                payload["description"] = container_name
            return self._post(url, payload)
        else:
            return_error("No Container Name provided")

    def delete_exception_container(self, container_name=None, list_id=None):
        if container_name and not list_id:
            container = self.get_exception_container(container_name)
            if container:
                list_id = container["list_id"]
            else:
                return_error("No Container found")
        if list_id:
            url = self.base_url + "/api/exception_lists?list_id=" + list_id
            return self._delete(url)
        else:
            return_error("No Container Name or List ID provided")

    def attach_container_to_rule(
            self, container_name=None, rule_name=None, list_id=None
    ):
        if container_name and not list_id:
            container = self.get_exception_container(container_name)
            if container:
                list_id = container["list_id"]
            else:
                return_error("No Container found")

    def post_alert_status(self, signal_ids: str, status: str, space_id: str = "default"):
        # closed / active
        url = self.base_url + f"/s/{space_id}/api/detection_engine/signals/status"
        payload = {"signal_ids": signal_ids, "status": status}
        self._post(url, payload)

    def post_ack_alert(self, signal_ids):
        url = self.base_url + "/api/detection_engine/signals/status"
        payload = {"signal_ids": signal_ids, "status": "in-progress"}
        self._post(url, payload)

    def get_alert(self, alert_id: str, space_id=None):
        url = self.base_url + "/api/detection_engine/alerts/" + alert_id


import urllib3

# Disable insecure warnings
urllib3.disable_warnings()
warnings.filterwarnings(action="ignore", message=".*using SSL with verify_certs=False is insecure.")

ES_DEFAULT_DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss.SSSSSS"
PYTHON_DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
API_KEY_PREFIX = "_api_key_id:"
SERVER = demisto.params().get("url", "").rstrip("/")
USERNAME: str = demisto.params().get("credentials", {}).get("identifier")
PASSWORD: str = demisto.params().get("credentials", {}).get("password")
API_KEY_ID = USERNAME[len(API_KEY_PREFIX):] if USERNAME and USERNAME.startswith(API_KEY_PREFIX) else None
if API_KEY_ID:
    USERNAME = ""
    API_KEY = (API_KEY_ID, PASSWORD)
PROXY = demisto.params().get("proxy")


def kibana_client():
    kibana_client = kibana(base_url=SERVER, api_key=PASSWORD)
    return kibana_client


def test_func(proxies):
    """
    Tests API connectivity to Kibana.
    Tests the existence of all necessary fields for fetch.

    Due to load considerations, the test module doesn't check the validity of the fetch-incident - to test that the fetch works
    as excepted the user should run the es-integration-health-check command.

    """
    kc = kibana_client()
    kc.get_prebuilt_rules_status()
    demisto.results("ok")


def get_prebuilt_rules_status(kc):
    response = kc.get_prebuilt_rules_status()
    return CommandResults(
        outputs_prefix="Kibana.Rules",
        outputs_key_field="kibana",
        outputs=response
    )


def get_dataview(kc: object, args: dict):
    dv = args["dataview"]
    response = kc.get_dataview(dv)

    return CommandResults(
        outputs_prefix="Kibana.DataView",
        outputs_key_field="kibana",
        outputs=response,
        # readable_output="test",
    )


def get_all_rules(kc: object, args: dict) -> CommandResults:
    title = args["title"]
    response = kc.get_all_rules(title)
    return CommandResults(
        outputs_prefix="Kibana.Rules",
        outputs_key_field="kibana",
        outputs=response,
        # readable_output="test",
    )


def main():  # pragma: no cover
    proxies = handle_proxy()
    proxies = proxies if proxies else None
    args = demisto.args()
    kc = kibana_client()
    try:
        LOG(f"command is {demisto.command()}")
        if demisto.command() == "test-module":
            test_func(proxies)
        elif demisto.command() == "kb-get_prebuilt_rules_status":
            return_results(get_prebuilt_rules_status(kc))
        elif demisto.command() == "kb-get_dataview":
            return_results(get_dataview(kc, args))
        elif demisto.command() == "kb-get_all_rules":
            return_results(get_all_rules(kc, args))

    except Exception as e:
        if "The client noticed that the server is not a supported distribution of Elasticsearch" in str(e):
            return_error(
                f"Failed executing {demisto.command()}. Seems that the client does not support the server's "
                f"distribution, Please try using the Open Search client in the instance configuration."
                f"\nError message: {e!s}",
                error=str(e),
            )
        if "failed to parse date field" in str(e):
            return_error(
                f"Failed to execute the {demisto.command()} command. Make sure the `Time field type` is correctly set.",
                error=str(e),
            )
        return_error(f"Failed executing {demisto.command()}.\nError message: {e}", error=str(e))


if __name__ in ("__main__", "builtin", "builtins"):
    main()
