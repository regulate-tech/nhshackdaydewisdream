from flask import Flask, render_template, request, jsonify
import json

# Comment out the following line if Ollama is not installed or available
# import ollama

app = Flask(__name__)


# NHS Domain Knowledge
with open("./text_content.json", "r", encoding="utf-8") as json_data:
    nhs_domains = json.load(json_data)
    json_data.close()


# domain.key_metrics


# Routes must come AFTER the nhs_domains variable is defined
@app.route("/")
def index():
    """Home page showing all domains/themes"""
    return render_template("index.html", domains=nhs_domains)


@app.route("/domain/<domain_id>")
def domain_detail(domain_id):
    """Domain detail page showing modules in a specific domain"""
    if domain_id in nhs_domains:
        return render_template(
            "domain_detail.html", domain=nhs_domains[domain_id], domain_id=domain_id
        )
    else:
        return render_template("404.html"), 404


@app.route("/domain/<domain_id>/module/<int:module_number>")
def module_detail(domain_id, module_number):
    """Module detail page showing overview of a specific module"""
    if domain_id in nhs_domains:
        # Find the specific module
        module = next(
            (
                m
                for m in nhs_domains[domain_id]["modules"]
                if m["module_number"] == module_number
            ),
            None,
        )

        if module:
            return render_template(
                "module_detail.html",
                domain=nhs_domains[domain_id],
                domain_id=domain_id,
                module=module,
            )

    return render_template("404.html"), 404


@app.route("/domain/<domain_id>/module/<int:module_number>/content")
def module_content(domain_id, module_number):
    """Content page showing detailed content for a specific module"""
    if domain_id in nhs_domains:
        # Find the specific module
        module = next(
            (
                m
                for m in nhs_domains[domain_id]["modules"]
                if m["module_number"] == module_number
            ),
            None,
        )

        if module:
            return render_template(
                "content_detail.html",
                domain=nhs_domains[domain_id],
                domain_id=domain_id,
                module=module,
            )

    return render_template("404.html"), 404


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """API endpoint for AI assistant chat functionality"""
    data = request.json
    user_message = data.get("message", "")
    domain_context = data.get("domain", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Create system prompt with domain context if provided
        system_content = """You are an NHS data science assistant chatbot.
You provide helpful, accurate, and concise information about NHS data, systems, and healthcare analytics.
When suggesting approaches, prioritize NHS-approved methods and technologies.
Include references to NHS Digital standards and frameworks when relevant.
Always clarify you are an AI assistant providing general information, not specific implementation advice."""

        # Add domain-specific context if a domain was specified
        if domain_context and domain_context in nhs_domains:
            domain_info = nhs_domains[domain_context]
            system_content += f"\n\nYou are currently helping with questions about {domain_info['title']}: {domain_info['description']}."

        # Try using ollama, but fall back to a mock response if not available
        try:
            # Uncomment the following if Ollama is available
            """
            messages = [
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
            response = ollama.chat(model='llama3', messages=messages)
            bot_response = response['message']['content']
            """
            # Mock response for demo
            bot_response = f"This is a simulated AI response about '{user_message}'. In a real implementation, this would connect to an LLM like Ollama."
            if domain_context:
                bot_response += f"\n\nI'm specifically focusing on {nhs_domains[domain_context]['title']} context in this response."
        except Exception as e:
            print(f"Error with AI response: {str(e)}")
            # Fallback response
            bot_response = "I'm sorry, I couldn't connect to the language model. Please ensure Ollama is running with the llama3 model."

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
