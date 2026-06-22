<template>
  <div class="page-container" v-loading="loading">
    <div class="page-header">
      <div>
        <el-button type="text" icon="el-icon-arrow-left" @click="goBack">返回宠物档案</el-button>
        <h1 class="page-title" style="display: inline-block; margin-left: 12px;">
          就诊记录详情
        </h1>
      </div>
      <div>
        <el-button type="primary" icon="el-icon-edit" @click="editRecord">
          编辑病历
        </el-button>
      </div>
    </div>

    <div class="card-section" v-if="record && pet">
      <div class="info-grid" style="grid-template-columns: repeat(4, 1fr);">
        <div class="info-item">
          <span class="label">宠物名</span>
          <span class="value">{{ pet.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">品种</span>
          <span class="value">{{ pet.breed || pet.species }}</span>
        </div>
        <div class="info-item">
          <span class="label">就诊日期</span>
          <span class="value">{{ formatDate(record.visit_date) }}</span>
        </div>
        <div class="info-item">
          <span class="label">主人</span>
          <span class="value">{{ pet.owner_name }}</span>
        </div>
      </div>
    </div>

    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="主诉与病史" name="history">
        <div class="card-section">
          <h2 class="section-title">主诉信息</h2>
          <el-form label-width="100px">
            <el-form-item label="主诉">
              <el-input
                type="textarea"
                :value="record?.chief_complaint"
                :readonly="!editingHistory"
                :rows="2"
                v-model="historyForm.chief_complaint"
              />
            </el-form-item>
            <el-form-item label="现病史">
              <el-input
                type="textarea"
                :value="record?.present_illness"
                :readonly="!editingHistory"
                :rows="4"
                v-model="historyForm.present_illness"
              />
            </el-form-item>
            <el-form-item label="既往病史">
              <el-input
                type="textarea"
                :value="record?.past_illness"
                :readonly="!editingHistory"
                :rows="3"
                v-model="historyForm.past_illness"
              />
            </el-form-item>
            <el-form-item label="备注">
              <el-input
                type="textarea"
                :value="record?.notes"
                :readonly="!editingHistory"
                :rows="2"
                v-model="historyForm.notes"
              />
            </el-form-item>
            <el-form-item v-if="editingHistory">
              <el-button type="primary" @click="saveHistory">保存</el-button>
              <el-button @click="cancelEditHistory">取消</el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="card-section">
          <h2 class="section-title">过敏史</h2>
          <el-table :data="allergies" stripe v-if="allergies.length">
            <el-table-column prop="allergy_type" label="过敏类型" width="100">
              <template slot-scope="scope">
                <el-tag :type="getAllergyTagType(scope.row.allergy_type)" size="small">
                  {{ scope.row.allergy_type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="allergen" label="过敏原" width="150" />
            <el-table-column prop="reaction" label="反应症状" />
            <el-table-column prop="severity" label="严重程度" width="100">
              <template slot-scope="scope">
                <el-tag :type="getSeverityTagType(scope.row.severity)" size="small">
                  {{ scope.row.severity }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <el-empty description="暂无过敏史" v-else />
        </div>
      </el-tab-pane>

      <el-tab-pane label="临床检查" name="clinical">
        <div class="card-section">
          <div class="toolbar">
            <h2 class="section-title" style="margin-bottom: 0;">临床检查数据</h2>
            <div>
              <el-button v-if="!editingClinical && !clinicalExam" type="primary" size="small" icon="el-icon-plus" @click="startAddClinical">
                录入检查结果
              </el-button>
              <el-button v-if="!editingClinical && clinicalExam" type="primary" size="small" icon="el-icon-edit" @click="startEditClinical">
                编辑
              </el-button>
              <el-button v-if="editingClinical" size="small" @click="cancelEditClinical">
                取消
              </el-button>
            </div>
          </div>

          <el-form v-if="clinicalExam || editingClinical" label-width="140px">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="体温 (℃)">
                  <el-input-number
                    v-model="clinicalForm.temperature"
                    :min="35" :max="45" :step="0.1"
                    :disabled="!editingClinical"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="心率 (次/分)">
                  <el-input-number
                    v-model="clinicalForm.heart_rate"
                    :min="0" :max="300"
                    :disabled="!editingClinical"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="呼吸频率 (次/分)">
                  <el-input-number
                    v-model="clinicalForm.respiratory_rate"
                    :min="0" :max="100"
                    :disabled="!editingClinical"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="体重 (kg)">
                  <el-input-number
                    v-model="clinicalForm.weight"
                    :min="0" :max="200" :step="0.1"
                    :disabled="!editingClinical"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="体况评分 (1-9)">
                  <el-input-number
                    v-model="clinicalForm.body_condition_score"
                    :min="1" :max="9"
                    :disabled="!editingClinical"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="可视黏膜颜色">
                  <el-select v-model="clinicalForm.mucous_membrane_color" :disabled="!editingClinical" style="width: 100%;">
                    <el-option v-for="c in mucousMembraneColors" :key="c" :label="c" :value="c" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="淋巴结触诊">
              <el-input
                type="textarea"
                v-model="clinicalForm.lymph_node_abnormality"
                :rows="2"
                :disabled="!editingClinical"
                placeholder="描述淋巴结异常情况"
              />
            </el-form-item>
            <el-form-item label="心肺听诊">
              <el-input
                type="textarea"
                v-model="clinicalForm.cardio_pulmonary_auscultation"
                :rows="3"
                :disabled="!editingClinical"
                placeholder="描述心肺听诊结果"
              />
            </el-form-item>
            <el-form-item v-if="editingClinical">
              <el-button type="primary" @click="saveClinical">保存</el-button>
              <el-button @click="cancelEditClinical">取消</el-button>
            </el-form-item>
          </el-form>
          <el-empty description="暂无临床检查数据" v-else />
        </div>
      </el-tab-pane>

      <el-tab-pane label="实验室检查" name="lab">
        <div class="card-section">
          <div class="toolbar">
            <h2 class="section-title" style="margin-bottom: 0;">实验室检查</h2>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="openLabDialog">
              添加检查报告
            </el-button>
          </div>

          <el-collapse v-model="activeLabPanels" accordion>
            <el-collapse-item
              v-for="exam in labExams"
              :key="exam.id"
              :name="exam.id.toString()"
            >
              <template slot="title">
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                  <span>
                    <span style="font-weight: 500;">{{ exam.exam_type }}</span>
                    <span class="text-info" style="margin-left: 12px;">{{ formatDate(exam.created_at) }}</span>
                    <el-tag
                      v-if="exam.analysis?.has_abnormal"
                      type="danger"
                      size="mini"
                      style="margin-left: 12px;"
                    >
                      {{ exam.analysis.abnormal_count }}项异常
                    </el-tag>
                  </span>
                  <span>
                    <el-button size="mini" type="danger" @click.stop="deleteLabExam(exam)">删除</el-button>
                  </span>
                </div>
              </template>

              <el-table :data="getLabExamRows(exam)" stripe size="small">
                <el-table-column prop="name" label="项目" width="180" />
                <el-table-column prop="value" label="结果" width="120">
                  <template slot-scope="scope">
                    <span
                      :class="{
                        'abnormal-value': scope.row.is_abnormal,
                        'abnormal-low': scope.row.direction === 'low',
                        'abnormal-high': scope.row.direction === 'high'
                      }"
                    >
                      {{ scope.row.value }}
                    </span>
                    <span v-if="scope.row.unit" class="text-info" style="margin-left: 4px;">{{ scope.row.unit }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="reference_range" label="参考范围" width="180" />
                <el-table-column prop="message" label="状态" width="120">
                  <template slot-scope="scope">
                    <el-tag
                      v-if="scope.row.is_abnormal"
                      :type="scope.row.direction === 'low' ? 'primary' : 'danger'"
                      size="mini"
                    >
                      {{ scope.row.message }}
                    </el-tag>
                    <el-tag v-else type="success" size="mini">正常</el-tag>
                  </template>
                </el-table-column>
              </el-table>

              <el-form-item label="备注" style="margin-top: 16px;" v-if="exam.notes">
                <span>{{ exam.notes }}</span>
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <el-empty description="暂无实验室检查数据" v-if="!labExams.length" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="诊断管理" name="diagnosis">
        <div class="card-section">
          <div class="toolbar">
            <h2 class="section-title" style="margin-bottom: 0;">诊断结果</h2>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="openDiagnosisDialog">
              添加诊断
            </el-button>
          </div>

          <el-table :data="diagnoses" stripe v-if="diagnoses.length">
            <el-table-column prop="icd_code" label="ICD编码" width="120" />
            <el-table-column prop="diagnosis_name" label="诊断名称" min-width="200" />
            <el-table-column prop="severity_level" label="严重程度" width="120">
              <template slot-scope="scope">
                <el-tag :type="getSeverityTagType(scope.row.severity_level)" size="small">
                  {{ scope.row.severity_level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="notes" label="备注" />
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button size="mini" type="warning" @click="openDiagnosisDialog(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="deleteDiagnosis(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty description="暂无诊断记录" v-else />
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      title="添加实验室检查"
      :visible.sync="labDialogVisible"
      width="700px"
      @close="resetLabForm"
    >
      <el-form :model="labForm" :rules="labRules" ref="labForm" label-width="120px">
        <el-form-item label="检查类型" prop="exam_type">
          <el-select v-model="labForm.exam_type" placeholder="请选择检查类型" style="width: 100%;" @change="onExamTypeChange">
            <el-option v-for="t in examTypes" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>

        <div v-if="labForm.exam_type && referenceRanges">
          <div v-for="(range, key) in referenceRanges" :key="key" class="lab-input-row">
            <label class="lab-label">{{ range.name }}</label>
            <div class="lab-input-wrapper">
              <el-input
                v-model="labForm.result_data[key]"
                :placeholder="getPlaceholder(range)"
                size="small"
                style="width: 200px;"
              />
              <span class="lab-unit">{{ range.unit }}</span>
              <span class="lab-reference text-info">
                {{ getRangeText(range) }}
              </span>
            </div>
          </div>
        </div>

        <el-form-item label="备注">
          <el-input type="textarea" v-model="labForm.notes" :rows="2" placeholder="检查备注" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="labDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitLab">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      :title="diagnosisDialogTitle"
      :visible.sync="diagnosisDialogVisible"
      width="600px"
      @close="resetDiagnosisForm"
    >
      <el-form :model="diagnosisForm" :rules="diagnosisRules" ref="diagnosisForm" label-width="120px">
        <el-form-item label="ICD编码">
          <el-select
            v-model="diagnosisForm.icd_code"
            filterable
            remote
            reserve-keyword
            placeholder="搜索ICD编码或疾病名称"
            :remote-method="searchIcdCodes"
            :loading="icdLoading"
            style="width: 100%;"
          >
            <el-option
              v-for="item in icdOptions"
              :key="item.code"
              :label="`${item.code} - ${item.name}`"
              :value="item.code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="诊断名称" prop="diagnosis_name">
          <el-input v-model="diagnosisForm.diagnosis_name" placeholder="请输入诊断名称" />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity_level">
          <el-select v-model="diagnosisForm.severity_level" placeholder="请选择严重程度" style="width: 100%;">
            <el-option v-for="s in diagnosisSeverityLevels" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="diagnosisForm.notes" :rows="3" placeholder="治疗方案或其他备注" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="diagnosisDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDiagnosis">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  petsApi,
  allergiesApi,
  medicalRecordsApi,
  clinicalExamsApi,
  labExamsApi,
  diagnosesApi,
  constantsApi
} from '@/api'

export default {
  name: 'MedicalRecordDetail',
  data() {
    return {
      loading: false,
      record: null,
      pet: null,
      allergies: [],
      clinicalExam: null,
      labExams: [],
      diagnoses: [],
      activeTab: 'history',
      activeLabPanels: [],
      editingHistory: false,
      historyForm: {
        chief_complaint: '',
        present_illness: '',
        past_illness: '',
        notes: ''
      },
      editingClinical: false,
      isNewClinical: false,
      clinicalForm: {
        temperature: null,
        heart_rate: null,
        respiratory_rate: null,
        weight: null,
        body_condition_score: null,
        mucous_membrane_color: '',
        lymph_node_abnormality: '',
        cardio_pulmonary_auscultation: ''
      },
      mucousMembraneColors: [],
      examTypes: [],
      labDialogVisible: false,
      labForm: {
        exam_type: '',
        result_data: {},
        notes: ''
      },
      labRules: {
        exam_type: [{ required: true, message: '请选择检查类型', trigger: 'change' }]
      },
      referenceRanges: null,
      diagnosisDialogVisible: false,
      diagnosisDialogTitle: '添加诊断',
      diagnosisIsEdit: false,
      diagnosisEditId: null,
      diagnosisForm: {
        icd_code: '',
        diagnosis_name: '',
        severity_level: '',
        notes: ''
      },
      diagnosisRules: {
        diagnosis_name: [{ required: true, message: '请输入诊断名称', trigger: 'blur' }],
        severity_level: [{ required: true, message: '请选择严重程度', trigger: 'change' }]
      },
      diagnosisSeverityLevels: [],
      icdOptions: [],
      icdLoading: false
    }
  },
  async mounted() {
    this.mucousMembraneColors = await constantsApi.getMucousMembraneColors()
    this.examTypes = await constantsApi.getExamTypes()
    this.diagnosisSeverityLevels = await constantsApi.getDiagnosisSeverityLevels()
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const recordId = this.$route.params.recordId
        this.record = await medicalRecordsApi.get(recordId)
        this.pet = await petsApi.get(this.record.pet_id)
        this.allergies = await allergiesApi.list(this.record.pet_id)
        try {
          this.clinicalExam = await clinicalExamsApi.get(recordId)
        } catch (e) {
          this.clinicalExam = null
        }
        this.labExams = await labExamsApi.list(recordId)
        this.diagnoses = await diagnosesApi.list(recordId)
      } catch (e) {
        console.error('Failed to load data:', e)
      } finally {
        this.loading = false
      }
    },
    goBack() {
      if (this.pet) {
        this.$router.push(`/pets/${this.pet.id}`)
      } else {
        this.$router.push('/pets')
      }
    },
    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('zh-CN')
    },
    getAllergyTagType(type) {
      const map = { '药物': 'danger', '食物': 'warning', '跳蚤药': 'info', '环境': '', '其他': '' }
      return map[type] || ''
    },
    getSeverityTagType(severity) {
      const map = { '轻度': 'success', '中度': 'warning', '重度': 'danger', '危重': 'danger' }
      return map[severity] || ''
    },
    editRecord() {
      this.editingHistory = true
      this.historyForm = {
        chief_complaint: this.record.chief_complaint || '',
        present_illness: this.record.present_illness || '',
        past_illness: this.record.past_illness || '',
        notes: this.record.notes || ''
      }
    },
    async saveHistory() {
      try {
        await medicalRecordsApi.update(this.record.id, this.historyForm)
        this.$message.success('保存成功')
        this.editingHistory = false
        this.record = await medicalRecordsApi.get(this.record.id)
      } catch (e) {
        console.error('Save failed:', e)
      }
    },
    cancelEditHistory() {
      this.editingHistory = false
    },
    startAddClinical() {
      this.editingClinical = true
      this.isNewClinical = true
      this.clinicalForm = {
        temperature: null,
        heart_rate: null,
        respiratory_rate: null,
        weight: this.pet?.weight || null,
        body_condition_score: null,
        mucous_membrane_color: '',
        lymph_node_abnormality: '',
        cardio_pulmonary_auscultation: ''
      }
    },
    startEditClinical() {
      this.editingClinical = true
      this.isNewClinical = false
      this.clinicalForm = { ...this.clinicalExam }
    },
    async saveClinical() {
      try {
        if (this.isNewClinical) {
          await clinicalExamsApi.create(this.record.id, this.clinicalForm)
          this.$message.success('添加成功')
        } else {
          await clinicalExamsApi.update(this.clinicalExam.id, this.clinicalForm)
          this.$message.success('更新成功')
        }
        this.editingClinical = false
        this.clinicalExam = await clinicalExamsApi.get(this.record.id)
      } catch (e) {
        console.error('Save failed:', e)
      }
    },
    cancelEditClinical() {
      this.editingClinical = false
    },
    openLabDialog() {
      this.labDialogVisible = true
    },
    resetLabForm() {
      this.$refs.labForm?.resetFields()
      this.labForm = {
        exam_type: '',
        result_data: {},
        notes: ''
      }
      this.referenceRanges = null
    },
    async onExamTypeChange(examType) {
      this.labForm.result_data = {}
      this.referenceRanges = await constantsApi.getLabReferenceRanges(examType)
    },
    getPlaceholder(range) {
      if (range.normal && range.normal.length) {
        return `如: ${range.normal[0]}`
      }
      return '请输入结果'
    },
    getRangeText(range) {
      if (range.normal && range.normal.length) {
        return `正常: ${range.normal.join('/')}`
      }
      if (range.species === '通用') {
        return `${range.min}-${range.max}`
      }
      if (this.pet?.species === '犬' && range.min_dog !== undefined) {
        return `${range.min_dog}-${range.max_dog}`
      }
      if (this.pet?.species === '猫' && range.min_cat !== undefined) {
        return `${range.min_cat}-${range.max_cat}`
      }
      if (range.min !== undefined) {
        return `${range.min}-${range.max}`
      }
      return ''
    },
    async submitLab() {
      this.$refs.labForm.validate(async valid => {
        if (!valid) return
        try {
          await labExamsApi.create(this.record.id, this.labForm)
          this.$message.success('添加成功')
          this.labDialogVisible = false
          this.labExams = await labExamsApi.list(this.record.id)
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    async deleteLabExam(row) {
      this.$confirm('确定要删除这份检查报告吗？', '提示', { type: 'warning' }).then(async () => {
        try {
          await labExamsApi.delete(row.id)
          this.$message.success('删除成功')
          this.labExams = await labExamsApi.list(this.record.id)
        } catch (e) {
          console.error('Delete failed:', e)
        }
      }).catch(() => {})
    },
    getLabExamRows(exam) {
      if (!exam.analysis || !exam.analysis.analysis) {
        return Object.entries(exam.result_data || {}).map(([key, value]) => ({
          key,
          name: key,
          value,
          unit: '',
          reference_range: '-',
          is_abnormal: false,
          message: '-'
        }))
      }
      return Object.entries(exam.analysis.analysis).map(([key, analysis]) => ({
        key,
        name: analysis.reference,
        value: analysis.value,
        unit: analysis.unit,
        reference_range: analysis.reference_range || '-',
        is_abnormal: analysis.is_abnormal,
        direction: analysis.direction,
        message: analysis.message
      }))
    },
    openDiagnosisDialog(row = null) {
      if (row) {
        this.diagnosisIsEdit = true
        this.diagnosisEditId = row.id
        this.diagnosisDialogTitle = '编辑诊断'
        this.diagnosisForm = { ...row }
      } else {
        this.diagnosisIsEdit = false
        this.diagnosisDialogTitle = '添加诊断'
      }
      this.diagnosisDialogVisible = true
    },
    resetDiagnosisForm() {
      this.$refs.diagnosisForm?.resetFields()
      this.diagnosisForm = {
        icd_code: '',
        diagnosis_name: '',
        severity_level: '',
        notes: ''
      }
      this.diagnosisIsEdit = false
      this.diagnosisEditId = null
      this.icdOptions = []
    },
    async searchIcdCodes(query) {
      if (!query) {
        this.icdOptions = await constantsApi.getIcdCodes({})
        return
      }
      this.icdLoading = true
      try {
        this.icdOptions = await constantsApi.getIcdCodes({ search: query })
      } catch (e) {
        console.error('Search ICD failed:', e)
      } finally {
        this.icdLoading = false
      }
    },
    async submitDiagnosis() {
      this.$refs.diagnosisForm.validate(async valid => {
        if (!valid) return
        try {
          if (this.diagnosisIsEdit) {
            await diagnosesApi.update(this.diagnosisEditId, this.diagnosisForm)
            this.$message.success('更新成功')
          } else {
            await diagnosesApi.create(this.record.id, this.diagnosisForm)
            this.$message.success('添加成功')
          }
          this.diagnosisDialogVisible = false
          this.diagnoses = await diagnosesApi.list(this.record.id)
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    async deleteDiagnosis(row) {
      this.$confirm('确定要删除这条诊断记录吗？', '提示', { type: 'warning' }).then(async () => {
        try {
          await diagnosesApi.delete(row.id)
          this.$message.success('删除成功')
          this.diagnoses = await diagnosesApi.list(this.record.id)
        } catch (e) {
          console.error('Delete failed:', e)
        }
      }).catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.lab-input-row {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;

  .lab-label {
    width: 150px;
    font-size: 13px;
    color: #606266;
  }

  .lab-input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;

    .lab-unit {
      font-size: 12px;
      color: #606266;
      min-width: 40px;
    }

    .lab-reference {
      font-size: 12px;
    }
  }
}
</style>
