# RabbitMQ Patterns

## Overview

When integrating with RabbitMQ in this project, follow these patterns for exchange usage, serialization, and acknowledgment.

## Exchange types

- **Direct**: Route by routing key; one-to-one or fan-out to matching queues.
- **Topic**: Route by pattern (e.g. `logs.*.error`); useful for event categories.
- **Fanout**: Broadcast to all bound queues; no routing key.
- **Headers**: Route by message headers; use when routing key is not enough.

Choose the exchange type that matches your routing and scaling needs.

## Serialization

- Use a consistent format (e.g. JSON) for message bodies.
- Validate or parse payloads before use; handle invalid messages without crashing the consumer.
- Document the schema or provide a shared DTO/model for producers and consumers.

## Ack handling

- **Ack** a message only after processing completes successfully (e.g. after DB write or downstream call).
- **Nack** (or reject) with `requeue=False` for poison messages so they do not block the queue; consider a dead-letter setup.
- **Nack** with `requeue=True` only for transient failures (e.g. temporary network error); be cautious to avoid tight retry loops.
- Prefer explicit ack/nack over auto-ack when processing has side effects.

## Checklist

- Choose the correct exchange type and binding keys.
- Serialize/deserialize consistently and handle errors.
- Ack after success; nack poison messages without requeue; use dead-letter if needed.
