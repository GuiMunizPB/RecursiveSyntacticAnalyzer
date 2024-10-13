from models.patient_record import PatientInfo, MedicalHistory, Consultation, PatientRecord

def parsedData_to_patient_record(parsed_data):
    patient_info = PatientInfo(
        name=parsed_data["patient_info"]["name"],
        age=parsed_data["patient_info"]["age"],
        gender=parsed_data["patient_info"]["gender"],
        patient_id=parsed_data["patient_info"]["patient_id"]
    )

    medical_history = [
        MedicalHistory(cond["condition"], cond["diagnosed_date"], cond["status"])
        for cond in parsed_data["medical_history"]
    ]

    consultations = [
        Consultation(cons["date"], cons["doctor"], cons["symptoms"], cons["diagnosis"])
        for cons in parsed_data["consultations"]
    ]

    return PatientRecord(patient_info, medical_history, consultations)
