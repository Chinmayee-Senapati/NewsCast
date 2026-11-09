
import torch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor

MODEL_NAME = "ai4bharat/indictrans2-en-indic-dist-200M"
HOST = "127.0.0.1"
PORT = 8765

LANGUAGES = {
    "hi": "hin_Deva",
    "or": "ory_Orya",
}

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"Loading IndicTrans2 on {device}...")
if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME, trust_remote_code=True
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=dtype,
).to(device)
processor = IndicProcessor(inference=True)
print("IndicTrans2 is ready.")
model_lock = Lock()

class TranslationHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ready", "device": device})
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/translate":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            texts = payload.get("texts", [])
            target = payload.get("target", "hi")
            target_language = LANGUAGES.get(target)

            if not isinstance(texts, list) or not texts:
                self.send_json(400, {"error": "'texts' must be a non-empty list"})
                return
            if not target_language:
                self.send_json(400, {"error": "Target must be 'hi' or 'or'"})
                return
            if not all(isinstance(text, str) for text in texts):
                self.send_json(400, {"error": "Every text must be a string"})
                return

            translations = []
            with model_lock, torch.inference_mode():
                for batch_start in range(0, len(texts), 8):
                    batch = texts[batch_start:batch_start + 8]
                    prepared = processor.preprocess_batch(
                        batch,
                        src_lang="eng_Latn",
                        tgt_lang=target_language,
                    )
                    inputs = tokenizer(
                        prepared,
                        truncation=True,
                        padding="longest",
                        max_length=128,
                        return_tensors="pt",
                    ).to(device)

                    output_tokens = model.generate(
                        **inputs,
                        num_beams=1,
                        max_new_tokens=128,
                    )
                    decoded = tokenizer.batch_decode(
                        output_tokens,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=True,
                    )
                    translations.extend(
                        processor.postprocess_batch(decoded, lang=target_language)
                    )

            self.send_json(200, {"translations": translations})

        except Exception as exc:
            print(f"Translation error: {exc}")
            self.send_json(500, {"error": "Translation failed"})

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), TranslationHandler)
    print(f"Translation service listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping translation service...")
    finally:
        server.server_close()

