import base64
import os
from typing import Any, Dict, Optional

import requests


class CosyVoiceError(RuntimeError):
    pass


def _require(value: Optional[str], label: str) -> str:
    if not value:
        raise CosyVoiceError(f"缺少 {label} 配置")
    return value


def _post_json(endpoint: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    response = requests.post(endpoint, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise CosyVoiceError("CosyVoice API 返回非 JSON 对象")
    return data


def _extract_audio_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    if "data" in data and isinstance(data["data"], dict):
        return data["data"]
    return data


def _write_audio_from_base64(b64_value: str, output_path: str) -> None:
    audio_bytes = base64.b64decode(b64_value)
    with open(output_path, "wb") as file:
        file.write(audio_bytes)


def _download_audio(url: str, output_path: str, timeout: int) -> None:
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)


def synthesize_tts(model_config: Dict[str, Any], output_path: str) -> None:
    params = model_config.get("param", {})
    endpoint = params.get("endpoint") or os.getenv("COSYVOICE_TTS_ENDPOINT")
    timeout = int(params.get("timeout", 60))
    text = model_config.get("text")

    endpoint = _require(endpoint, "CosyVoice TTS endpoint")
    text = _require(text, "text")

    payload = {
        "text": text,
        "speaker": params.get("speaker"),
        "language": params.get("language"),
        "format": params.get("format", "wav"),
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    response = _post_json(endpoint, payload, timeout)
    audio_payload = _extract_audio_payload(response)

    if "audio_base64" in audio_payload:
        _write_audio_from_base64(audio_payload["audio_base64"], output_path)
        return
    if "url" in audio_payload:
        _download_audio(audio_payload["url"], output_path, timeout)
        return

    raise CosyVoiceError("CosyVoice TTS 响应未包含音频内容")


def synthesize_clone(model_config: Dict[str, Any], output_path: str) -> None:
    params = model_config.get("param", {})
    endpoint = params.get("endpoint") or os.getenv("COSYVOICE_CLONE_ENDPOINT")
    timeout = int(params.get("timeout", 60))
    text = model_config.get("text")
    prompt_audio = model_config.get("promptAudio")
    prompt_text = model_config.get("promptText")

    endpoint = _require(endpoint, "CosyVoice Clone endpoint")
    text = _require(text, "text")
    prompt_audio = _require(prompt_audio, "promptAudio")

    payload = {
        "text": text,
        "prompt_audio": prompt_audio,
        "prompt_text": prompt_text,
        "speaker": params.get("speaker"),
        "language": params.get("language"),
        "format": params.get("format", "wav"),
    }
    payload = {key: value for key, value in payload.items() if value is not None}

    response = _post_json(endpoint, payload, timeout)
    audio_payload = _extract_audio_payload(response)

    if "audio_base64" in audio_payload:
        _write_audio_from_base64(audio_payload["audio_base64"], output_path)
        return
    if "url" in audio_payload:
        _download_audio(audio_payload["url"], output_path, timeout)
        return

    raise CosyVoiceError("CosyVoice 克隆响应未包含音频内容")
