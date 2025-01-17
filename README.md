# Oh Kale No Backend

Django backend for Oh Kale No, a wellness application that encourages healthy choices through playful, vegetable-themed interactions.

## Tech Stack

- Django REST Framework
- PostgreSQL (via Neon DB)
- Anthropic's Claude 3 Sonnet for AI responses
- Python 3.11+
- Deployed on Render

## API Endpoints

### Core Endpoints

- `GET /core/visit-count/` - Get current visitor count
- `POST /core/increment-visit/` - Increment visitor count
- `POST /core/get-claude-response/` - Get AI response for user input
- `GET /core/get-csrf-token/` - Get CSRF token for secure requests

## Local Development

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with:
ANTHROPIC_API_KEY=your_api_key
DATABASE_URL=your_database_url
DJANGO_SECRET_KEY=your_secret_key
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Security

- CSRF protection enabled for all POST requests
- CORS configured for specific origins
- Environment variables for sensitive data
- Secure cookie handling
- Cross-origin resource sharing with credentials

## Database Schema

### VisitCounter
- `count` (IntegerField): Tracks total site visits
- `last_updated` (DateTimeField): Timestamp of last update

## Deployment

The application is deployed on Render with the following configuration:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn ohkaleno_project.wsgi:application`
- Environment: Python 3.11
- Database: Neon PostgreSQL

## Related Repositories

- Frontend: [oh-kale-no](https://github.com/lana-z/oh-kale-no)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if applicable)
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
