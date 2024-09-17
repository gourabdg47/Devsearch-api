# DevSearch API

DevSearch API is a powerful search engine API service that provides structured data from web searches. It offers customizable search verticals, AI-powered features, and developer-friendly tools.

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- Basic search results in JSON format
- Customizable search verticals
- AI-powered content summarization
- Multi-lingual support
- Real-time trending topics
- Developer-friendly features (SDKs, documentation)

## Project Structure

devsearch-api/
├── api/
│ ├── main.py
│ ├── config.py
│ ├── dependencies.py
│ ├── db/
│ │ └── database.py
│ ├── models/
│ │ ├── custom_vertical.py
│ │ └── search_result.py
│ ├── routers/
│ │ ├── search.py
│ │ ├── custom_verticals.py
│ │ └── ai_features.py
│ └── services/
│ ├── search_engine.py
│ ├── custom_vertical_service.py
│ └── ai_service.py
├── alembic/
│ ├── env.py
│ └── versions/
├── tests/
│ └── db_test.py
├── alembic.ini
└── requirements.txt


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/devsearch-api.git
   cd devsearch-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database and run migrations:
   ```
   alembic upgrade head
   ```

## Configuration

1. Create a `.env` file in the project root and add the following variables:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/devsearch
   ELASTICSEARCH_URL=http://localhost:9200
   SECRET_KEY=your_secret_key
   SEARCH_API_KEY=your_search_api_key
   CUSTOM_SEARCH_ENGINE_ID=your_custom_search_engine_id
   ```

2. Update the `api/config.py` file if you need to change any default settings.

## Usage

To run the application:

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /api/v1/search/`: Perform a search
- `POST /api/v1/custom/`: Create a custom vertical
- `GET /api/v1/custom/`: List custom verticals
- `GET /api/v1/custom/{vertical_id}`: Get a specific custom vertical
- `GET /api/v1/ai/summarize`: Summarize text using AI

For detailed API documentation, visit `http://localhost:8000/docs` after starting the server.

## Testing

To run the database connection test:

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [MIT License](https://github.com/gourabdg47/Devsearch-api/blob/master/LICENSE) file for details.