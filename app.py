from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

# Comment out the following line if Ollama is not installed or available
# import ollama

app = Flask(__name__)


#domain.key_metrics


# NHS Domain Knowledge based on the provided document
nhs_domains = {
    "how_healthcare_works": {

        "title": "How Healthcare Works",
        "key_metrics" : ["Organizational Structure", "Data Governance", "System Mapping"],
        "description": "Understanding the structure and organization of healthcare systems",
        "modules": [
            {
                "module_number": 1,
                "module_name": "Structure of the NHS",
                "module_learning_outcomes": "1. Understand the overall structure of health and care systems in the UK\n2. Learn about the identifiers for and directories of health and care organisations\n3. Achieve a sense of the size and scale of different organisations providing care",
                "description": "This module provides a comprehensive overview of the NHS structure, from national bodies to local service delivery. You'll explore the complex relationships between different organizations within the health and social care system, including NHS England, Integrated Care Systems (ICSs), NHS Trusts, Primary Care Networks, and the various regulatory bodies.",
                "why_this_matters": "Understanding the NHS structure is fundamental for data scientists as it provides context for data flows, governance requirements, and organizational priorities. This knowledge helps you identify key stakeholders for your projects and understand where and how data is generated, collected, and used across the system.",
                "questions": [
                    "How do Integrated Care Systems differ from the previous commissioning structures?",
                    "What are the key identifiers used for NHS organizations and how are they maintained?",
                    "What is the relationship between NHS Digital (now part of NHS England) and local NHS Trusts?",
                    "How are primary care services structured and what implications does this have for data collection?"
                ],
                "content_urls": [
                    {"title": "NHS England: Who We Are", "url": "https://www.england.nhs.uk/about/"},
                    {"title": "The King's Fund: Structure of the NHS in England", "url": "https://www.kingsfund.org.uk/audio-video/how-does-nhs-in-england-work"},
                    {"title": "NHS Digital Organization Data Service", "url": "https://digital.nhs.uk/services/organisation-data-service"},
                    {"title": "Understanding Integrated Care Systems", "url": "https://www.england.nhs.uk/integratedcare/what-is-integrated-care/"}
                ],
                "activities": [
                    "Map out the NHS organizations in your local area and identify their relationships",
                    "Complete the interactive NHS structure learning tool (available on NHS Learning Hub)",
                    "Interview a colleague from a different part of the NHS to understand their organizational context"
                ]
            },
            {
                "module_number": 2,
                "module_name": "Flow in a Healthcare System",
                "module_learning_outcomes": "1. Recognise the digital and non-digital sources of data that can feed into healthcare data analyses\n2. Recognise some potential limitations of summary codes and recognise the potential for a data subject to cross organisational and data silo boundaries\n3. Understand the importance of getting a good understanding of the real world issue for analysis before selecting data/data-sets",
                "description": "This module explores how patients, information, and resources flow through the healthcare system. You'll learn about patient pathways, referral processes, and how these journeys are represented in data. The module highlights the challenges of tracking individuals across different care settings and the implications this has for data analysis.",
                "why_this_matters": "Healthcare data rarely exists in isolation. Understanding how patients move through the system and how their data is captured at different points is essential for meaningful analysis. This knowledge helps you identify potential data quality issues, recognize when data might be missing, and understand the context behind the numbers.",
                "questions": [
                    "What happens to patient data when they are referred from primary to secondary care?",
                    "How might a patient's journey be represented differently in different datasets?",
                    "What are common data quality issues that arise from patients moving between care settings?",
                    "How can you identify and address potential blind spots in your analysis due to care boundaries?"
                ],
                "content_urls": [
                    {"title": "NHS Data Model and Dictionary", "url": "https://www.datadictionary.nhs.uk/"},
                    {"title": "The King's Fund: Understanding Patient Flow in Hospitals", "url": "https://www.kingsfund.org.uk/publications/patient-flow-hospitals"},
                    {"title": "NHS Digital: Data Quality Maturity Index", "url": "https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/data-quality"},
                    {"title": "Healthcare Evaluation Data (HED): Patient Pathways", "url": "https://www.hed.nhs.uk/info/patientpathways.htm"}
                ],
                "activities": [
                    "Shadow a clinician for a day to observe how data is captured during patient care",
                    "Map a typical patient journey for a specific condition and identify all potential data capture points",
                    "Analyze a dataset to identify where patients might have crossed organizational boundaries",
                    "Design a visualization that represents patient flow through a care system"
                ]
            },
            {
                "module_number": 3,
                "module_name": "Intro to Healthcare Data Ontologies and Classification",
                "module_learning_outcomes": "1. Identify what healthcare data ontologies are and name the most common ones used in healthcare (like SNOMED CT and ICD-10)\n2. Explain in simple terms why healthcare needs standardized ways to organize medical information\n3. Recognize how healthcare data classification helps in storing and finding patient information in databases",
                "description": "This module introduces the structured vocabularies and coding systems used to standardize healthcare information. You'll learn about major classification systems including SNOMED CT, ICD-10, OPCS-4, Read Codes, and dm+d. The module covers the purpose, structure, and application of these systems, along with their strengths and limitations for data analysis.",
                "why_this_matters": "Healthcare terminologies are the foundation for consistent data capture and analysis. Understanding these coding systems is essential for extracting meaningful insights from clinical data, ensuring your analyses accurately reflect clinical realities, and communicating effectively with clinical colleagues.",
                "questions": [
                    "What are the key differences between SNOMED CT and ICD-10?",
                    "How does hierarchical classification in healthcare terminologies support different levels of analysis?",
                    "What challenges might arise when analyzing data coded using different classification systems?",
                    "How are medications and procedures coded in NHS systems?"
                ],
                "content_urls": [
                    {"title": "SNOMED International", "url": "https://www.snomed.org/snomed-ct/five-step-briefing"},
                    {"title": "NHS Digital: SNOMED CT", "url": "https://digital.nhs.uk/services/terminology-and-classifications/snomed-ct"},
                    {"title": "World Health Organization: ICD-10", "url": "https://www.who.int/standards/classifications/classification-of-diseases"},
                    {"title": "NHS Digital: Dictionary of Medicines and Devices", "url": "https://digital.nhs.uk/services/dictionary-of-medicines-and-devices"},
                    {"title": "NHS Digital: OPCS Classification of Interventions and Procedures", "url": "https://digital.nhs.uk/services/terminology-and-classifications/opcs-classification-of-interventions-and-procedures"}
                ],
                "activities": [
                    "Complete the SNOMED CT Foundation course",
                    "Practice coding scenarios using both ICD-10 and SNOMED CT to understand differences",
                    "Analyze a clinical dataset to identify patterns in coding practices",
                    "Create a simple ontology for a specific healthcare domain"
                ]
            }
        ]
    },
    "humans_in_healthcare": {
        "title": "Humans in Healthcare",
        "key_metrics": ["Patient Experience", "Staff Wellbeing", "Ethical Frameworks"],
        "description": "Understanding patient and staff experiences in healthcare settings",
        "modules": [
            {
                "module_number": 1,
                "module_name": "Intro to Healthcare Ethics",
                "module_learning_outcomes": "1. I can describe how to find out if the correct research and ethical approvals are in place for my project\n2. I understand who needs a certificate of GCP and have completed the training if it is required for my role\n3. I understand my responsibilities as an ethical user of data and how to work in a Trusted Research Environment",
                "description": "You should already have completed information governance training before accessing NHS data. Before you start analysing any data, it is important to understand where the data have come from, what type of data it is and what consent has been given for you to analyse it. This is because you may be dealing with confidential patient data or other data of a sensitive nature.",
                "why_this_matters": "Ethical data use is not just about compliance—it's about maintaining public trust in the NHS and ensuring that data science contributes positively to patient care and system improvement. Understanding the ethical frameworks helps you design analyses that respect patient rights and produce results that can be used with confidence.",
                "questions": [
                    "What is the difference between service evaluation, audit, and research?",
                    "How do you determine what type of ethical approval is needed for a data analysis project?",
                    "What special considerations apply when working with data from vulnerable populations?",
                    "How do you ensure data minimization while still conducting meaningful analysis?"
                ],
                "content_urls": [
                    {"title": "Health Data Research UK Learning Platform", "url": "https://hdruklearn.org/"},
                    {"title": "Accessing Health Data Course", "url": "https://hdruklearn.org/courses/course-v1:MRCRegulatorySupportCentre+AHD001+2024"},
                    {"title": "HRA: What Approvals Do I Need?", "url": "https://www.hra.nhs.uk/approvals-amendments/what-approvals-do-i-need/"},
                    {"title": "HRA Research Decision Tool Glossary", "url": "https://www.hra-decisiontools.org.uk/research/glossary.html"},
                    {"title": "HRA Research Decision Tool", "url": "https://www.hra-decisiontools.org.uk/research/"}
                ],
                "activities": [
                    "Complete the Good Clinical Practice (GCP) training if required for your role",
                    "Use the HRA decision-making tool to classify a project you're working on",
                    "Complete the Health Data Research UK's 'Accessing Health Data' course",
                    "Draft a data management plan for a current or upcoming project"
                ]
            },
            {
                "module_number": 2,
                "module_name": "Who are the People that Work in Healthcare?",
                "module_learning_outcomes": "1. List the main professional groups in healthcare and understand their different roles in patient care\n2. Recognize how various healthcare professionals interact with and contribute to healthcare data\n3. Identify the key stakeholders who might use the insights from your data analysis",
                "description": "This module introduces the diverse workforce that makes up the healthcare system. You'll learn about the roles and responsibilities of different healthcare professionals including doctors, nurses, allied health professionals, healthcare scientists, and non-clinical staff. The module emphasizes how different professionals interact with and contribute to healthcare data, and how their perspectives might influence data interpretation and use.",
                "why_this_matters": "Understanding who works in healthcare helps you identify key stakeholders for your data projects and tailor your approaches to their needs. Different professional groups have different priorities, workflows, and ways of engaging with data, so this knowledge helps you design more effective data solutions and communicate findings more appropriately.",
                "questions": [
                    "How do different healthcare professionals record and use data in their daily work?",
                    "What data-related challenges do different professional groups face?",
                    "How might the perspectives of different healthcare professionals influence the interpretation of data?",
                    "Which healthcare professionals should be involved in different types of data projects?"
                ],
                "content_urls": [
                    {"title": "NHS Careers", "url": "https://www.healthcareers.nhs.uk/explore-roles"},
                    {"title": "Royal College of Nursing: Professional Development", "url": "https://www.rcn.org.uk/professional-development"},
                    {"title": "British Medical Association: Doctors' Roles", "url": "https://www.bma.org.uk/advice-and-support/nhs-delivery-and-workforce/workforce/medical-staffing-in-england-report"},
                    {"title": "Allied Health Professionals Federation", "url": "https://www.ahpf.org.uk/AHP_roles.htm"},
                    {"title": "NHS Confederation: NHS Workforce", "url": "https://www.nhsconfed.org/publications/state-nhs-provider-sector"}
                ],
                "activities": [
                    "Shadow professionals from different healthcare roles to understand their work",
                    "Interview healthcare staff about their data needs and challenges",
                    "Map how different professional groups interact with data in a patient journey",
                    "Create a stakeholder analysis for a data project identifying relevant professional groups"
                ]
            },
            {
                "module_number": 3,
                "module_name": "Patient Experience and Healthcare Journeys",
                "module_learning_outcomes": "1. Explain what 'patient journey' means and why understanding it matters for healthcare data analysis\n2. Identify different touchpoints where patient data is collected throughout their healthcare experience\n3. Understand how patient-reported outcomes and experiences can be incorporated into healthcare data projects",
                "description": "This module explores healthcare from the patient's perspective, focusing on patient journeys, experiences, and reported outcomes. You'll learn about typical patient pathways through the healthcare system, how patient experience is measured and recorded, and approaches to incorporating patient perspectives into data projects. The module emphasizes the importance of seeing healthcare as a connected journey rather than isolated episodes.",
                "why_this_matters": "Patient experience is central to healthcare quality and should inform data science work. Understanding patient journeys helps you identify important data collection points, recognize potential gaps in data, and design analyses that reflect the reality of patient experiences rather than just organizational processes.",
                "questions": [
                    "How do patients typically navigate through different healthcare services?",
                    "What methods are used to capture patient experience and outcome data?",
                    "How can patient-reported data be integrated with clinical and administrative data?",
                    "What are the challenges in using patient-generated data for analysis?"
                ],
                "content_urls": [
                    {"title": "NHS England: Patient Experience", "url": "https://www.england.nhs.uk/ourwork/patient-participation/"},
                    {"title": "The Point of Care Foundation: Patient Experience", "url": "https://www.pointofcarefoundation.org.uk/resource/patient-experience/"},
                    {"title": "The King's Fund: Patient Experience and Patient-Centred Care", "url": "https://www.kingsfund.org.uk/topics/patient-experience"},
                    {"title": "NHS England: Friends and Family Test", "url": "https://www.england.nhs.uk/fft/"},
                    {"title": "NICE: Patient Experience in Adult NHS Services", "url": "https://www.nice.org.uk/guidance/qs15"}
                ],
                "activities": [
                    "Map a typical patient journey for a common condition, identifying data touchpoints",
                    "Analyze a set of patient feedback data (such as Friends and Family Test results)",
                    "Interview patients about their healthcare experiences and data sharing views",
                    "Design a data collection approach that incorporates patient-reported outcomes"
                ]
            }
        ]
    },
    "clinical_healthcare": {
        "title": "Clinical Healthcare",
        "key_metrics": ["Clinical Pathways", "Medical Coding", "Treatment Protocols"],
        "description": "Understanding medical procedures, treatments, and clinical processes",
        "modules": [
            {
                "module_number": 1,
                "module_name": "How Do Blood Tests Work?",
                "module_learning_outcomes": "1. Explain the purpose of common blood tests and interpret basic results using reference ranges to make informed decisions about their personal health\n2. Identify and interpret common medical abbreviations found in their NHS health records to better understand personal health information\n3. Describe the basic steps involved in the blood collection process",
                "description": "Blood test interpretation guides explain common laboratory tests including complete blood counts, liver function tests, and metabolic panels, detailing normal ranges and what abnormal results indicate clinically. Medical abbreviations in health records include standardised notations for conditions like HTN for hypertension, treatments such as ABx for antibiotics, and assessments like SOB for shortness of breath that healthcare professionals use to document patient care efficiently.",
                "why_this_matters": "For new NHS data scientists, understanding blood test interpretation provides essential context for analysing patient data and collaborating with clinical colleagues. Knowledge of medical abbreviations in health records prevents misinterpretation of the specialised shorthand prevalent in healthcare data. This clinical understanding enables more relevant analyses, better predictive modelling, and more effective communication of findings to healthcare professionals.",
                "questions": [
                    "Why do you think doctors often order blood tests even when you're feeling perfectly healthy?",
                    "How would you explain to a friend or family member why blood tests are an important part of healthcare?",
                    "Why do you think healthcare professionals use so many abbreviations? What are the benefits and drawbacks of this practice?",
                    "Why do you think different tests require different coloured tubes?",
                    "How would you explain the blood drawing process to a friend who's nervous about having their blood drawn?"
                ],
                "content_urls": [
                    {"title": "NHS: Blood Tests", "url": "https://www.nhs.uk/conditions/blood-tests/"},
                    {"title": "Geeky Medics: Blood Test Interpretation Guide", "url": "https://geekymedics.com/blood-test-interpretation-guide/"},
                    {"title": "NHS: Medical Record Abbreviations", "url": "https://www.nhs.uk/nhs-app/nhs-app-help-and-support/health-records-in-the-nhs-app/abbreviations-commonly-found-in-medical-records/"},
                    {"title": "NHS Blood Testing Video", "url": "https://www.youtube.com/watch?v=XBiwXSTSTdk"}
                ],
                "activities": [
                    "Draw a simple outline of a human body and label 5-6 organs that blood tests measure the function of",
                    "Create a simple chart matching tube colours to the types of tests they're used for",
                    "Practice explaining to a friend why blood tests are important in healthcare",
                    "Review common medical abbreviations and create a personal reference guide"
                ]
            },
            {
                "module_number": 2,
                "module_name": "What Types of Medical Specialities Might You See?",
                "module_learning_outcomes": "1. List at least 5 common medical specialties and briefly describe what each one does\n2. Understand the basic difference between primary care doctors and specialists\n3. Recognize how different medical professionals might use or need different types of data",
                "description": "This module introduces the diverse range of medical specialties in the healthcare system. You'll learn about major specialty areas such as cardiology, oncology, pediatrics, psychiatry, and surgery, along with their sub-specialties. The module explains how medical care is organized from primary care through to tertiary specialists, and how different specialties approach patient care and use health data in different ways.",
                "why_this_matters": "Understanding medical specialties provides essential context for working with healthcare data. Different specialties generate different types of data, use different coding systems, and have different analytical needs. This knowledge helps you communicate effectively with clinical colleagues and design analyses that are relevant to specific clinical contexts.",
                "questions": [
                    "How do primary, secondary, and tertiary care differ in their approaches to patient care?",
                    "What types of data are most important for different medical specialties?",
                    "How might the analytical needs of different specialties vary?",
                    "How do healthcare pathways connect different specialties for complex conditions?"
                ],
                "content_urls": [
                    {"title": "NHS: Medical Specialties", "url": "https://www.healthcareers.nhs.uk/explore-roles/doctors/roles-doctors/medicine"},
                    {"title": "Royal College of Physicians: Specialties", "url": "https://www.rcplondon.ac.uk/education-practice/advice/medical-specialties"},
                    {"title": "General Medical Council: Specialty Curricula", "url": "https://www.gmc-uk.org/education/standards-guidance-and-curricula/curricula"},
                    {"title": "British Medical Association: Hospital Doctors", "url": "https://www.bma.org.uk/advice-and-support/nhs-delivery-and-workforce/workforce/medical-staffing-in-england-report"},
                    {"title": "NHS Digital: Hospital Episode Statistics by Specialty", "url": "https://digital.nhs.uk/data-and-information/publications/statistical/hospital-admitted-patient-care-activity"}
                ],
                "activities": [
                    "Shadow clinicians from different specialties to observe their work",
                    "Compare data collection approaches across different specialty areas",
                    "Analyze specialty-specific datasets to identify characteristic patterns",
                    "Create a flowchart showing how patients might move between specialties"
                ]
            },
            {
                "module_number": 3,
                "module_name": "Why Do We Use Clinical Guidelines, and How Do They Work?",
                "module_learning_outcomes": "1. Explain what clinical guidelines are and why healthcare providers use them\n2. Identify how guidelines help standardize patient care across different healthcare settings\n3. Understand the basic connection between guidelines and the data collected during patient care",
                "description": "This module introduces clinical guidelines and their role in healthcare delivery. You'll learn about guideline development by organizations like NICE, how guidelines are implemented in practice, their relationship to clinical pathways and protocols, and how they influence both care delivery and data collection. The module covers the strengths and limitations of guidelines and their implications for data analysis.",
                "why_this_matters": "Clinical guidelines have a major influence on healthcare practice and the data that's collected. Understanding guidelines helps you interpret patterns in healthcare data, design analyses that align with clinical practice, and evaluate how closely actual care follows recommended standards. This knowledge is essential for producing clinically relevant insights.",
                "questions": [
                    "How are clinical guidelines developed and what evidence are they based on?",
                    "What factors influence whether clinicians follow guidelines in practice?",
                    "How can data be used to evaluate guideline adherence and impact?",
                    "What are the advantages and disadvantages of standardizing care through guidelines?"
                ],
                "content_urls": [
                    {"title": "NICE Guidelines", "url": "https://www.nice.org.uk/guidance"},
                    {"title": "Scottish Intercollegiate Guidelines Network (SIGN)", "url": "https://www.sign.ac.uk/"},
                    {"title": "BMJ: Clinical Guidelines", "url": "https://www.bmj.com/specialties/clinical-guidelines"},
                    {"title": "Guidelines in Practice", "url": "https://www.guidelinesinpractice.co.uk/"},
                    {"title": "NHS England: Clinical Pathways", "url": "https://www.england.nhs.uk/rightcare/what-is-nhs-rightcare/pathways/"}
                ],
                "activities": [
                    "Review a NICE guideline relevant to your work area",
                    "Compare a guideline to actual practice data to identify variations",
                    "Map how a guideline influences data collection points in a patient journey",
                    "Interview clinicians about their use of guidelines in daily practice"
                ]
            }
        ]
    },
    "money_in_healthcare": {
        "title": "Money in Healthcare",
        "key_metrics": ["Funding Models", "Performance Metrics", "Cost Analysis"],
        "description": "Understanding healthcare funding, budgeting, and resource allocation",
        "modules": [
            {
                "module_number": 1,
                "module_name": "Talking About the Economic Value of Healthcare",
                "module_learning_outcomes": "1. Define basic healthcare economic terms like 'cost-effectiveness' in simple language\n2. Identify the main ways healthcare services are paid for in the NHS\n3. Understand how data can help show whether healthcare services provide good value",
                "description": "This module introduces fundamental concepts in healthcare economics and financing. You'll learn about approaches to valuing healthcare interventions, payment systems in the NHS, economic evaluation methods including cost-effectiveness and cost-utility analysis, and how data supports economic decision-making. The module explains these concepts in accessible language for non-economists.",
                "why_this_matters": "Economic considerations are central to healthcare decision-making. Understanding healthcare economics helps you contribute to analyses that demonstrate value, support resource allocation decisions, and identify opportunities for efficiency. This knowledge ensures your data work addresses the financial realities of healthcare delivery.",
                "questions": [
                    "How do we determine whether a healthcare intervention provides good value?",
                    "What are the different ways healthcare providers are paid in the NHS?",
                    "How can data analysis contribute to improving the economic value of healthcare?",
                    "What are the advantages and disadvantages of different economic evaluation approaches?"
                ],
                "content_urls": [
                    {"title": "The Health Foundation: Healthcare Economics", "url": "https://www.health.org.uk/publications/the-economics-of-health-care"},
                    {"title": "NICE: Health Economics", "url": "https://www.nice.org.uk/process/pmg20/chapter/incorporating-economic-evaluation"},
                    {"title": "NHS England: NHS Payment System", "url": "https://www.england.nhs.uk/pay-syst/"},
                    {"title": "The King's Fund: How the NHS is Funded", "url": "https://www.kingsfund.org.uk/projects/nhs-in-a-nutshell/how-nhs-funded"},
                    {"title": "York Health Economics Consortium", "url": "https://yhec.co.uk/resources/glossary/"}
                ],
                "activities": [
                    "Calculate a simple cost-effectiveness analysis for a healthcare intervention",
                    "Analyze financial data for a healthcare service to identify cost drivers",
                    "Compare different payment approaches for the same healthcare service",
                    "Design a data collection approach to support economic evaluation"
                ]
            },
            {
                "module_number": 2,
                "module_name": "Measuring Healthcare Performance",
                "module_learning_outcomes": "1. Understand why metrics are used to measure healthcare performance\n2. Describe common ways that metrics can influence system behaviour, both positive and negative\n3. List key characteristics of good metrics and describe how these can be implemented in a healthcare context",
                "description": "Measuring healthcare performance is crucial for identifying and resolving service issues, targeting resources effectively, and tracking progress and improvement. However, metrics can sometimes lead to undesirable behaviors. Staff may focus on meeting metrics rather than achieving good patient outcomes, such as prioritizing patients close to breaching the A&E 4-hour wait target. Additionally, metrics can encourage resource hoarding, siloed working, and tribalism.",
                "why_this_matters": "Data scientists are often supporting teams and managers to develop metrics and measure system performance. You should be aware of how metrics can be damaging, and why careful thought around metrics is required to avoid unintended consequences.",
                "questions": [
                    "What metrics are used for health system performance assessment?",
                    "Why do metrics impact the way that clinicians, managers, and senior leaders organise and deliver their healthcare?",
                    "What do good metrics look like, and why are they successful in driving improvement?"
                ],
                "content_urls": [
                    {"title": "NHS How-to-guide for Measurement for Improvement", "url": "https://www.england.nhs.uk/improvement-hub/wp-content/uploads/sites/44/2017/11/How-to-Guide-for-Measurement-for-Improvement.pdf"},
                    {"title": "OECD Rethinking Health System Performance Assessment", "url": "https://www.oecd.org/en/publications/2024/01/rethinking-health-system-performance-assessment_c9e8ce53.html"},
                    {"title": "Unintended consequences of implementing a national performance measurement system into local practice", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3304045/"},
                    {"title": "UK Government How to set performance metrics for your service", "url": "https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service"}
                ],
                "activities": [
                    "Find out which metrics your local organisation uses to track performance of their healthcare systems",
                    "Evaluate these metrics for how they might affect the behaviour of employees at different levels of the system",
                    "Redesign one of these metrics to more effectively capture patient outcomes within it",
                    "Present your findings to colleagues and gather feedback"
                ]
            },
            {
                "module_number": 3,
                "module_name": "NHS Funding and Resource Allocation",
                "module_learning_outcomes": "1. Identify the main sources of NHS funding and how money flows through the healthcare system\n2. Understand basic NHS financial terminology and budgeting concepts relevant to data analysis projects\n3. Recognize how data insights can inform resource allocation decisions and help identify potential cost savings",
                "description": "This module explores the financial structure of the NHS and how resources are allocated. You'll learn about NHS funding sources, budget setting processes, financial flows between organizations, key financial statements and metrics, and how data analysis contributes to financial decision-making. The module emphasizes practical financial concepts relevant to data scientists rather than detailed accounting procedures.",
                "why_this_matters": "Financial constraints are a constant reality in healthcare, and data projects often need to demonstrate financial benefits. Understanding NHS funding helps you design analyses that address financial priorities, identify opportunities for cost savings or income generation, and communicate findings in ways that resonate with financial decision-makers.",
                "questions": [
                    "How does money flow from central government to front-line healthcare services?",
                    "What financial considerations influence healthcare decision-making at different levels?",
                    "How can data analysis support more effective resource allocation?",
                    "What financial metrics are most important for evaluating healthcare services?"
                ],
                "content_urls": [
                    {"title": "The King's Fund: NHS Finances and Funding", "url": "https://www.kingsfund.org.uk/topics/nhs-finances-funding"},
                    {"title": "NHS England: Financial Framework", "url": "https://www.england.nhs.uk/financial-accounting-and-reporting/"},
                    {"title": "Nuffield Trust: NHS Finances", "url": "https://www.nuffieldtrust.org.uk/research/the-nhs-financial-regime-in-england"},
                    {"title": "The Health Foundation: NHS Finances", "url": "https://www.health.org.uk/publications/reports/nhs-finances-the-challenges-all-political-parties-need-to-face"},
                    {"title": "NHS Providers: Finance Resources", "url": "https://nhsproviders.org/topics/finance"}
                ],
                "activities": [
                    "Analyze the financial statements of an NHS organization",
                    "Map the flow of funding for a specific healthcare service",
                    "Identify potential efficiency opportunities through data analysis",
                    "Design a dashboard to support resource allocation decisions"
                ]
            }
        ]
    },
    "being_part_of_healthcare_system": {
        "title": "Being Part of a Healthcare System",
        "key_metrics": ["Knowledge Management", "Stakeholder Engagement", "Communication Skills"],
        "description": "Understanding how to effectively work within and contribute to healthcare",
        "modules": [
            {
                "module_number": 1,
                "module_name": "Effectively Uncovering Information",
                "module_learning_outcomes": "1. Identifying stakeholders\n2. Accessing existing datasets\n3. Identifying and learning from pre-existing similar projects",
                "description": "This module focuses on how to navigate the healthcare information landscape to find and use existing knowledge and resources. You'll learn techniques for stakeholder mapping and engagement, approaches to discovering and accessing relevant datasets, methods for identifying related projects and learning from their experiences, and strategies for knowledge management in healthcare data science.",
                "why_this_matters": "Healthcare systems have vast amounts of existing knowledge and data that can inform your work. Effectively uncovering this information prevents duplication of effort, helps you build on previous successes, learn from past challenges, and connect with relevant experts and stakeholders. These skills help you work more efficiently and produce more valuable insights.",
                "questions": [
                    "How can you identify all the relevant stakeholders for a healthcare data project?",
                    "What approaches help you discover existing datasets that might be relevant to your work?",
                    "How can you learn from similar projects that have been conducted elsewhere?",
                    "What sources of information are most valuable for different types of healthcare data questions?"
                ],



                "activities": [
                    "Complete a stakeholder mapping exercise for a current project",
                    "Create a data inventory for your organization or department",
                    "Research similar projects through literature and NHS networks",
                    "Develop a knowledge management approach for your team"
                ]
            },
            {
                "module_number": 2,
                "module_name": "Glossary of NHS Abbreviations",
                "module_learning_outcomes": "1. Recognize 20 of the most commonly used NHS abbreviations you'll see in healthcare data\n2. Match common NHS abbreviations to their full terms when reviewing healthcare datasets\n3. Understand why knowing these abbreviations matters when working with healthcare data",
                "description": "This module introduces the specialized language and abbreviations commonly used in NHS contexts. You'll learn about organizational abbreviations (e.g., CCG, ICS, PCN), clinical abbreviations found in datasets (e.g., BP, HR, BMI), technical and system abbreviations (e.g., EPR, PAS, ESR), and policy-related terms (e.g., QOF, CQC, QIPP). The module provides context for when and how these abbreviations are used.",
                "why_this_matters": "NHS abbreviations appear frequently in healthcare data and discussions, and misunderstanding them can lead to confusion or errors. Familiarity with common abbreviations helps you interpret data correctly, communicate effectively with colleagues, and navigate NHS documentation and systems with confidence.",
                "questions": [
                    "Why do healthcare professionals use so many abbreviations?",
                    "How might abbreviations in data affect analysis and interpretation?",
                    "What strategies can help you keep track of unfamiliar abbreviations?",
                    "How do abbreviations vary between different healthcare contexts?"
                ],
                "content_urls": [
                    {"title": "NHS Data Dictionary", "url": "https://www.datadictionary.nhs.uk/"},
                    {"title": "NHS England: Acronym Buster", "url": "https://www.england.nhs.uk/participation/resources/involvementglossary/"},
                    {"title": "NHS Confederation: NHS Acronym Buster", "url": "https://www.nhsconfed.org/acronym-buster"},
                    {"title": "NICE Glossary", "url": "https://www.nice.org.uk/glossary"},
                    {"title": "NHS Digital Service Manual: Abbreviations", "url": "https://service-manual.nhs.uk/content/a-to-z-of-nhs-health-writing"}
                ],
                "activities": [
                    "Create flashcards of common NHS abbreviations to test your knowledge",
                    "Develop a personal glossary of abbreviations relevant to your work area",
                    "Review a healthcare dataset to identify and interpret all abbreviations",
                    "Practice explaining abbreviations in plain language for non-specialists"
                ]
            },
            {
                "module_number": 3,
                "module_name": "Communication Skills for Healthcare Data Scientists",
                "module_learning_outcomes": "1. Explain complex data findings to non-technical healthcare stakeholders using clear, jargon-free language\n2. Identify appropriate visualization techniques to present healthcare data insights effectively to different audiences\n3. Understand how to actively listen to clinical staff needs and translate them into actionable data questions",
                "description": "This module focuses on developing the communication skills needed to work effectively in healthcare environments. You'll learn about communicating with different healthcare audiences, translating technical concepts into accessible language, active listening techniques for understanding stakeholder needs, creating impactful data visualizations, and presenting findings in ways that drive action and decision-making.",
                "why_this_matters": "Communication skills are essential for healthcare data scientists to have impact. The ability to understand stakeholder needs, explain complex analyses clearly, and present insights compellingly helps ensure your work is understood, valued, and used to improve healthcare delivery and outcomes.",
                "questions": [
                    "How can you adapt your communication for different healthcare audiences?",
                    "What techniques help translate technical concepts into accessible language?",
                    "How can you ensure you're addressing the real needs of clinical stakeholders?",
                    "What visualization approaches are most effective for different types of healthcare data?"
                ],
                "content_urls": [
                    {"title": "NHS Digital Service Manual: Communication Guidelines", "url": "https://service-manual.nhs.uk/content/how-we-write"},
                    {"title": "The Health Foundation: Communicating Your Research", "url": "https://www.health.org.uk/publications/communications-in-healthcare-improvement-toolkit"},
                    {"title": "NHS England: Using Data Effectively", "url": "https://www.england.nhs.uk/publication/using-data-well/"},
                    {"title": "Understanding Patient Data: Communicating About Data", "url": "https://understandingpatientdata.org.uk/what-does-good-look-like/communicating-about-data"},
                    {"title": "Alan Turing Institute: Data Visualization for Healthcare", "url": "https://www.turing.ac.uk/research/research-projects/data-visualisation-healthcare"}
                ],
                "activities": [
                    "Practice explaining a complex analysis to colleagues with different backgrounds",
                    "Create a data visualization designed for a specific clinical audience",
                    "Attend a clinical meeting to practice active listening and needs identification",
                    "Develop a communication plan for a healthcare data project",
                    "Record yourself explaining a technical concept and review it for clarity and accessibility"
                ]
            }
        ]
    }
}
# Routes must come AFTER the nhs_domains variable is defined
@app.route('/')
def index():
    """Home page showing all domains/themes"""
    return render_template('index.html', domains=nhs_domains)

@app.route('/domain/<domain_id>')
def domain_detail(domain_id):
    """Domain detail page showing modules in a specific domain"""
    if domain_id in nhs_domains:
        return render_template('domain_detail.html', 
                              domain=nhs_domains[domain_id], 
                              domain_id=domain_id)
    else:
        return render_template('404.html'), 404

@app.route('/domain/<domain_id>/module/<int:module_number>')
def module_detail(domain_id, module_number):
    """Module detail page showing overview of a specific module"""
    if domain_id in nhs_domains:
        # Find the specific module
        module = next((m for m in nhs_domains[domain_id]['modules'] 
                      if m['module_number'] == module_number), None)
        
        if module:
            return render_template('module_detail.html',
                                  domain=nhs_domains[domain_id],
                                  domain_id=domain_id,
                                  module=module)
        
    return render_template('404.html'), 404

@app.route('/domain/<domain_id>/module/<int:module_number>/content')
def module_content(domain_id, module_number):
    """Content page showing detailed content for a specific module"""
    if domain_id in nhs_domains:
        # Find the specific module
        module = next((m for m in nhs_domains[domain_id]['modules'] 
                      if m['module_number'] == module_number), None)
        
        if module:
            return render_template('content_detail.html',
                                  domain=nhs_domains[domain_id],
                                  domain_id=domain_id,
                                  module=module)
        
    return render_template('404.html'), 404

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for AI assistant chat functionality"""
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

if __name__ == '__main__':
    app.run(debug=True)