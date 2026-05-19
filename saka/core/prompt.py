import json
import re
from typing import Optional, Any, Union
from .normalizer import normalize, async_normalize
from .tokenizer import tokenize, async_tokenize

def build_prompt(
    instruction: str,
    input_data: str,
    context: str = "",
    output_indicator: str = "Teks",
    optimize_text: bool = True,
    max_tokens: Optional[int] = None
) -> str:
    """
    Membangun prompt yang terstruktur untuk LLM berdasarkan Anatomi Prompt:
    1. Instruksi
    2. Konteks
    3. Data Input
    4. Indikator Output
    
    Parameters:
        instruction (str): Tugas spesifik yang harus dilakukan AI.
        input_data (str): Teks mentah yang perlu diproses.
        context (str, optional): Latar belakang atau gaya bahasa.
        output_indicator (str, optional): Format hasil (misalnya JSON, Tabel).
        optimize_text (bool, optional): Jika True, akan menormalisasi input_data dari bahasa gaul/slang.
        max_tokens (int, optional): Batas maksimal token untuk input_data. Jika lebih, teks akan dipotong.
        
    Returns:
        str: Prompt utuh yang siap dimasukkan ke LLM.
    """
    
    processed_input = input_data
    
    # Optimasi: Normalisasi (slang to formal)
    if optimize_text:
        processed_input = normalize(processed_input)
        
    # Optimasi: Pembatasan panjang token
    if max_tokens is not None and max_tokens > 0:
        tokens = tokenize(processed_input)
        if len(tokens) > max_tokens:
            processed_input = " ".join(tokens[:max_tokens])
            
    # Merakit Prompt
    prompt_parts = []
    
    prompt_parts.append(f"[Instruksi]:\n{instruction.strip()}\n")
    
    if context.strip():
        prompt_parts.append(f"[Konteks]:\n{context.strip()}\n")
        
    prompt_parts.append(f"[Data Input]:\n{processed_input.strip()}\n")
    
    output_str = output_indicator.strip()
    if output_str.upper() in ["JSON", "LIST", "TABEL", "MARKDOWN"]:
        output_str = f"{output_str}\n(Keluarkan output HANYA dalam format {output_str} tanpa pengantar maupun penjelasan tambahan)"
    
    prompt_parts.append(f"[Indikator Output]:\n{output_str}")
    
    return "\n".join(prompt_parts)

async def async_build_prompt(
    instruction: str,
    input_data: str,
    context: str = "",
    output_indicator: str = "Teks",
    optimize_text: bool = True,
    max_tokens: Optional[int] = None
) -> str:
    """
    Versi asinkron dari build_prompt. Sangat direkomendasikan jika ingin memproses dataset besar secara paralel.
    """
    
    processed_input = input_data
    
    # Optimasi: Normalisasi (slang to formal)
    if optimize_text:
        processed_input = await async_normalize(processed_input)
        
    # Optimasi: Pembatasan panjang token
    if max_tokens is not None and max_tokens > 0:
        tokens = await async_tokenize(processed_input)
        if len(tokens) > max_tokens:
            processed_input = " ".join(tokens[:max_tokens])
            
    # Merakit Prompt
    prompt_parts = []
    
    prompt_parts.append(f"[Instruksi]:\n{instruction.strip()}\n")
    
    if context.strip():
        prompt_parts.append(f"[Konteks]:\n{context.strip()}\n")
        
    prompt_parts.append(f"[Data Input]:\n{processed_input.strip()}\n")
    
    output_str = output_indicator.strip()
    if output_str.upper() in ["JSON", "LIST", "TABEL", "MARKDOWN"]:
        output_str = f"{output_str}\n(Keluarkan output HANYA dalam format {output_str} tanpa pengantar maupun penjelasan tambahan)"
    
    prompt_parts.append(f"[Indikator Output]:\n{output_str}")
    
    return "\n".join(prompt_parts)

def parse_llm_output(text: str, format_type: str = "json") -> Any:
    """
    Mem-parsing teks balasan dari LLM menjadi struktur data asli Python.
    Mendukung tipe 'json' dan 'list'.
    
    Parameters:
        text (str): Teks respons mentah dari LLM.
        format_type (str): Tipe format yang diekspektasikan ("json" atau "list").
        
    Returns:
        Any: Dictionary/List untuk json, List of string untuk list, atau teks aslinya jika format tidak dikenali.
    """
    format_type = format_type.lower()
    
    if format_type == "json":
        # Cari blok kode markdown
        match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # Fallback jika LLM tidak menggunakan markdown code block
            match_fallback = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
            if match_fallback:
                json_str = match_fallback.group(1)
            else:
                json_str = text
                
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
            
    elif format_type == "list":
        lines = text.split('\n')
        result = []
        for line in lines:
            line = line.strip()
            # Mencocokkan bullet point seperti "-", "*", atau "1."
            match = re.match(r"^(?:[-*]|\d+\.)\s+(.+)$", line)
            if match:
                result.append(match.group(1))
        return result
        
    return text
