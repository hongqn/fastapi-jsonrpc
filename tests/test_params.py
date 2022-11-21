from typing import List, Tuple

import pytest
from pydantic import BaseModel, Field

from fastapi_jsonrpc import Params


class WholeParams(BaseModel):
    data: List[str] = Field(..., example=["111", "222"])
    amount: int = Field(..., gt=5, example=10)


@pytest.fixture
def ep(ep):
    @ep.method()
    def probe(whole_params: WholeParams = Params(...)) -> List[int]:
        return [int(item) + whole_params.amount for item in whole_params.data]

    @ep.method()
    def probe_by_position_params(
        whole_params: Tuple[List[str], int] = Params(...)
    ) -> List[int]:
        data, amount = whole_params
        return [int(item) + amount for item in data]

    return ep


def test_basic(json_request):
    resp = json_request(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "probe",
            "params": {"data": ["11", "22", "33"], "amount": 1000},
        }
    )
    assert resp == {"id": 1, "jsonrpc": "2.0", "result": [1011, 1022, 1033]}


def test_by_position_params(json_request):
    resp = json_request(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "probe_by_position_params",
            "params": [["11", "22", "33"], 1000],
        }
    )
    assert resp == {"id": 1, "jsonrpc": "2.0", "result": [1011, 1022, 1033]}


def test_openapi(app_client, openapi_compatible):
    resp = app_client.get("/openapi.json")
    assert resp.json() == openapi_compatible(
        {
            "components": {
                "schemas": {
                    "InternalError": {
                        "properties": {
                            "code": {
                                "const": -32603,
                                "default": -32603,
                                "example": -32603,
                                "title": "Code",
                                "type": "integer",
                            },
                            "message": {
                                "const": "Internal error",
                                "default": "Internal error",
                                "example": "Internal error",
                                "title": "Message",
                                "type": "string",
                            },
                        },
                        "title": "InternalError",
                        "type": "object",
                    },
                    "InvalidParams": {
                        "properties": {
                            "code": {
                                "const": -32602,
                                "default": -32602,
                                "example": -32602,
                                "title": "Code",
                                "type": "integer",
                            },
                            "data": {
                                "$ref": "#/components/schemas/_ErrorData__Error_",
                            },
                            "message": {
                                "const": "Invalid params",
                                "default": "Invalid params",
                                "example": "Invalid params",
                                "title": "Message",
                                "type": "string",
                            },
                        },
                        "title": "InvalidParams",
                        "type": "object",
                    },
                    "InvalidRequest": {
                        "properties": {
                            "code": {
                                "const": -32600,
                                "default": -32600,
                                "example": -32600,
                                "title": "Code",
                                "type": "integer",
                            },
                            "data": {
                                "$ref": "#/components/schemas/_ErrorData__Error_",
                            },
                            "message": {
                                "const": "Invalid Request",
                                "default": "Invalid Request",
                                "example": "Invalid Request",
                                "title": "Message",
                                "type": "string",
                            },
                        },
                        "title": "InvalidRequest",
                        "type": "object",
                    },
                    "MethodNotFound": {
                        "properties": {
                            "code": {
                                "const": -32601,
                                "default": -32601,
                                "example": -32601,
                                "title": "Code",
                                "type": "integer",
                            },
                            "message": {
                                "const": "Method not found",
                                "default": "Method not found",
                                "example": "Method not found",
                                "title": "Message",
                                "type": "string",
                            },
                        },
                        "title": "MethodNotFound",
                        "type": "object",
                    },
                    "ParseError": {
                        "properties": {
                            "code": {
                                "const": -32700,
                                "default": -32700,
                                "example": -32700,
                                "title": "Code",
                                "type": "integer",
                            },
                            "message": {
                                "const": "Parse error",
                                "default": "Parse error",
                                "example": "Parse error",
                                "title": "Message",
                                "type": "string",
                            },
                        },
                        "title": "ParseError",
                        "type": "object",
                    },
                    "WholeParams": {
                        "properties": {
                            "amount": {
                                "example": 10,
                                "exclusiveMinimum": 5.0,
                                "title": "Amount",
                                "type": "integer",
                            },
                            "data": {
                                "example": ["111", "222"],
                                "items": {"type": "string"},
                                "title": "Data",
                                "type": "array",
                            },
                        },
                        "required": ["data", "amount"],
                        "title": "WholeParams",
                        "type": "object",
                    },
                    "_Error": {
                        "properties": {
                            "ctx": {
                                "title": "Ctx",
                                "type": "object",
                            },
                            "loc": {
                                "items": {
                                    "type": "string",
                                },
                                "title": "Loc",
                                "type": "array",
                            },
                            "msg": {
                                "title": "Msg",
                                "type": "string",
                            },
                            "type": {
                                "title": "Type",
                                "type": "string",
                            },
                        },
                        "required": ["loc", "msg", "type"],
                        "title": "_Error",
                        "type": "object",
                    },
                    "_ErrorData__Error_": {
                        "properties": {
                            "errors": {
                                "items": {
                                    "$ref": "#/components/schemas/_Error",
                                },
                                "title": "Errors",
                                "type": "array",
                            },
                        },
                        "title": "_ErrorData[_Error]",
                        "type": "object",
                    },
                    "_ErrorResponse_InternalError_": {
                        "additionalProperties": False,
                        "properties": {
                            "error": {
                                "$ref": "#/components/schemas/InternalError",
                            },
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                        },
                        "required": ["error"],
                        "title": "_ErrorResponse[InternalError]",
                        "type": "object",
                    },
                    "_ErrorResponse_InvalidParams_": {
                        "additionalProperties": False,
                        "properties": {
                            "error": {
                                "$ref": "#/components/schemas/InvalidParams",
                            },
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                        },
                        "required": ["error"],
                        "title": "_ErrorResponse[InvalidParams]",
                        "type": "object",
                    },
                    "_ErrorResponse_InvalidRequest_": {
                        "additionalProperties": False,
                        "properties": {
                            "error": {
                                "$ref": "#/components/schemas/InvalidRequest",
                            },
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                        },
                        "required": ["error"],
                        "title": "_ErrorResponse[InvalidRequest]",
                        "type": "object",
                    },
                    "_ErrorResponse_MethodNotFound_": {
                        "additionalProperties": False,
                        "properties": {
                            "error": {
                                "$ref": "#/components/schemas/MethodNotFound",
                            },
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                        },
                        "required": ["error"],
                        "title": "_ErrorResponse[MethodNotFound]",
                        "type": "object",
                    },
                    "_ErrorResponse_ParseError_": {
                        "additionalProperties": False,
                        "properties": {
                            "error": {
                                "$ref": "#/components/schemas/ParseError",
                            },
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                        },
                        "required": ["error"],
                        "title": "_ErrorResponse[ParseError]",
                        "type": "object",
                    },
                    "_Request": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "method": {
                                "title": "Method",
                                "type": "string",
                            },
                            "params": {
                                "title": "Params",
                                "anyOf": [
                                    {
                                        "type": "object",
                                    },
                                    {
                                        "type": "array",
                                        "items": {},
                                    },
                                ],
                            },
                        },
                        "required": ["method"],
                        "title": "_Request",
                        "type": "object",
                    },
                    "_Request_probe_": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "method": {
                                "const": "probe",
                                "default": "probe",
                                "example": "probe",
                                "title": "Method",
                                "type": "string",
                            },
                            "params": {
                                "$ref": "#/components/schemas/WholeParams",
                            },
                        },
                        "required": ["params"],
                        "title": "_Request[probe]",
                        "type": "object",
                    },
                    "_Request_probe_by_position_params_": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "method": {
                                "const": "probe_by_position_params",
                                "example": "probe_by_position_params",
                                "title": "Method",
                                "type": "string",
                            },
                            "params": {
                                "items": [
                                    {"items": {"type": "string"}, "type": "array"},
                                    {"type": "integer"},
                                ],
                                "maxItems": 2,
                                "minItems": 2,
                                "title": "Params",
                                "type": "array",
                            },
                        },
                        "required": ["params"],
                        "title": "_Request[probe_by_position_params]",
                        "type": "object",
                    },
                    "_Response": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "result": {
                                "title": "Result",
                                "type": "object",
                            },
                        },
                        "required": ["result"],
                        "title": "_Response",
                        "type": "object",
                    },
                    "_Response_probe_": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "default": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "result": {
                                "items": {
                                    "type": "integer",
                                },
                                "title": "Result",
                                "type": "array",
                            },
                        },
                        "required": ["result"],
                        "title": "_Response[probe]",
                        "type": "object",
                    },
                    "_Response_probe_by_position_params_": {
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}],
                                "example": 0,
                                "title": "Id",
                            },
                            "jsonrpc": {
                                "const": "2.0",
                                "example": "2.0",
                                "title": "Jsonrpc",
                                "type": "string",
                            },
                            "result": {
                                "items": {"type": "integer"},
                                "title": "Result",
                                "type": "array",
                            },
                        },
                        "required": ["result"],
                        "title": "_Response[probe_by_position_params]",
                        "type": "object",
                    },
                }
            },
            "info": {
                "title": "FastAPI",
                "version": "0.1.0",
            },
            "openapi": "3.0.2",
            "paths": {
                "/api/v1/jsonrpc": {
                    "post": {
                        "operationId": "entrypoint_api_v1_jsonrpc_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/_Request",
                                    },
                                },
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_Response",
                                        },
                                    },
                                },
                                "description": "Successful Response",
                            },
                            "200 ": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_ErrorResponse_InvalidParams_",
                                        },
                                    },
                                },
                                "description": "[-32602] Invalid params\n\nInvalid method parameter(s)",
                            },
                            "200  ": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_ErrorResponse_MethodNotFound_",
                                        },
                                    },
                                },
                                "description": "[-32601] Method not found\n\nThe method does not exist / is not available",
                            },
                            "200   ": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_ErrorResponse_ParseError_",
                                        },
                                    },
                                },
                                "description": "[-32700] Parse error\n\nInvalid JSON was received by the server",
                            },
                            "200    ": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_ErrorResponse_InvalidRequest_",
                                        },
                                    },
                                },
                                "description": "[-32600] Invalid Request\n\nThe JSON sent is not a valid Request object",
                            },
                            "200     ": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_ErrorResponse_InternalError_",
                                        },
                                    },
                                },
                                "description": "[-32603] Internal error\n\nInternal JSON-RPC error",
                            },
                        },
                        "summary": "Entrypoint",
                    },
                },
                "/api/v1/jsonrpc/probe": {
                    "post": {
                        "operationId": "probe_api_v1_jsonrpc_probe_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/_Request_probe_",
                                    },
                                },
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_Response_probe_",
                                        },
                                    },
                                },
                                "description": "Successful Response",
                            },
                        },
                        "summary": "Probe",
                    },
                },
                "/api/v1/jsonrpc/probe_by_position_params": {
                    "post": {
                        "operationId": "probe_by_position_params_api_v1_jsonrpc_probe_by_position_params_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/_Request_probe_by_position_params_"
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/_Response_probe_by_position_params_"
                                        }
                                    }
                                },
                                "description": "Successful " "Response",
                            }
                        },
                        "summary": "Probe " "By " "Position " "Params",
                    }
                },
            },
        }
    )
