# AI Engineer World's Fair 2025: Gemini 2.5 Flash Preview Live API + Pipecat demo

## What

 At AI Engineer World's Fair in June 2025, we (Shrestha Basu Mallick and Kwindla Hultman Kramer) gave a talk about building real-world voice agents with advanced features.

 The themes of the talk were:

   - What the moving parts involved in building production voice agents are today.
   - What's hard and what's easy right now.
   - How functionality is distributed between application code, libraries/frameworks, APIs, and models. And how that's changing over time.

During the talk we did a live demo of the latest Gemini 2.5 Flash Preview model and Live API.

This repo is the code that powered that demo.

## Why

The idea was to take some code from a real-world use case, tinker with it together, and experiment with the latest Gemini speech-to-speech model/API.

We ended up pulling some code out of an application Kwin uses every day: a kind of personal todo list app that's always changing and evolving. We stripped the code down to just use the Gemini Live API and Supabase. Then we:

  - Added a function to display text on screen (the code we started with was voice only).
  - Added an async function to generate embedded, dynamic UI via a one-shot call to the standard (non-Live) Gemini API.
  - Iterated on the prompt (a lot).
  - Had a lot of fun seeing what worked and what didn't.

The context here was partly familiar, and partly new, for both of us. So it turned out to be a really good playground for experimenting with the Preview model.

## Code

### Pipecat bot

The [Pipecat](https://docs.pipecat.ai/introduction) bot code is in the [pipecat](pipecat) directory.

  - The main bot code is in [pipecat/gemini_live.py](pipecat/gemini_live.py).
  - The core system_instruction is in [pipecat/system_instruction.txt](pipecat/system_instruction.txt).
  - The dynamic UI one-shot tool is in [pipecat/genai_single_page_app.py](pipecat/genai_single_page_app.py).

To start a local dev server that will run a bot process when the frontend connects:

```
cd pipecat
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# copy env.example to .env and fill in values
python local-dev-server.py
```

To run this code as-is, you'll need to set up a [Supabase project](https://supabase.com/). Given the appropriate Supabase-related environment variables, the [supa/utils/create_todo_turns_table.py](supa/utils/create_todo_turns_table.py) script should create a table, `todo_turns`, in your Supabase project. This is not heavily tested.

You'll also need a [Daily](https://daily.co/) room_url and token. Or you can modify this code to use a different Pipecat transport, for example the [SmallWebRTCTransport](https://docs.pipecat.ai/server/services/transport/small-webrtc), which has no service dependencies.

### Frontend

The frontend code is in the [client](client) directory. It's a very simple app built with the [Pipecat React client-side SDK](https://docs.pipecat.ai/client/react/introduction).

```
cd client
npm install
cp env.local.example .env.local
npm run dev
```

### Deploying the code.

It should be fairly straightforward to deploy the frontend code to [Vercel](https://vercel.com/) and the Pipecat code to [Pipecat Cloud](https://docs.pipecat.daily.co/introduction).
