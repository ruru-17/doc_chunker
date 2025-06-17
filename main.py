from fastapi import FastAPI, UploadFile, File, HTTPException, Body, Form, Header
from fastapi.responses import JSONResponse
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
from unstructured.chunking.basic import chunk_elements
from unstructured.chunking.title import chunk_by_title
from typing import Annotated, Literal
from pydantic import BaseModel
from pathlib import Path
import json

app = FastAPI()

class PartitionPdfParameters(BaseModel):
    partition_strategy: Literal["auto", "hi_res", "ocr_only", "fast"] = "auto"

class ChunkingParameters(BaseModel):
    chunking_strategy: Literal["basic", "by_title"] = "by_title"
    max_characters: int = 500
    new_after_n_chars: int | None = None
    overlap: int = 0
    overlap_all: bool = False
    multipage_sections: bool | None = True
    combine_text_under_n_chars: int = 0

class CombinedParams(PartitionPdfParameters, ChunkingParameters):
    output_dir: str | None = None

@app.post("/chunk_pdf/")
async def chunk_pdf_endpoint(params: Annotated[CombinedParams, Header(convert_underscores=False)], file: UploadFile):

    if params.new_after_n_chars == None:
        params.new_after_n_chars = params.max_characters

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    contents = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    partition_params = params.model_dump(include={"partition_strat"}) | {"filename": "temp.pdf"}
    elements = partition_pdf(**partition_params)

    if params.chunking_strategy == "basic":
        chunk_params_with_elements = params.model_dump(exclude={"file", "output_dir", "partition_strategy", "chunking_strategy", "multipage_sections", "combine_text_under_n_chars"}) | {"elements": elements}
        chunks = chunk_elements(**chunk_params_with_elements)
    else:
        chunk_params_with_elements = params.model_dump(exclude={"file", "output_dir", "partition_strategy", "chunking_strategy"}) | {"elements": elements}
        chunks = chunk_by_title(**chunk_params_with_elements)

    result = []
    for i, elem in enumerate(chunks):
        result.append({"chunk_id": i,
                       "text": getattr(elem, "text", None)})

    response_data = {"num_chunks": len(chunks), "chunks": result}
    response = JSONResponse(content=response_data)

    if params.output_dir:
        output_dir = Path(params.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / file.filename
        file_path = file_path.with_suffix(".json")
        with open(file_path, "w") as f:
            json.dump(response_data, f, indent=4)

    return response                                                                                                                                                                                                                                                                                                                                                                