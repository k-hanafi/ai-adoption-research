RESPONSE_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "genai_research_result",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "company_id": {"type": "integer"},
                "company_name": {"type": "string"},
                "genai_adoption_found": {"type": "boolean"},
                "findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "finding_id": {"type": "integer"},
                            "AI_tool_used": {"type": "string"},
                            "use_case": {"type": "string"},
                            "business_function": {"type": "string"},
                            "evidence_description": {"type": "string"},
                            "source_url": {"type": "string"},
                            "source_type": {"type": "string"},
                        },
                        "required": [
                            "finding_id",
                            "AI_tool_used",
                            "use_case",
                            "business_function",
                            "evidence_description",
                            "source_url",
                            "source_type",
                        ],
                        "additionalProperties": False,
                    },
                },
                "no_finding_reason": {"type": ["string", "null"]},
                "no_finding_analysis": {"type": ["string", "null"]},
            },
            "required": [
                "company_id",
                "company_name",
                "genai_adoption_found",
                "findings",
                "no_finding_reason",
                "no_finding_analysis",
            ],
            "additionalProperties": False,
        },
    },
}
