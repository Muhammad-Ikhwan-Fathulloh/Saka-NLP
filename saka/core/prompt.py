import json, re
from typing import Optional, Any, Union, List, Dict
from .normalizer import normalize, async_normalize
from .tokenizer import tokenize, async_tokenize, get_token_count

class PromptTemplate:
    def __init__(self, template: str): self.template = template
    def render(self, **kwargs) -> str:
        res = self.template
        for k, v in kwargs.items(): res = res.replace(f"{{{{{k}}}}}", str(v))
        return res

def build_prompt(**kwargs) -> Union[str, Dict[str, Any]]:
    """Membangun prompt terstruktur. Jika return_meta=True, mengembalikan dict dengan prompt dan token_count."""
    opt, max_t = kwargs.get('optimize_text', True), kwargs.get('max_tokens')
    inp = kwargs.get('input_data', "")
    ret_meta = kwargs.get('return_meta', False)
    
    if opt and inp: inp = normalize(inp)
    if max_t and inp:
        tokens = tokenize(inp)
        if len(tokens) > max_t: inp = " ".join(tokens[:max_t])
            
    parts = []
    def add(label, val): 
        if val: parts.append(f"{label.upper()}:\n{val.strip()}\n")

    add("role", kwargs.get('role'))
    add("task", kwargs.get('task') or kwargs.get('instruction'))
    add("context", kwargs.get('context'))
    add("constraint", kwargs.get('constraint'))
    
    if kwargs.get('output_contract'):
        parts.append(f"OUTPUT CONTRACT (JSON):\nKembalikan JSON valid sesuai skema:\n{json.dumps(kwargs['output_contract'], indent=2)}\n")
    
    add("fallback rule", kwargs.get('fallback_rule'))
    
    if kwargs.get('examples'):
        parts.append("EXAMPLES:")
        for i, ex in enumerate(kwargs['examples']):
            parts.append(f"Ex {i+1}: In: {ex.get('input')} | Out: {ex.get('output')}")
            
    add("data input", inp)
    
    if not kwargs.get('output_contract'):
        ind = kwargs.get('output_indicator', 'Teks').strip()
        if ind.upper() in ["JSON", "LIST", "TABEL"]:
            ind = f"{ind}\n(Output HANYA format {ind} tanpa penjelasan)"
        add("output indicator", ind)
    
    prompt_text = "\n".join(parts)
    
    if ret_meta:
        return {
            "prompt": prompt_text,
            "token_count": get_token_count(prompt_text)
        }
    return prompt_text

async def async_build_prompt(**kwargs) -> str:
    if kwargs.get('optimize_text', True) and kwargs.get('input_data'):
        kwargs['input_data'] = await async_normalize(kwargs['input_data'])
        kwargs['optimize_text'] = False
    return build_prompt(**kwargs)

def parse_llm_output(text: str, format_type: str = "json") -> Any:
    if format_type.lower() == "json":
        text = text.strip()
        match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", text, re.DOTALL)
        if match: text = match.group(1)
        else:
            match_raw = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
            if match_raw: text = match_raw.group(1)
        try: return json.loads(text)
        except: return None
    elif format_type.lower() == "list":
        return [re.match(r"^(?:[-*]|\d+\.)\s+(.+)$", l.strip()).group(1) for l in text.split('\n') if re.match(r"^(?:[-*]|\d+\.)\s+(.+)$", l.strip())]
    return text
