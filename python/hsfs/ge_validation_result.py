#
#   Copyright 2022 Logical Clocks AB
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import json

import humps
import great_expectations as ge

from hsfs import util


class ValidationResult:
    """Metadata object representing a validation result generated by Great Expectations in the Feature Store."""

    def __init__(
        self,
        success,
        result,
        exception_info,
        expectation_config,
        meta,
        id=None,
        observed_value=None,
        expectation_id=None,
        validation_report_id=None,
        href=None,
        expand=None,
        items=None,
        count=None,
        type=None,
    ):
        self._id = id
        self._success = success
        self._observed_value = observed_value
        self._expectation_id = expectation_id
        self._validation_report_id = validation_report_id

        self.result = result
        self.meta = meta
        self.exception_info = exception_info
        self.expectation_config = expectation_config

    @classmethod
    def from_response_json(cls, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        if "count" in json_decamelized:
            if json_decamelized["count"] == 0:
                return []
            return [
                cls(**validation_report)
                for validation_report in json_decamelized["items"]
            ]
        else:
            return cls(**json_decamelized)

    def json(self):
        return json.dumps(self, cls=util.FeatureStoreEncoder)

    def to_dict(self):
        return {
            "id": self._id,
            "success": self.success,
            "exceptionInfo": json.dumps(self._exception_info),
            "expectationConfig": json.dumps(self._expectation_config),
            "result": json.dumps(self._result),
            "meta": json.dumps(self._meta),
        }

    def to_json_dict(self):
        return {
            "id": self._id,
            "success": self.success,
            "exceptionInfo": self._exception_info,
            "expectationConfig": self._expectation_config,
            "result": self._result,
            "meta": self._meta,
        }

    def to_ge_type(self):
        return ge.core.ExpectationValidationResult(
            success=self.success,
            exception_info=self.exception_info,
            expectation_config=self.expectation_config,
            result=self.result,
            meta=self.meta,
        )

    @property
    def id(self):
        """Id of the validation report, set by backend."""
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def success(self):
        """Overall success of the validation step."""
        return self._success

    @success.setter
    def success(self, success):
        self._success = success

    @property
    def result(self):
        """Result of the expectation after validation."""
        return self._result

    @result.setter
    def result(self, result):
        if isinstance(result, dict):
            self._result = result
        elif isinstance(result, str):
            self._result = json.loads(result)
        else:
            raise ValueError("Result field must be stringified json or dict.")

    @property
    def meta(self):
        """Meta field of the validation report to store additional informations."""
        return self._meta

    @meta.setter
    def meta(self, meta):
        if isinstance(meta, dict):
            self._meta = meta
        elif isinstance(meta, str):
            self._meta = json.loads(meta)
        else:
            raise ValueError("Meta field must be stringified json or dict")

    @property
    def exception_info(self):
        """Exception info which can be raised when running validation."""
        return self._exception_info

    @exception_info.setter
    def exception_info(self, exception_info):
        if isinstance(exception_info, dict):
            self._exception_info = exception_info
        elif isinstance(exception_info, str):
            self._exception_info = json.loads(exception_info)
        else:
            raise ValueError("Exception info field must be stringified json or dict.")

    @property
    def expectation_config(self):
        """Expectation configuration used when running validation."""
        return self._expectation_config

    @expectation_config.setter
    def expectation_config(self, expectation_config):
        if isinstance(expectation_config, dict):
            self._expectation_config = expectation_config
        elif isinstance(expectation_config, str):
            self._expectation_config = json.loads(expectation_config)
        else:
            raise ValueError(
                "Expectation config field must be stringified json or dict"
            )

    def __str__(self):
        return self.json()

    def __repr__(self):
        result_string = ""
        if self._result is None and self._observed_value is not None:
            result_string += f"observed_value : {self._observed_value}"
        elif self._result is not None and self._observed_value is None:
            result_string += f"result : {self._result}"

        return (
            f"ValidationResult(success: {self._success},"
            + result_string
            + f"{self._exception_info}, {self._expectation_config}, {self._meta})"
        )
