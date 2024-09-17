import asyncio
import asyncpg

async def check_db_connection():
    connection_string = "postgresql+asyncpg://devsearch:root@localhost/devsearch"
    
    # Remove the 'asyncpg+' prefix as asyncpg doesn't use it
    connection_string = connection_string.replace('postgresql+asyncpg://', 'postgresql://')
    
    try:
        # Attempt to establish a connection
        conn = await asyncpg.connect(connection_string)
        
        # Execute a simple query
        version = await conn.fetchval('SELECT version()')
        
        print(f"Successfully connected to the database.")
        print(f"PostgreSQL version: {version}")
        
        # Close the connection
        await conn.close()
        
    except asyncpg.exceptions.PostgresError as e:
        print(f"Error connecting to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the async function
asyncio.run(check_db_connection())