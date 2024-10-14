class PatientRecord:
    def __init__(self, patient_info, medical_history, consultations):
        self.patient_info = patient_info  # instância de PatientInfo
        self.medical_history = medical_history  # lista de MedicalHistory
        self.consultations = consultations  # lista de Consultation

    def __repr__(self):
        return f"PatientRecord(info={self.patient_info}, history={self.medical_history}, consultations={self.consultations})"


class PatientInfo:
    def __init__(self, name, age, gender, patient_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.patient_id = patient_id

    def __repr__(self):
        return f"PatientInfo(name='{self.name}', age={self.age}, gender='{self.gender}', patient_id='{self.patient_id}')"

class MedicalHistory:
    def __init__(self, condition, diagnosed_date, status):
        self.condition = condition
        self.diagnosed_date = diagnosed_date
        self.status = status

    def __repr__(self):
        return f"MedicalHistory(condition='{self.condition}', diagnosed_date='{self.diagnosed_date}', status='{self.status}')"


class Consultation:
    def __init__(self, date, doctor, symptoms, diagnosis):
        self.date = date
        self.doctor = doctor
        self.symptoms = symptoms
        self.diagnosis = diagnosis

    def __repr__(self):
        return f"Consultation(date='{self.date}', doctor='{self.doctor}', symptoms='{self.symptoms}', diagnosis='{self.diagnosis}')"
