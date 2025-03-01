from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import os
import ollama  # Make sure to install using: pip install ollama

app = Flask(__name__)

# NHS Domain Knowledge
nhs_domains = {
    "patient_records": {
        "title": "Patient Records & EHR",
        "description": "Electronic health records and patient data management",
        "suggested_questions": [
            "What are the data quality issues with the patient record system?",
            "How can we identify and resolve duplicate patient records?",
            "What percentage of patient records are missing key demographic information?",
            "How do clinicians currently document patient interactions?",
            "What are the main data fields captured during patient registration?"
        ],
        "key_metrics": ["Records completeness", "Data quality score", "Duplication rate"],
        "relevant_data_sources": ["EMIS", "TPP SystmOne", "Lorenzo", "Cerner"],
    },
    "population_health": {
        "title": "Population Health",
        "description": "Analysis of health outcomes and risks across populations",
        "suggested_questions": [
            "What are the demographic profiles of high-risk patient groups?",
            "How do social determinants correlate with health outcomes in our region?",
            "What preventative interventions have the highest success rates?",
            "Which population segments are underutilizing preventative services?",
            "How do seasonal factors impact hospital admissions?"
        ],
        "key_metrics": ["Risk stratification accuracy", "Intervention effectiveness", "Population coverage"],
        "relevant_data_sources": ["Public Health England datasets", "ONS data", "Local authority data"],
    },
    "clinical_pathways": {
        "title": "Clinical Pathways",
        "description": "Analysis and optimization of care delivery processes",
        "suggested_questions": [
            "What are the bottlenecks in our current cancer treatment pathway?",
            "How do variations in clinical pathways impact patient outcomes?",
            "Which steps in the care pathway have the highest resource utilization?",
            "What is the average delay between referral and first treatment?",
            "How do pathway compliance rates correlate with readmission rates?"
        ],
        "key_metrics": ["Pathway adherence", "Treatment delays", "Resource utilization"],
        "relevant_data_sources": ["Patient journey tracking systems", "Hospital episode statistics"],
    },
    "operational_efficiency": {
        "title": "Operational Efficiency",
        "description": "Resource planning, scheduling, and service optimization",
        "suggested_questions": [
            "What are the patterns of A&E attendance that could inform staffing levels?",
            "How can we optimize bed allocation based on historical demand?",
            "What are the primary causes of surgical cancellations?",
            "How does staff-to-patient ratio impact care quality metrics?",
            "What are the predictive factors for high-demand periods?"
        ],
        "key_metrics": ["Wait times", "Resource utilization", "Service throughput"],
        "relevant_data_sources": ["Hospital management systems", "Staff scheduling systems", "Patient flow data"],
    },
    "prescribing_patterns": {
        "title": "Prescribing Patterns",
        "description": "Analysis of medication prescribing and dispensing",
        "suggested_questions": [
            "What are the prescribing patterns for antibiotics across different GP practices?",
            "How does formulary adherence vary across the region?",
            "What is the uptake of biosimilars compared to originator products?",
            "How does seasonal variation affect prescribing of certain medications?",
            "What are the geographical patterns in high-cost drug prescribing?"
        ],
        "key_metrics": ["Formulary adherence", "Prescription costs", "Appropriate prescribing rates"],
        "relevant_data_sources": ["OpenPrescribing", "ePACT2", "Local formulary data"],
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