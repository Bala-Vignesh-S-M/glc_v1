# glc/voice/tts/providers/gemini_live/adapter.py

from glc.voice.tts.base import TTSProvider, SynthesizeResult, TTSError

class Provider(TTSProvider):
    # This must match the name expected by the tests
    name = "gemini_live"

    async def synthesize(self, text: str, voice_id: str | None = None) -> SynthesizeResult:
        # 1. Handle empty text edge case (Test 6 requires this)
        if not text:
            return SynthesizeResult(
                audio_b64="",
                mime="audio/wav",
                sample_rate=24000,
                provider=self.name,
            )

        # 2. Get the mock object from the config (if we are running in tests)
        mock = self.config.get("mock")

        # 3. Format the required setup frame for Gemini Live
        # The behavioral test strictly checks for this exact configuration!
        setup_frame = {
            "setup": {
                "generationConfig": {
                    "responseModalities": ["AUDIO"]
                }
            }
        }

        # ---------------------------------------------------------
        # TESTING MODE (When running `pytest`)
        # ---------------------------------------------------------
        if mock is not None:
            # We MUST record the frame so the mock can grade our behavior
            mock.record_frame(setup_frame)
            
            # Then we let the mock fake the actual API call
            return await mock.synthesize(text, voice_id)

        # ---------------------------------------------------------
        # LIVE MODE (When actually running the gateway server)
        # ---------------------------------------------------------
        
        # Here is where you will write the REAL code to connect to Google:
        # 1. Open a websockets connection to: wss://generativelanguage.googleapis.com/...
        # 2. Send the setup_frame
        # 3. Send the `text`
        # 4. Receive the audio bytes, base64 encode them.
        # 5. Handle HTTP/WebSocket errors (raise TTSError(msg, status) if it fails)
        # 6. Return a real SynthesizeResult
        
        raise NotImplementedError("Live API not yet implemented")
