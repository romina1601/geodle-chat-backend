import uuid

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import StreamingResponse

from geodle_chat.core.data_fetcher import fetch_country_details, retrieve_facts_from_json, logger
from geodle_chat.core.session import select_daily_country, session_store
from geodle_chat.llm.prompts import build_system_prompt
from geodle_chat.models.chat import QuestionRequest, ValidationInput
from geodle_chat.core.openai_client import generate_answer_stream

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to Geodle Chat Backend!"}

@router.post("/start_game")
async def start_game():
    session_id = str(uuid.uuid4())

    secret_country = select_daily_country()

    country_facts = fetch_country_details(secret_country)   # Get country details for daily country
    country_flag = None if not country_facts else country_facts['flag']
    logger.info(f'Country facts for {secret_country}: {country_facts}')

    conversation =[{
        "role": "developer",
        "content": build_system_prompt(secret_country=secret_country, country_facts=country_facts,
                                       country_flag=country_flag)
    }]

    # Session data
    session_store[session_id] = {
        "conversation": conversation,
        "secret_country": secret_country
    }

    return {
        "session_id": session_id,
        "message": "I am thinking of a country... Can you guess it? 🗺️",
    }

# Ask Question endpoint. "Stream" refers to how the response is received, i.e. as stream of chunks
@router.post("/ask_stream")
async def ask_question_stream(data: QuestionRequest, request: Request):
    session_id = request.headers.get("X-Session-ID")
    if not session_id or session_id not in session_store:
        raise HTTPException(status_code=400, detail="Session not found. Please start a new game.")

    # Get session data
    session_data = session_store[session_id]
    conversation = session_data["conversation"]
    secret_country = session_data["secret_country"]

    country_facts = retrieve_facts_from_json(secret_country)
    conversation.append({"role": "developer", "content": f"Additional information: {country_facts}"})

    # Add new question
    conversation.append({"role": "user", "content": data.question})

    try:
        async def stream_generator():
            full_response = ""
            async for chunk in generate_answer_stream(conversation=conversation):
                full_response += chunk
                yield chunk
            # Need to add full_response to the conversation to have the whole history
            conversation.append({"role": "assistant", "content": full_response})
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
def validate_answer(data: ValidationInput, request: Request):
    session_id = request.headers.get("X-Session-ID")
    if not session_id or session_id not in session_store:
        raise HTTPException(status_code=400, detail="Session not found. Please start a new game.")

    # Get session data
    session_data = session_store[session_id]
    secret_country = session_data["secret_country"]

    full_response = data.full_answer.lower()
    country_lower = secret_country.lower()
    logger.info(f'Validating AI response: {full_response}')

    is_game_over = (
            "correct" in full_response and
            "the country is" in full_response and
            country_lower in full_response
    )

    return {"is_game_over": is_game_over}