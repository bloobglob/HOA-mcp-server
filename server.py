from fastmcp import FastMCP
import retrieve

mcp = FastMCP('HOA-mcp-server', json_response=True)

@mcp.tool
def retrieve_context(prompt: str) -> str:
    """Retrieves HOA Document context."""
    print('tool called')
    r_list = retrieve.retrieve(prompt)
    r_str = ''
    for r in r_list:
        r_str += r[0]
    return r_str

def main():
    mcp.run(transport='sse', host='127.0.0.1', port=8000)

if __name__ == "__main__":
    main()
    
# client = Client(mcp)

# async def call_tool(prompt: str):
#     async with client:
#         result = await client.call_tool("retrieve_context", {"prompt": prompt})
#         print(result)

# asyncio.run(call_tool("hi"))