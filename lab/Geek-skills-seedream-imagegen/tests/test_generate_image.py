import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "generate_image.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("seedream_generate_image", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    def __init__(self, payload=None, content=b"", headers=None):
        self.payload = payload
        self.content = content
        self.headers = headers or {}
        self.text = ""

    def json(self):
        return self.payload

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self, post_responses, get_responses):
        self.post_responses = list(post_responses)
        self.get_responses = list(get_responses)
        self.post_calls = []
        self.get_calls = []

    def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        return self.post_responses.pop(0)

    def get(self, url, **kwargs):
        self.get_calls.append((url, kwargs))
        return self.get_responses.pop(0)


class SeedreamImageGeneratorTest(unittest.TestCase):
    def test_atlas_posts_once_then_polls_and_downloads(self):
        session = FakeSession(
            post_responses=[FakeResponse({"id": "req/1", "status": "created"})],
            get_responses=[
                FakeResponse({"id": "req/1", "status": "completed", "outputs": ["https://cdn.test/image.png"]}),
                FakeResponse(content=b"png-data"),
            ],
        )
        generator = MODULE.SeedreamImageGenerator(
            api_key="test-key",
            provider="atlas",
            atlas_base_url="https://atlas.test",
            session=session,
            poll_interval=0,
        )

        with tempfile.TemporaryDirectory() as output_dir:
            paths = generator.generate(
                prompt="test image",
                size="2K",
                aspect_ratio="16:9",
                output_dir=output_dir,
            )
            self.assertEqual(Path(paths[0]).read_bytes(), b"png-data")

        self.assertEqual(len(session.post_calls), 1)
        post_url, post_kwargs = session.post_calls[0]
        self.assertEqual(post_url, "https://atlas.test/api/v1/model/generateImage")
        self.assertEqual(
            post_kwargs["json"],
            {
                "model": "bytedance/seedream-v4",
                "prompt": "test image",
                "size": "2048*1152",
            },
        )
        self.assertEqual(post_kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(
            session.get_calls[0][0],
            "https://atlas.test/api/v1/model/result/req%2F1",
        )

    def test_atlas_rejects_unsupported_reference_and_sequential_modes(self):
        generator = MODULE.SeedreamImageGenerator(
            api_key="test-key",
            provider="atlas",
            session=FakeSession([], []),
        )

        with self.assertRaisesRegex(ValueError, "image_input"):
            generator.generate(prompt="test", image_input=["https://example.test/ref.png"])
        with self.assertRaisesRegex(ValueError, "sequential"):
            generator.generate(prompt="test", sequential=True)

    def test_segmind_remains_the_default_provider(self):
        session = FakeSession(
            post_responses=[FakeResponse(content=b"segmind-image")],
            get_responses=[],
        )
        generator = MODULE.SeedreamImageGenerator(api_key="test-key", session=session)

        with tempfile.TemporaryDirectory() as output_dir:
            paths = generator.generate(prompt="test image", output_dir=output_dir)
            self.assertEqual(Path(paths[0]).read_bytes(), b"segmind-image")

        post_url, post_kwargs = session.post_calls[0]
        self.assertEqual(post_url, "https://api.segmind.com/v1/seedream-4")
        self.assertEqual(post_kwargs["headers"]["x-api-key"], "test-key")


if __name__ == "__main__":
    unittest.main()
