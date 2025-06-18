#!/usr/bin/env python3

import sys
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from supabase import acreate_client, AsyncClient
from loguru import logger

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


async def save_todo_state(user_id: str) -> None:
    """
    Save all todo turns for a user to a JSON file.
    
    Args:
        user_id: The user ID to export todo turns for
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Missing SUPABASE_URL or SUPABASE_KEY in environment")
        sys.exit(1)
    
    try:
        # Create Supabase client
        supabase: AsyncClient = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Query all todo turns for the user in chronological order
        logger.info(f"Fetching todo turns for user: {user_id}")
        response = await supabase.from_("todo_turns")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("timestamp", desc=False)\
            .execute()
        
        if hasattr(response, "error") and response.error:
            logger.error(f"Error querying todo_turns: {response.error}")
            sys.exit(1)
        
        todo_turns = response.data
        logger.info(f"Found {len(todo_turns)} todo turns")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"todo_state_{user_id}_{timestamp}.json"
        
        # Save to JSON file
        with open(filename, "w") as f:
            json.dump(todo_turns, f, indent=2, default=str)
        
        logger.info(f"Saved todo state to {filename}")
        print(f"Successfully saved {len(todo_turns)} todo turns to {filename}")
        
    except Exception as e:
        logger.error(f"Error saving todo state: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python save-todo-state.py <user_id>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    asyncio.run(save_todo_state(user_id))


if __name__ == "__main__":
    main()