
# 🚀 AIGCPanel 模型自定义接入 - 简易接入示例

本项目用于演示如何在 AIGCPanel 中自定义接入 AI 模型，支持快速环境初始化和依赖安装，适用于 Windows、Linux 和 macOS。✨

## 📋 项目简介

- 🌍 支持多平台环境初始化
- 📁 提供示例配置文件和数据
- 🔧 便于二次开发和集成

## ⚙️ 环境初始化

> 请根据实际情况调整环境配置 🛠️

### 🪟 Windows

```shell
conda 'shell.powershell' 'hook' | Out-String | Invoke-Expression
conda create --prefix ./_aienv -y python=3.10
conda activate ./_aienv
pip install -r requirements.txt
```

### 🐧 Linux / macOS

```shell
eval "$(conda shell.bash hook)"
conda create --prefix ./_aienv -y python=3.10
conda activate ./_aienv
pip install -r requirements.txt
```

## ▶️ 运行示例

```shell
python run.py
```

## 📂 目录结构说明

- `run.py`：主程序入口 🏠
- `cosyvoice_client.py`：CosyVoice API 客户端封装 🔊
- `requirements.txt`：依赖包列表 📦
- `config.json`：主配置文件 ⚙️
- `example/`：示例数据与配置 📊

## 🔊 CosyVoice 集成说明

本示例已支持通过 HTTP API 方式对接 CosyVoice，实现语音合成与语音克隆能力。需在请求参数中提供对应的接口地址或通过环境变量配置。

### 语音合成（soundTts）

- 配置字段：`modelConfig.param.endpoint` 或环境变量 `COSYVOICE_TTS_ENDPOINT`
- 可选字段：`speaker`、`language`、`format`、`timeout`

示例：

```json
{
  "id": "xxx",
  "mode": "local",
  "modelConfig": {
    "type": "soundTts",
    "param": {
      "endpoint": "http://127.0.0.1:5000/v1/tts",
      "speaker": "default",
      "language": "zh",
      "format": "wav",
      "timeout": 60
    },
    "text": "你好，欢迎使用 CosyVoice。"
  },
  "setting": {}
}
```

### 语音克隆（soundClone）

- 配置字段：`modelConfig.param.endpoint` 或环境变量 `COSYVOICE_CLONE_ENDPOINT`
- 必填字段：`promptAudio`（参考音频 URL 或路径）
- 可选字段：`promptText`、`speaker`、`language`、`format`、`timeout`

示例：

```json
{
  "id": "xxx",
  "mode": "local",
  "modelConfig": {
    "type": "soundClone",
    "param": {
      "endpoint": "http://127.0.0.1:5000/v1/clone",
      "speaker": "default",
      "language": "zh",
      "format": "wav",
      "timeout": 60
    },
    "text": "请按照参考音色合成这段文字。",
    "promptAudio": "http://example.com/sample.wav",
    "promptText": "参考音频的文字内容"
  },
  "setting": {}
}
```

### 返回格式说明

CosyVoice API 需要返回 JSON 数据，以下任一格式可被识别：

- `{\"audio_base64\": \"...\"}`：Base64 编码音频
- `{\"url\": \"...\"}`：音频下载链接
- 或嵌套在 `data` 字段内（例如：`{\"data\": {\"url\": \"...\"}}`）

## 📄 License

MIT 📜
