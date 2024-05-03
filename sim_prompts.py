output_format = """

# Case Study: {{case_title}}
## Clinical Dashboard - Pertinent History and Physical

### Paragraph Summary of Case:
- **Paragraph Summary**: {{paragraph_summary}}

### Patient Approach:
- **Education Level**: `{{patient_education_level}}`
- **Emotional Response**: `{{emotional_response}}`
- **Communication Style**: `{{communication_style}}`

### History of Present Illness (HPI):
- **Onset**: `{{onset}}`
- **Location**: `{{location}}`
- **Duration**: `{{duration}}`
- **Character**: `{{character}}`
- **Aggravating/Alleviating Factors**: `{{aggravating_alleviating}}`
- **Radiation**: `{{radiation}}`
- **Timing**: `{{timing}}`
- **Severity**: `{{severity}}`
- **Additional Details**: `{{other_hpi_details}}`

### Past Medical History (PMHx):
- **Active Problems**: `{{active_problems}}`
- **Inactive Problems**: `{{inactive_problems}}`
- **Hospitalizations**: `{{hospitalizations}}`
- **Surgical History**: `{{surgical_history}}`
- **Immunizations**: `{{immunizations}}`

### Social History (SHx):
- **Tobacco**: `{{tobacco_use}}`
- **Alcohol**: `{{alcohol_use}}`
- **Substances**: `{{substance_use}}`
- **Diet**: `{{diet}}`
- **Exercise**: `{{exercise}}`
- **Sexual Activity**: `{{sexual_activity}}`
- **Home Life/Safety**: `{{home_safety}}`
- **Mood**: `{{mood}}`
- **Contextual Details**: `{{context_additional}}`

### Family History (FHx):
- **Parents**: `{{parents_health_status}}`
- **Siblings**: `{{siblings_health_status}}`

### Medications and Allergies:
- **Medications**: `{{medications_details}}`
- **Allergies**: `{{allergies_details}}`

### Review of Systems (ROS):
- **Pertinent Findings**: `{{ros_details}}`

### Physical Examination:
- **Findings**: `{{physical_exam_details}}`

### Diagnostic Reasoning:
- **Differential Diagnoses**: `{{differential_diagnoses}}`
- **Rationale**: `{{diagnostic_reasoning}}`

### Teaching Points:
- **Key Learning Objectives**: `{{learning_objectives}}`
- **Educational Content**: `{{educational_content}}`

---

## PATIENT DOOR CHART and Learner Instructions

- **Patient Name**: `{{patient_name}}`
- **Age**: `{{age}}`
- **Gender**: `{{gender}}`
- **Chief Complaint**: `{{chief_complaint}}`
- **Clinical Setting**: `{{setting}}`

### Vital Signs:
- **Blood Pressure Reading**: `{{blood_pressure}}`
- **Pulse Rate**: `{{pulse}}`
- **Respiratory Rate**: `{{respiratory_rate}}`
- **Temperature(Celsius)**: `{{temperature}}`
- **SpO2**: `{{spo2}}`
"""

output_format_json = """{
    "case_id": 1,
    "title": "45 Year Old Man with Upper Abdominal Pain and Vomiting",
    "description": "A 45-year-old man presents to the Emergency Department complaining of severe upper abdominal pain that radiates to the back, accompanied by nausea and vomiting.",
    "chief_complaint": "upper abdominal pain",
    "setting": "Emergency Department",
    "patient": {
      "name": "Marcus Johnson",
      "age": 45,
      "gender": "Male"
    },
    "hpi": {
      "onset": "Sudden onset, 4 hours before presenting",
      "provocation_palliation": "Pain not relieved by any position or over-the-counter pain medications",
      "quality": "Severe, stabbing",
      "radiation": "Radiates to the back",
      "severity": "9/10 on the pain scale",
      "timing": "Constant",
      "location": "Upper abdomen",
      "assoc_symptoms": "Nausea and vomiting, the vomitus contains food but no blood. Fever of 38.5°C (101.3°F)"
    },
    "pmh": {
      "prior_occurence": "No",
      "med_conditions": [
        "History of hyperlipidemia and alcohol use disorder"
      ],
      "hospitalizations": "None",
      "surgeries": "None",
      "ob_gyn_history": "Not applicable",
      "medications": [
        "Atorvastatin"
      ],
      "med_compliance": "Poor, often forgets doses",
      "allergies": "No known drug allergies",
      "vaccines": "Up-to-date"
    },
    "family_history": {
      "conditions": "Father with type 2 diabetes mellitus, mother with hypertension"
    },
    "social_history": {
      "risk_factors": "High-fat diet, regular alcohol consumption (3-4 drinks/day)",
      "diet": "High in fats, prefers fast food",
      "exercise": "Sedentary lifestyle",
      "drugs": "Denies illegal drug use",
      "tobacco": "Smokes half a pack of cigarettes per day",
      "alcohol": "Regular, heavy",
      "household_composition": "Lives with partner",
      "occupation": "Office job, mostly sedentary",
      "sexually_active": "Yes, monogamous relationship",
      "mental_health": "Reports occasional stress, no history of depression or anxiety",
      "sleep": "Occasional insomnia, self-reports 6 hours of sleep on average"
    },
    "sections": [
      {
        "title": "Section One",
        "points": 15,
        "findings": [],
        "questions": [
          "Based on the history you gathered from the patient, what is your current differential diagnosis in order of priority? List at least 3 possible diagnoses.",
          "Justify your top three diagnoses by listing pertinent positives and negatives.",
          "What physical exam findings would you expect to find for your top differential diagnosis?"
        ]
      },
      {
        "title": "Section Two",
        "points": 20,
        "findings": [
          {
            "title": "Vitals",
            "findings": "BP: 150/90, HR: 110 bpm, RR: 22 bpm, Temp: 38.5°C (101.3°F), o2sat: 97% on room air"
          },
          {
            "title": "General",
            "findings": "Patient appears uncomfortable, grimacing"
          },
          {
            "title": "Cardiovascular",
            "findings": "Tachycardia, normal rhythm, no murmurs"
          },
          {
            "title": "Respiratory",
            "findings": "Rapid respirations but clear to auscultation bilaterally"
          },
          {
            "title": "Abdominal",
            "findings": "Diffuse tenderness in the upper abdomen with guarding, no rebound tenderness. No masses palpable."
          },
          {
            "title": "Extremities",
            "findings": "No cyanosis, clubbing or edema"
          },
          {
            "title": "Neurologic",
            "findings": "Alert and oriented x3, no focal deficits"
          }
        ],
        "questions": [
          "Based on the history and physical exam findings, please list your current differential diagnosis in order of priority. List at least 3 possible diagnoses.",
          "Justify your top three diagnoses by listing pertinent positives and negatives.",
          "Based on the history and physical exam findings, please write a summary statement for the patient?",
          "What additional labs, imaging, or diagnostic studies would you like to order?"
        ]
      },
      {
        "title": "Section Three",
        "points": 15,
        "findings": [
          {
            "title": "Complete blood count (CBC)",
            "findings": "HB: 14 g/dL, WBC: 16 x 10^9/L, PLT: 300 x 10^9/L"
          },
          {
            "title": "Liver function tests (LFTs)",
            "findings": "AST: 250 U/L, ALT: 230 U/L, ALP: 120 U/L, Bilirubin total: 1.5 mg/dL, Albumin: 3.5 g/dL"
          },
          {
            "title": "Lipase",
            "findings": "800 U/L (normal <60 U/L)"
          },
          {
            "title": "Abdominal ultrasound",
            "findings": "Gallbladder normal, no stones, pancreas appears swollen with no clear evidence of gallstones"
          },
          {
            "title": "CT abdomen/pelvis with contrast",
            "findings": "Diffuse enlargement of the pancreas with peripancreatic fat stranding suggestive of pancreatitis, no gallstones seen"
          }
        ],
        "questions": [
          "Based on the additional information provided above, what is the most likely diagnosis and why?",
          "Based on the additional information provided above, please list two other possible diagnoses and why they are less likely than your leading diagnosis.",
          "What is the next step(s) in management?"
        ]
      }
    ],
    "diagnosis": {
      "actual": "Acute pancreatitis",
      "differential": [
        "Cholecystitis",
        "Peptic ulcer disease",
        "Hepatitis",
        "Gastroenteritis",
        "Myocardial infarction"
      ]
    },
    "case_summary": "This was a case of acute pancreatitis in a middle-aged male who presented with sudden onset of severe, stabbing upper abdominal pain that radiated to the back, accompanied by nausea, vomiting, and fever. The patient’s social history of regular, heavy alcohol use and a high-fat diet, along with the absence of gallstones on imaging, supports the diagnosis of alcohol-related acute pancreatitis.\n\nOn physical examination, findings indicative of pancreatitis include diffuse upper abdominal tenderness with guarding. Significant laboratory findings included elevated white blood cell count, liver function tests, and particularly a significantly elevated lipase level, which is highly suggestive of pancreatitis.\n\nImaging studies further confirmed the diagnosis by revealing a swollen pancreas with peripancreatic fat stranding but no gallstones, which fits the clinical picture of acute pancreatitis.\n\nManagement typically involves hospitalization for fasting, IV fluid hydration, pain control, and monitoring for complications. Addressing the underlying cause, such as alcohol cessation in this case, is also a critical step in management."
  }
  """