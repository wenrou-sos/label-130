<template>
  <div class="page-container" v-loading="loading">
    <div class="page-header">
      <div>
        <el-button type="text" icon="el-icon-arrow-left" @click="goBack">返回列表</el-button>
        <h1 class="page-title" style="display: inline-block; margin-left: 12px;">
          {{ pet?.name }} 的档案
        </h1>
      </div>
      <el-button type="primary" icon="el-icon-plus" @click="openRecordDialog">
        新建就诊记录
      </el-button>
    </div>

    <div class="card-section" v-if="pet">
      <h2 class="section-title">基本信息</h2>
      <div class="info-grid">
        <div class="info-item">
          <span class="label">宠物名</span>
          <span class="value">{{ pet.name }}</span>
        </div>
        <div class="info-item">
          <span class="label">物种</span>
          <span class="value">{{ pet.species }}</span>
        </div>
        <div class="info-item">
          <span class="label">品种</span>
          <span class="value">{{ pet.breed || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">性别</span>
          <span class="value">{{ pet.gender }}</span>
        </div>
        <div class="info-item">
          <span class="label">年龄</span>
          <span class="value">{{ pet.age ? pet.age + ' 岁' : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">体重</span>
          <span class="value">{{ pet.weight ? pet.weight + ' kg' : '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">毛色</span>
          <span class="value">{{ pet.fur_color || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="label">是否绝育</span>
          <span class="value">{{ pet.neutered ? '已绝育' : '未绝育' }}</span>
        </div>
        <div class="info-item">
          <span class="label">主人姓名</span>
          <span class="value">{{ pet.owner_name }}</span>
        </div>
        <div class="info-item">
          <span class="label">联系电话</span>
          <span class="value">{{ pet.owner_phone }}</span>
        </div>
        <div class="info-item">
          <span class="label">建档时间</span>
          <span class="value">{{ formatDate(pet.created_at) }}</span>
        </div>
      </div>
    </div>

    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="疫苗记录" name="vaccines">
        <div class="card-section">
          <div class="toolbar">
            <h3 class="section-title" style="margin-bottom: 0;">疫苗接种记录</h3>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="openVaccineDialog">
              添加疫苗记录
            </el-button>
          </div>
          <el-table :data="vaccines" stripe v-if="vaccines.length">
            <el-table-column prop="vaccine_type" label="疫苗类型" width="120" />
            <el-table-column prop="injection_date" label="接种日期" width="120">
              <template slot-scope="scope">{{ formatDate(scope.row.injection_date) }}</template>
            </el-table-column>
            <el-table-column prop="brand" label="品牌" width="120" />
            <el-table-column prop="batch_no" label="批号" width="140" />
            <el-table-column prop="next_date" label="下次接种日期" width="140">
              <template slot-scope="scope">{{ formatDate(scope.row.next_date) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button size="mini" type="warning" @click="openVaccineDialog(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="deleteVaccine(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty description="暂无疫苗记录" v-else />
        </div>
      </el-tab-pane>

      <el-tab-pane label="过敏史" name="allergies">
        <div class="card-section">
          <div class="toolbar">
            <h3 class="section-title" style="margin-bottom: 0;">过敏史记录</h3>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="openAllergyDialog">
              添加过敏记录
            </el-button>
          </div>
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
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button size="mini" type="warning" @click="openAllergyDialog(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="deleteAllergy(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty description="暂无过敏史记录" v-else />
        </div>
      </el-tab-pane>

      <el-tab-pane label="就诊记录" name="records">
        <div class="card-section">
          <div class="toolbar">
            <h3 class="section-title" style="margin-bottom: 0;">历史就诊记录</h3>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="openRecordDialog">
              新建就诊
            </el-button>
          </div>
          <el-table :data="medicalRecords" stripe v-if="medicalRecords.length">
            <el-table-column prop="id" label="编号" width="80" />
            <el-table-column prop="visit_date" label="就诊日期" width="120">
              <template slot-scope="scope">{{ formatDate(scope.row.visit_date) }}</template>
            </el-table-column>
            <el-table-column prop="chief_complaint" label="主诉" show-overflow-tooltip />
            <el-table-column label="诊断结果">
              <template slot-scope="scope">
                <span v-if="scope.row.diagnoses && scope.row.diagnoses.length">
                  {{ scope.row.diagnoses.map(d => d.diagnosis_name).join('、') }}
                </span>
                <span v-else class="text-info">待诊断</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button size="mini" type="primary" @click="goToRecordDetail(scope.row.id)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty description="暂无就诊记录" v-else />
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      :title="vaccineDialogTitle"
      :visible.sync="vaccineDialogVisible"
      width="500px"
      @close="resetVaccineForm"
    >
      <el-form :model="vaccineForm" :rules="vaccineRules" ref="vaccineForm" label-width="100px">
        <el-form-item label="疫苗类型" prop="vaccine_type">
          <el-select v-model="vaccineForm.vaccine_type" placeholder="请选择疫苗类型" filterable>
            <el-option v-for="t in vaccineTypes" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
        <el-form-item label="接种日期" prop="injection_date">
          <el-date-picker v-model="vaccineForm.injection_date" type="date" placeholder="选择日期" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="品牌">
          <el-input v-model="vaccineForm.brand" placeholder="请输入疫苗品牌" />
        </el-form-item>
        <el-form-item label="批号">
          <el-input v-model="vaccineForm.batch_no" placeholder="请输入疫苗批号" />
        </el-form-item>
        <el-form-item label="下次接种日期">
          <el-date-picker v-model="vaccineForm.next_date" type="date" placeholder="选择日期" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="vaccineDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitVaccine">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      :title="allergyDialogTitle"
      :visible.sync="allergyDialogVisible"
      width="500px"
      @close="resetAllergyForm"
    >
      <el-form :model="allergyForm" :rules="allergyRules" ref="allergyForm" label-width="100px">
        <el-form-item label="过敏类型" prop="allergy_type">
          <el-select v-model="allergyForm.allergy_type" placeholder="请选择过敏类型">
            <el-option v-for="t in allergyTypes" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
        <el-form-item label="过敏原" prop="allergen">
          <el-input v-model="allergyForm.allergen" placeholder="请输入过敏原" />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity">
          <el-select v-model="allergyForm.severity" placeholder="请选择严重程度">
            <el-option v-for="s in severityLevels" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="反应症状">
          <el-input type="textarea" v-model="allergyForm.reaction" :rows="3" placeholder="请描述过敏反应" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="allergyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAllergy">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="新建就诊记录"
      :visible.sync="recordDialogVisible"
      width="600px"
      @close="resetRecordForm"
    >
      <el-form :model="recordForm" :rules="recordRules" ref="recordForm" label-width="100px">
        <el-form-item label="就诊日期" prop="visit_date">
          <el-date-picker v-model="recordForm.visit_date" type="date" placeholder="选择日期" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="主诉">
          <el-input type="textarea" v-model="recordForm.chief_complaint" :rows="2" placeholder="请输入主诉" />
        </el-form-item>
        <el-form-item label="现病史">
          <el-input type="textarea" v-model="recordForm.present_illness" :rows="3" placeholder="请输入现病史" />
        </el-form-item>
        <el-form-item label="既往病史">
          <el-input type="textarea" v-model="recordForm.past_illness" :rows="3" placeholder="请输入既往病史" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="recordForm.notes" :rows="2" placeholder="其他备注" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="recordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRecord">确定并进入详情</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  petsApi,
  vaccinesApi,
  allergiesApi,
  medicalRecordsApi,
  constantsApi
} from '@/api'

export default {
  name: 'PetDetail',
  data() {
    return {
      loading: false,
      pet: null,
      vaccines: [],
      allergies: [],
      medicalRecords: [],
      activeTab: 'vaccines',
      vaccineTypes: [],
      allergyTypes: [],
      severityLevels: [],
      vaccineDialogVisible: false,
      vaccineDialogTitle: '添加疫苗记录',
      vaccineIsEdit: false,
      vaccineEditId: null,
      vaccineForm: {
        vaccine_type: '',
        injection_date: null,
        brand: '',
        batch_no: '',
        next_date: null
      },
      vaccineRules: {
        vaccine_type: [{ required: true, message: '请选择疫苗类型', trigger: 'change' }],
        injection_date: [{ required: true, message: '请选择接种日期', trigger: 'change' }]
      },
      allergyDialogVisible: false,
      allergyDialogTitle: '添加过敏记录',
      allergyIsEdit: false,
      allergyEditId: null,
      allergyForm: {
        allergy_type: '',
        allergen: '',
        reaction: '',
        severity: ''
      },
      allergyRules: {
        allergy_type: [{ required: true, message: '请选择过敏类型', trigger: 'change' }],
        allergen: [{ required: true, message: '请输入过敏原', trigger: 'blur' }],
        severity: [{ required: true, message: '请选择严重程度', trigger: 'change' }]
      },
      recordDialogVisible: false,
      recordForm: {
        visit_date: null,
        chief_complaint: '',
        present_illness: '',
        past_illness: '',
        notes: ''
      },
      recordRules: {
        visit_date: [{ required: true, message: '请选择就诊日期', trigger: 'change' }]
      }
    }
  },
  async mounted() {
    this.vaccineTypes = await constantsApi.getVaccineTypes()
    this.allergyTypes = await constantsApi.getAllergyTypes()
    this.severityLevels = await constantsApi.getSeverityLevels()
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const petId = this.$route.params.id
        this.pet = await petsApi.get(petId)
        this.vaccines = await vaccinesApi.list(petId)
        this.allergies = await allergiesApi.list(petId)
        this.medicalRecords = await medicalRecordsApi.list(petId)
      } catch (e) {
        console.error('Failed to load data:', e)
      } finally {
        this.loading = false
      }
    },
    goBack() {
      this.$router.push('/pets')
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
    openVaccineDialog(row = null) {
      if (row) {
        this.vaccineIsEdit = true
        this.vaccineEditId = row.id
        this.vaccineDialogTitle = '编辑疫苗记录'
        this.vaccineForm = { ...row, injection_date: row.injection_date ? new Date(row.injection_date) : null, next_date: row.next_date ? new Date(row.next_date) : null }
      } else {
        this.vaccineIsEdit = false
        this.vaccineDialogTitle = '添加疫苗记录'
      }
      this.vaccineDialogVisible = true
    },
    resetVaccineForm() {
      this.$refs.vaccineForm?.resetFields()
      this.vaccineForm = {
        vaccine_type: '',
        injection_date: null,
        brand: '',
        batch_no: '',
        next_date: null
      }
      this.vaccineIsEdit = false
      this.vaccineEditId = null
    },
    async submitVaccine() {
      this.$refs.vaccineForm.validate(async valid => {
        if (!valid) return
        try {
          if (this.vaccineIsEdit) {
            await vaccinesApi.update(this.vaccineEditId, this.vaccineForm)
            this.$message.success('更新成功')
          } else {
            await vaccinesApi.create(this.$route.params.id, this.vaccineForm)
            this.$message.success('添加成功')
          }
          this.vaccineDialogVisible = false
          this.vaccines = await vaccinesApi.list(this.$route.params.id)
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    async deleteVaccine(row) {
      this.$confirm('确定要删除这条疫苗记录吗？', '提示', { type: 'warning' }).then(async () => {
        try {
          await vaccinesApi.delete(row.id)
          this.$message.success('删除成功')
          this.vaccines = await vaccinesApi.list(this.$route.params.id)
        } catch (e) {
          console.error('Delete failed:', e)
        }
      }).catch(() => {})
    },
    openAllergyDialog(row = null) {
      if (row) {
        this.allergyIsEdit = true
        this.allergyEditId = row.id
        this.allergyDialogTitle = '编辑过敏记录'
        this.allergyForm = { ...row }
      } else {
        this.allergyIsEdit = false
        this.allergyDialogTitle = '添加过敏记录'
      }
      this.allergyDialogVisible = true
    },
    resetAllergyForm() {
      this.$refs.allergyForm?.resetFields()
      this.allergyForm = {
        allergy_type: '',
        allergen: '',
        reaction: '',
        severity: ''
      }
      this.allergyIsEdit = false
      this.allergyEditId = null
    },
    async submitAllergy() {
      this.$refs.allergyForm.validate(async valid => {
        if (!valid) return
        try {
          if (this.allergyIsEdit) {
            await allergiesApi.update(this.allergyEditId, this.allergyForm)
            this.$message.success('更新成功')
          } else {
            await allergiesApi.create(this.$route.params.id, this.allergyForm)
            this.$message.success('添加成功')
          }
          this.allergyDialogVisible = false
          this.allergies = await allergiesApi.list(this.$route.params.id)
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    async deleteAllergy(row) {
      this.$confirm('确定要删除这条过敏记录吗？', '提示', { type: 'warning' }).then(async () => {
        try {
          await allergiesApi.delete(row.id)
          this.$message.success('删除成功')
          this.allergies = await allergiesApi.list(this.$route.params.id)
        } catch (e) {
          console.error('Delete failed:', e)
        }
      }).catch(() => {})
    },
    openRecordDialog() {
      this.recordForm.visit_date = new Date()
      this.recordDialogVisible = true
    },
    resetRecordForm() {
      this.$refs.recordForm?.resetFields()
      this.recordForm = {
        visit_date: null,
        chief_complaint: '',
        present_illness: '',
        past_illness: '',
        notes: ''
      }
    },
    async submitRecord() {
      this.$refs.recordForm.validate(async valid => {
        if (!valid) return
        try {
          const record = await medicalRecordsApi.create(this.$route.params.id, this.recordForm)
          this.$message.success('创建成功')
          this.recordDialogVisible = false
          this.$router.push(`/medical-records/${record.id}/detail`)
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    goToRecordDetail(recordId) {
      this.$router.push(`/medical-records/${recordId}/detail`)
    }
  }
}
</script>
