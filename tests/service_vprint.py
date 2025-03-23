from service import generate_mock_response

from py_data_viewer import vprint

response = generate_mock_response()
vprint(response, var_name="response", output="out/response.txt")
