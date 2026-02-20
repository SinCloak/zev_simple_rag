> ## Documentation Index
> Fetch the complete documentation index at: https://docs.trychroma.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete Data

> Learn how to delete data from Chroma collections.

export const Danger = ({title, children}) => <div className="my-6">
    <div className="relative pr-1.5 pb-1.5">
      <div className="absolute top-1.5 left-1.5 right-0 bottom-0 bg-red-500" />
      <div className="relative border border-black dark:border-white px-5 py-4 bg-white dark:bg-neutral-900">
        {title && <p className="block mb-2"><strong>{title}</strong></p>}
        {children}
      </div>
    </div>
  </div>;

Chroma supports deleting items from a collection by `id` using `.delete`. The embeddings, documents, and metadata associated with each item will be deleted.

<Danger>
  Naturally, this is a destructive operation, and cannot be undone.
</Danger>

<CodeGroup>
  ```python Python theme={null}
  collection.delete(
      ids=["id1", "id2", "id3",...],
  )
  ```

  ```typescript TypeScript theme={null}
  await collection.delete({
      ids: ["id1", "id2", "id3",...],
  })
  ```

  ```rust Rust theme={null}
  collection.delete(
      Some(vec!["id1".to_string(), "id2".to_string(), "id3".to_string()]),
      None,
  ).await?;
  ```
</CodeGroup>

`.delete` also supports the `where` filter. If no `ids` are supplied, it will delete all items in the collection that match the `where` filter.

<CodeGroup>
  ```python Python theme={null}
  collection.delete(
      ids=["id1", "id2", "id3",...],
  	where={"chapter": "20"}
  )
  ```

  ```typescript TypeScript theme={null}
  await collection.delete({
      ids: ["id1", "id2", "id3",...], //ids
      where: {"chapter": "20"} //where
  })
  ```

  ```rust Rust theme={null}
  use chroma::types::{MetadataComparison, MetadataExpression, MetadataValue, PrimitiveOperator, Where};

  let where_clause = Where::Metadata(MetadataExpression {
      key: "chapter".to_string(),
      comparison: MetadataComparison::Primitive(
          PrimitiveOperator::Equal,
          MetadataValue::Str("20".to_string()),
      ),
  });

  collection.delete(
      Some(vec!["id1".to_string(), "id2".to_string(), "id3".to_string()]),
      Some(where_clause),
  ).await?;
  ```
</CodeGroup>
