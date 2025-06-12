from fastmcp import FastMCP, Client
import tools.retrieve as retrieve
import tools.google_search as gs
import tools.vectorize as vectorize

mcp = FastMCP('HOA-mcp-server', json_response=True, stateless_http=True)

@mcp.tool
def retrieve_context(prompt: str) -> str:
    """Retrieves HOA Document context."""
    print('tool called')
    r_list = retrieve.retrieve(prompt)
    r_str = ''
    for r in r_list:
        r_str += r[0]
    return r_str

@mcp.tool
async def google_search(query: str) -> str:
    """Google searches the prompt"""
    return await gs.async_google_search(query)

@mcp.tool
def update_context():
    """Update HOA document context"""
    vectorize.vectorize()
    return f"The HOA documents context have been updated."

def main():
    mcp.run(transport='streamable-http', host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()
    
# client = Client(mcp)

# async def call_tool(prompt: str):
#     async with client:
#         result = await client.call_tool("retrieve_context", {"prompt": prompt})
#         print(result)

# asyncio.run(call_tool("hi"))