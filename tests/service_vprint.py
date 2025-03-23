from py_data_viewer import file_output, vprint
from service import generate_mock_response

response = generate_mock_response()
# vprint(response, var_name="response")
file_output.output(response, "out/output")
