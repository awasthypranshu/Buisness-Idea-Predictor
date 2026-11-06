
import os
import logging

from fastapi import FastAPI, HTTPException  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI, APIError, AuthenticationError, RateLimitError  # type: ignore

app = FastAPI()

logger = logging.getLogger(__name__)


@app.get("/api")
def idea():

    # Read the Groq API key from environment variables.
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY environment variable is missing."
        )

    # Configure OpenAI SDK to communicate with Groq.
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = [
        {
            "role": "user",
            "content": "Come up with a new business idea for AI Agents, format with headings, subheadings and bullet points."
        }
    ]

    try:
        # stream=True returns response chunks instead of waiting
        # for the complete AI-generated response.
        stream = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=prompt,
            stream=True
        )

    except AuthenticationError as error:
        raise HTTPException(
            status_code=502,
            detail="Groq API authentication failed."
        ) from error

    except RateLimitError as error:
        raise HTTPException(
            status_code=429,
            detail="Groq API rate limit exceeded."
        ) from error

    except APIError as error:
        logger.exception("Groq API request failed")
        raise HTTPException(
            status_code=502,
            detail="Groq API request failed."
        ) from error

    def event_stream():
        try:
            # Process each chunk as soon as Groq generates it.
            for chunk in stream:

                text = chunk.choices[0].delta.content

                if text:
                    # SSE requires each data line to start with "data:".
                    lines = text.splitlines()

                    for line in lines:
                        yield f"data: {line}\n"

                    # An empty line marks the end of an SSE event.
                    yield "\n"

        except Exception:
            logger.exception("Error while streaming Groq response")
            yield "event: error\ndata: Stream interrupted\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
