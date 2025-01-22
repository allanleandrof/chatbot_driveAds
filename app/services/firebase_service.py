from firebase_admin import firestore

class FirebaseService:
    def __init__(self):
        self.db = firestore.client()
    
    def check_cpf_exists(self, cpf):
        motorista_ref = self.db.collection('motoristas').where('cpf', '==', cpf).limit(1)
        results = motorista_ref.stream()
        for result in results:
            data = result.to_dict()
            nome_motorista = data.get('nome_motorista', 'Motorista')
            return True, nome_motorista
        return False, None