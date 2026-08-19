"""Atlas Cloud provider for Seedream v4 text-to-image generation."""

import os
import time
from urllib.parse import quote

import requests


DEFAULT_BASE_URL = "https://api.atlascloud.ai"
MODEL = "bytedance/seedream-v4"
PENDING_STATUSES = {"created", "queued", "processing"}
SUCCESS_STATUSES = {"completed", "succeeded"}
SIZE_PRESETS = {
    "2K": {
        "1:1": "2048*2048",
        "16:9": "2048*1152",
        "9:16": "1152*2048",
        "4:3": "2048*1536",
        "3:2": "2016*1344",
        "3:4": "1536*2048",
        "2:3": "1344*2016",
        "21:9": "2688*1152",
    },
    "4K": {
        "1:1": "4096*4096",
        "16:9": "4096*2304",
        "9:16": "2304*4096",
        "4:3": "4096*3072",
        "3:2": "4032*2688",
        "3:4": "3072*4096",
        "2:3": "2688*4032",
        "21:9": "4032*1728",
    },
}


class AtlasSeedreamProvider:
    def __init__(
        self,
        api_key,
        base_url=None,
        session=None,
        poll_interval=2,
        poll_timeout=300,
    ):
        self.base_url = (
            base_url
            or os.getenv("ATLASCLOUD_API_BASE")
            or os.getenv("ATLAS_CLOUD_API_BASE")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self.session = session or requests
        self.poll_interval = max(0, poll_interval)
        self.poll_timeout = max(1, poll_timeout)
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        prompt,
        size,
        aspect_ratio,
        max_images,
        width=None,
        height=None,
        image_input=None,
        sequential=False,
    ):
        """Submit each generation once, then poll its result with a bounded GET loop."""
        if image_input:
            raise ValueError("Atlas 的 Seedream v4 文生图端点不支持 image_input")
        if sequential:
            raise ValueError("Atlas 的 Seedream v4 文生图端点不支持 sequential")

        atlas_size = self.resolve_size(size, aspect_ratio, width, height)
        output_urls = []

        for _ in range(max_images):
            response = self.session.post(
                f"{self.base_url}/api/v1/model/generateImage",
                json={"model": MODEL, "prompt": prompt, "size": atlas_size},
                headers=self.headers,
                timeout=60,
            )
            response.raise_for_status()
            prediction = self._prediction_data(response.json())
            status = str(prediction.get("status", "")).lower()

            if status in SUCCESS_STATUSES and prediction.get("outputs"):
                output_urls.extend(prediction["outputs"])
                continue
            if status and status not in PENDING_STATUSES:
                detail = prediction.get("error") or prediction.get("message") or status
                raise RuntimeError(f"Atlas 任务失败: {detail}")

            request_id = prediction.get("id")
            if not request_id:
                raise RuntimeError("Atlas 响应缺少任务 id")
            output_urls.extend(self._poll_result(request_id))

        return output_urls, atlas_size

    @staticmethod
    def resolve_size(size, aspect_ratio, width, height):
        if size == "custom":
            if not width or not height:
                raise ValueError("自定义尺寸需要提供 width 和 height 参数")
            if not 1024 <= width <= 4096 or not 1024 <= height <= 4096:
                raise ValueError("Atlas 自定义宽高必须在 1024-4096 之间")
            return f"{width}*{height}"

        try:
            return SIZE_PRESETS[size][aspect_ratio]
        except KeyError as error:
            raise ValueError(f"Atlas 不支持尺寸组合: {size} / {aspect_ratio}") from error

    @staticmethod
    def _prediction_data(payload):
        if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
            return payload["data"]
        return payload

    def _poll_result(self, request_id):
        result_url = f"{self.base_url}/api/v1/model/result/{quote(str(request_id), safe='')}"
        deadline = time.monotonic() + self.poll_timeout

        while True:
            response = self.session.get(result_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            prediction = self._prediction_data(response.json())
            status = str(prediction.get("status", "")).lower()

            if status in SUCCESS_STATUSES:
                outputs = prediction.get("outputs") or []
                if not outputs:
                    raise RuntimeError("Atlas 任务已完成但未返回图像 URL")
                return outputs
            if status not in PENDING_STATUSES:
                detail = prediction.get("error") or prediction.get("message") or status
                raise RuntimeError(f"Atlas 任务失败: {detail}")
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Atlas 任务轮询超时: {request_id}")

            time.sleep(self.poll_interval)
