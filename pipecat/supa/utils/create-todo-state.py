#!/usr/bin/env python3

import sys
import json
import asyncio
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from supabase import acreate_client, AsyncClient
from loguru import logger

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


async def create_todo_state(user_id: str, filename: str) -> None:
    """
    Create todo state for a new user from a JSON file.
    
    Args:
        user_id: The user ID to create todo turns for
        filename: The JSON file containing todo turns to import
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Missing SUPABASE_URL or SUPABASE_KEY in environment")
        sys.exit(1)
    
    try:
        # Create Supabase client
        supabase: AsyncClient = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Check if user_id already exists in todo_turns
        logger.info(f"Checking if user_id '{user_id}' already exists")
        check_response = await supabase.from_("todo_turns")\
            .select("user_id")\
            .eq("user_id", user_id)\
            .limit(1)\
            .execute()
        
        if hasattr(check_response, "error") and check_response.error:
            logger.error(f"Error checking existing user: {check_response.error}")
            sys.exit(1)
        
        if check_response.data:
            logger.error(f"User ID '{user_id}' already exists in todo_turns table")
            print(f"Error: User ID '{user_id}' already has todo turns. Cannot create duplicate entries.")
            sys.exit(1)
        
        # Read JSON file
        logger.info(f"Reading todo turns from {filename}")
        try:
            with open(filename, "r") as f:
                todo_turns = json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file: {e}")
            print(f"Error: Invalid JSON in file '{filename}'")
            sys.exit(1)
        
        if not isinstance(todo_turns, list):
            logger.error("JSON file must contain a list of todo turns")
            print("Error: JSON file must contain a list of todo turns")
            sys.exit(1)
        
        logger.info(f"Found {len(todo_turns)} todo turns to import")
        
        # Update user_id for all turns
        for turn in todo_turns:
            turn["user_id"] = user_id
        
        # Insert todo turns in batches to avoid hitting API limits
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(todo_turns), batch_size):
            batch = todo_turns[i:i + batch_size]
            logger.info(f"Inserting batch {i//batch_size + 1} ({len(batch)} records)")
            
            insert_response = await supabase.from_("todo_turns")\
                .insert(batch)\
                .execute()
            
            if hasattr(insert_response, "error") and insert_response.error:
                logger.error(f"Error inserting batch: {insert_response.error}")
                print(f"Error inserting records: {insert_response.error}")
                sys.exit(1)
            
            total_inserted += len(batch)
        
        logger.info(f"Successfully inserted {total_inserted} todo turns")
        print(f"Successfully created todo state for user '{user_id}' with {total_inserted} turns")
        
    except Exception as e:
        logger.error(f"Error creating todo state: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python create-todo-state.py <user_id> <filename>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    filename = sys.argv[2]
    asyncio.run(create_todo_state(user_id, filename))


if __name__ == "__main__":
    main()