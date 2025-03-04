# NHS Healthcare Explorer

An interactive learning platform for NHS data scientists to understand healthcare systems, clinical processes, and best practices.

## About This Project

NHS Healthcare Explorer is a Flask-based web application designed for NHS data scientists to learn about the healthcare context in which their data exists. It provides domain-specific knowledge modules, interactive resources, and an AI assistant to help data scientists who may not have clinical backgrounds better understand the NHS environment.

## Features

- **Learning Domains**: Organized content around key healthcare knowledge areas
- **Interactive Modules**: Structured learning modules with questions, resources, and activities
- **AI Assistant**: Context-aware AI helper to answer questions about NHS systems and data
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Toggle between light and dark themes

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/nhs-healthcare-explorer.git
cd nhs-healthcare-explorer
```

2. Set up a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install flask
```

4. Run the application
```bash
python app.py
```

5. Open a browser and navigate to http://127.0.0.1:5000/

## Demo Presentation Setup

For hackathon demos, you can use Ngrok to create a temporary public URL:

1. Download [Ngrok](https://ngrok.com/download) and extract it
2. Run your Flask app: `python app.py`
3. In another terminal, run: `./ngrok http 5000`
4. Share the provided URL with judges and team members

## Future Development

- Additional domain content for more specialized areas
- Integration with NHS data tools and APIs
- User authentication for progress tracking
- Content contribution system for domain experts
- Expanded AI assistant capabilities

## Technologies Used

- Flask (Python web framework)
- HTML/CSS for frontend
- JavaScript for interactivity
- Ollama API for AI assistant (commented out in demo mode)

## Team

- Rosemary Walmsley
- Callum Cockburn
- Matt Mort
- Matt Hayden
- Stephanie Hanna
- Richard Allan
- Tom
- Hamish Graham

## License

This project is created for demonstration purposes as part of the [Cardiff 2025 NHS Hackathon](https://nhshackday.com/projects/28-cardiff/healthcare_wayfinder)

## Acknowledgments

Content is based on the NHS Data Scientist upskilling course materials.
