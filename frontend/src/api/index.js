import request from '@/utils/request'

export const petsApi = {
  list(params) {
    return request({ url: '/pets', method: 'get', params })
  },
  get(id) {
    return request({ url: `/pets/${id}`, method: 'get' })
  },
  create(data) {
    return request({ url: '/pets', method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/pets/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/pets/${id}`, method: 'delete' })
  }
}

export const vaccinesApi = {
  list(petId) {
    return request({ url: `/pets/${petId}/vaccines`, method: 'get' })
  },
  create(petId, data) {
    return request({ url: `/pets/${petId}/vaccines`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/vaccines/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/vaccines/${id}`, method: 'delete' })
  }
}

export const allergiesApi = {
  list(petId) {
    return request({ url: `/pets/${petId}/allergies`, method: 'get' })
  },
  create(petId, data) {
    return request({ url: `/pets/${petId}/allergies`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/allergies/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/allergies/${id}`, method: 'delete' })
  }
}

export const medicalRecordsApi = {
  list(petId) {
    return request({ url: `/pets/${petId}/medical-records`, method: 'get' })
  },
  get(id) {
    return request({ url: `/medical-records/${id}`, method: 'get' })
  },
  create(petId, data) {
    return request({ url: `/pets/${petId}/medical-records`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/medical-records/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/medical-records/${id}`, method: 'delete' })
  }
}

export const clinicalExamsApi = {
  get(recordId) {
    return request({ url: `/medical-records/${recordId}/clinical-exam`, method: 'get' })
  },
  create(recordId, data) {
    return request({ url: `/medical-records/${recordId}/clinical-exam`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/clinical-exams/${id}`, method: 'put', data })
  }
}

export const labExamsApi = {
  list(recordId) {
    return request({ url: `/medical-records/${recordId}/lab-exams`, method: 'get' })
  },
  create(recordId, data) {
    return request({ url: `/medical-records/${recordId}/lab-exams`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/lab-exams/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/lab-exams/${id}`, method: 'delete' })
  },
  analyze(recordId, examType, resultData) {
    return request({
      url: `/constants/analyze-lab-exam/${recordId}`,
      method: 'post',
      params: { exam_type: examType },
      data: resultData
    })
  }
}

export const diagnosesApi = {
  list(recordId) {
    return request({ url: `/medical-records/${recordId}/diagnoses`, method: 'get' })
  },
  create(recordId, data) {
    return request({ url: `/medical-records/${recordId}/diagnoses`, method: 'post', data })
  },
  update(id, data) {
    return request({ url: `/diagnoses/${id}`, method: 'put', data })
  },
  delete(id) {
    return request({ url: `/diagnoses/${id}`, method: 'delete' })
  }
}

export const constantsApi = {
  getBreeds(species) {
    return request({ url: '/constants/breeds', method: 'get', params: { species } })
  },
  getVaccineTypes() {
    return request({ url: '/constants/vaccine-types', method: 'get' })
  },
  getAllergyTypes() {
    return request({ url: '/constants/allergy-types', method: 'get' })
  },
  getSeverityLevels() {
    return request({ url: '/constants/severity-levels', method: 'get' })
  },
  getDiagnosisSeverityLevels() {
    return request({ url: '/constants/diagnosis-severity-levels', method: 'get' })
  },
  getMucousMembraneColors() {
    return request({ url: '/constants/mucous-membrane-colors', method: 'get' })
  },
  getExamTypes() {
    return request({ url: '/constants/exam-types', method: 'get' })
  },
  getLabReferenceRanges(examType) {
    return request({ url: '/constants/lab-reference-ranges', method: 'get', params: { exam_type: examType } })
  },
  getIcdCodes(params) {
    return request({ url: '/constants/icd-codes', method: 'get', params })
  },
  getIcdCategories() {
    return request({ url: '/constants/icd-categories', method: 'get' })
  }
}
