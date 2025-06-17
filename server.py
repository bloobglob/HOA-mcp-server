from fastmcp import FastMCP, Client
import tools.retrieve as retrieve
import tools.google_search as gs
import tools.vectorize as vectorize

mcp = FastMCP('HOA-mcp-server', json_response=True, stateless_http=True)

@mcp.tool
def retrieve_context(text: str) -> str:
    """Retrieves HOA Document context."""
    print('tool called')
    r_list = retrieve.retrieve(text)
    r_str = ''
    for r in r_list:
        r_str += r[0]
    return r_str

@mcp.tool
async def google_search(text: str) -> str:
    """Google searches the prompt"""
    return await gs.async_google_search(text)

@mcp.tool
def update_context(text: str):
    print(text)
    """Update HOA document context"""
    if text != '':
        with open(f'data/{text[0:20]}.txt', 'w') as f:
            f.write(text)
        vectorize.vectorize(f'{text[0:20]}.txt')
        return f"The HOA documents context have been updated."
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