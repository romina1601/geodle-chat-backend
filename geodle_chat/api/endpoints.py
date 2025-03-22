import uuid

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import StreamingResponse

from geodle_chat.core.data_fetcher import fetch_country_details, retrieve_facts_from_json
from geodle_chat.core.session import select_daily_country, session_store
from geodle_chat.models.question import QuestionRequest
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

    # Session data
    conversation =[{
        "role": "system",
        "content": f"You are playing a game with a user. You are thinking of a country, "
         f"{secret_country}, and the user will ask you questions to try and guess it."
         f"Do not give it away too easily. Country context: {country_facts}."
         f"The user can ask yes/no questions and open questions as well."
         f"Make sure that when you give hints you don't disclose the country."
         f"While giving hints, don't say the full name or part of the name of the country."
         f"When the user asks a question, if it appears to be a guess (for example, "
         f"phrases like 'Is it the UK?', 'I guess it's Italy', or similar natural language guesses), compare the guess with "
         f"the secret country (which you know from the context). If the guess is correct (even if it contains extra words or "
         f"typos), respond with 'Correct! The country is [secret_country]! Come back again tomorrow!' and do not provide further hints."
         f"You have to strictly use this format, not other variations. "
         f"If the guess is not correct, provide a helpful hint based on the country context."}]

    session_store[session_id] = {
        "conversation": conversation,
        "secret_country": secret_country
    }

    return {
        "session_id": session_id,
        "message": "I am thinking of a country... Can you guess it? 🗺️",
        "secret_country": secret_country,  # TODO: Debugging only, remove later
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
    conversation.append({"role": "system", "content": f"Additional information: {country_facts}"})

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