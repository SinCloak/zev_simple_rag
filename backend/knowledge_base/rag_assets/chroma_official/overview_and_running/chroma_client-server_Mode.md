> ## Documentation Index
> Fetch the complete documentation index at: https://docs.trychroma.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Client-Server Mode

> Learn how to run Chroma in client-server mode.

Chroma can also be configured to run in client/server mode. In this mode, the Chroma client connects to a Chroma server running in a separate process.

To start the Chroma server, run the following command:

```bash  theme={null}
chroma run --path /db_path
```

<Tabs>
  <Tab title="Python" icon="python">
    Then use the Chroma `HttpClient` to connect to the server:

    ```python  theme={null}
    import chromadb

    chroma_client = chromadb.HttpClient(host='localhost', port=8000)
    ```

    That's it! Chroma's API will run in `client-server` mode with just this change.

    Chroma also provides the async HTTP client. The behaviors and method signatures are identical to the synchronous client, but all methods that would block are now async. To use it, call `AsyncHttpClient` instead:

    ```python  theme={null}
    import asyncio
    import chromadb

    async def main():
        client = await chromadb.AsyncHttpClient()

        collection = await client.create_collection(name="my_collection")
        await collection.add(
            documents=["hello world"],
            ids=["id1"]
        )

    asyncio.run(main())
    ```

    If you [deploy](../../guides/deploy/client-server-mode) your Chroma server, you can also use our [http-only](../../guides/deploy/python-thin-client) package.
  </Tab>

  <Tab title="TypeScript" icon="js">
    Then you can connect to it by instantiating a new `ChromaClient`:

    ```typescript  theme={null}
    import { ChromaClient } from "chromadb";

    const client = new ChromaClient();
    ```

    If you run your Chroma server using a different configuration, or [deploy](../../guides/deploy/client-server-mode) your Chroma server, you can specify the `host`, `port`, and whether the client should connect over `ssl`:

    ```typescript  theme={null}
    import { ChromaClient } from "chromadb";

    const client = new ChromaClient({
      host: "YOUR-HOST",
      port: "YOUR-PORT",
      ssl: true,
    });
    ```
  </Tab>

  <Tab title="Rust" icon="rust">
    You can connect to it by instantiating a new `ChromaHttpClient`:

    ```rust  theme={null}
    let options = ChromaHttpClientOptions {
        endpoint: "http://localhost:8000".parse()?,
        ..Default::default()
    };
    let client = ChromaHttpClient::new(options);
    ```
  </Tab>
</Tabs>
