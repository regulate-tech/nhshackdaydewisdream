from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import os
import ollama  # Make sure to install using: pip install ollama

app = Flask(__name__)

# NHS Domain Knowledge
nhs_domains = {
    "healthcare_system": {
        "title": "How Healthcare Works",
        "description": "Understanding the structure and organization of healthcare systems",
        "suggested_questions": [
            "How is the NHS structured at national, regional, and local levels?",
            "What are the key differences between primary, secondary, and tertiary care?",
            "How do referral pathways work between different parts of the system?",
            "What are Integrated Care Systems and how do they operate?",
            "How does information flow between different healthcare providers?"
        ],
        "key_metrics": ["NHS organizational structure", "Healthcare policy and governance", "Patient pathways", "Data sharing frameworks"],
        "relevant_data_sources": ["NHS England", "Department of Health", "Integrated Care Boards", "Healthcare regulators"],
    },
    "humans_in_healthcare": {
        "title": "Humans in Healthcare",
        "description": "Understanding patient and staff experiences in healthcare settings",
        "suggested_questions": [
            "How do patients typically navigate the healthcare system?",
            "What are the main barriers to healthcare access for different demographics?",
            "How do healthcare professionals communicate across specialties?",
            "What impacts do staffing levels have on patient outcomes?",
            "How does digital literacy affect healthcare engagement?"
        ],
        "key_metrics": ["Patient experience measures", "Staff wellbeing frameworks", "Health literacy concepts", "Equity and access principles"],
        "relevant_data_sources": ["Patient representatives", "Healthcare staff", "Human resources", "Community engagement teams"],
    },
    "clinical_healthcare": {
        "title": "Clinical Healthcare",
        "description": "Understanding medical procedures, treatments, and clinical processes",
        "suggested_questions": [
            "How do blood tests work from request to results?",
            "What happens during the patient journey through surgery?",
            "How are medical conditions coded and classified?",
            "What technology is used in diagnostic imaging?",
            "How are medication safety checks implemented?"
        ],
        "key_metrics": ["Clinical pathways", "Medical testing processes", "Treatment protocols", "Clinical coding systems"],
        "relevant_data_sources": ["Clinical directors", "Laboratory departments", "Pharmacy teams", "Medical records specialists"],
    },
    "healthcare_finance": {
        "title": "Money in Healthcare",
        "description": "Understanding healthcare funding, budgeting, and resource allocation",
        "suggested_questions": [
            "How are NHS services commissioned and paid for?",
            "What financial incentives exist in different parts of the system?",
            "How are business cases for new services evaluated?",
            "What metrics determine resource allocation decisions?",
            "How are healthcare costs benchmarked across organizations?"
        ],
        "key_metrics": ["Healthcare funding models", "Commissioning frameworks", "Financial reporting standards", "Cost-effectiveness analysis"],
        "relevant_data_sources": ["Finance directors", "Commissioning teams", "Health economists", "Service planners"],
    },
    "healthcare_system_participation": {
        "title": "Being Part of a Healthcare System",
        "description": "Understanding how to effectively work within and contribute to healthcare",
        "suggested_questions": [
            "How are improvement projects typically structured in healthcare?",
            "What governance processes apply to research and innovation?",
            "How are data projects approved and implemented?",
            "What skills are most valued for data scientists in healthcare?",
            "How can analytical work be effectively communicated to clinical teams?"
        ],
        "key_metrics": ["Project management frameworks", "Change management approaches", "Knowledge sharing platforms", "Stakeholder engagement strategies"],
        "relevant_data_sources": ["Transformation teams", "Clinical informaticians", "Research offices", "Digital innovation hubs"],
    }
}

@app.route('/')
def index():
    return render_template('index.html', domains=nhs_domains)

@app.route('/domain/<domain_id>')
def domain_detail(domain_id):
    if domain_id in nhs_domains:
        return render_template('domain_detail.html', domain=nhs_domains[domain_id], domain_id=domain_id)
    else:
        return render_template('404.html'), 404

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_message = data.get('message', '')
    domain_context = data.get('domain', '')
    
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
            system_content += f"\nRelevant data sources include: {', '.join(domain_info['relevant_data_sources'])}."
            system_content += f"\nKey metrics for this domain include: {', '.join(domain_info['key_metrics'])}."
        
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
        
        # Try using ollama, but fall back to a mock response if not available
        try:
            response = ollama.chat(model='llama3', messages=messages)
            bot_response = response['message']['content']
        except Exception as e:
            print(f"Error using ollama: {str(e)}")
            # Fallback response
            bot_response = "I'm sorry, I couldn't connect to the language model. Please ensure Ollama is running with the llama3 model."
            
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/api/domains')
def get_domains():
    return jsonify(nhs_domains)

if __name__ == '__main__':
    app.run(debug=True)