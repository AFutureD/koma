# koma

![exmaple](.github/example.png)

## Overview

Notice: This project is still in development.

This project(`koma`) is designed to help users search for information on macOS.

Specifically thanks to the [apple_cloud_notes_parser](https://github.com/threeplanetssoftware/apple_cloud_notes_parser) and [neon](https://neon.tech).


## Feature

- [x] [core] List all notes from Notes.app;
- [x] [core] Convert all notes into markdown;
- [ ] [core] Get a specific note;
- [ ] [core] Create a note using AppleScript;
- [x] [api ] Incremental index all notes and its paragraphs;
- [x] [api ] Semantic query in both json and plain text;
- [ ] [api ] Summrize similar content;
- [ ] [api ] Automatic sync Apple notes.

## Usage 

### As a data connector in RAG platform.

By using OpenAPI this is easy to intergate into any rag platform, such as [Dify](https://dify.ai).

In Dify, goto [Tools](https://cloud.dify.ai/tools?category=api) and create one using `<Your Domain>/api/openapi.json`.

### Raycast

TODO.

## Install

### Step 0: Prepare

1. You have [pdm](https://pdm-project.org/en/stable/) and [uvicorn](https://www.uvicorn.org) installed.
2. Your Terminal or Docker have [Full Disk Access](https://www.perplexity.ai/search/How-to-enable-mOAW4vpVRlmeMvtg6EjnNw) permission.
3. Your Apple Notes.app folder is `~/Library/Group Containers/group.com.apple.notes`
4. Configure the `.env`

### Step 1: download this project

```
> git clone https://github.com/AFutureD/koma.git
```

### Step 2: Install dependencies.

```
> cd koma
> pdm sync
```

### Step 3: Run server

```
> pdm run django_manage migrate rag
> uvicorn agent.asgi:application --host 0.0.0.0 --env-file ./.env
```




