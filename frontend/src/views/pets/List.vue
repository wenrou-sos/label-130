<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">宠物管理</h1>
      <el-button type="primary" icon="el-icon-plus" @click="openCreateDialog">
        新建宠物档案
      </el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" @submit.native.prevent>
        <el-form-item label="物种">
          <el-select v-model="searchForm.species" placeholder="全部" clearable>
            <el-option label="犬" value="犬" />
            <el-option label="猫" value="猫" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="宠物名/主人名/电话"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="loadPets">
            搜索
          </el-button>
          <el-button icon="el-icon-refresh" @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card-section">
      <el-table :data="pets" v-loading="loading" stripe>
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column prop="name" label="宠物名" width="120" />
        <el-table-column prop="species" label="物种" width="80" />
        <el-table-column prop="breed" label="品种" width="140" />
        <el-table-column prop="gender" label="性别" width="80">
          <template slot-scope="scope">
            <el-tag :type="scope.row.gender === '公' ? 'primary' : 'danger'" size="small">
              {{ scope.row.gender }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄(岁)" width="100" />
        <el-table-column prop="weight" label="体重(kg)" width="100" />
        <el-table-column prop="owner_name" label="主人姓名" width="120" />
        <el-table-column prop="owner_phone" label="联系电话" width="140" />
        <el-table-column label="是否绝育" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.neutered ? 'success' : 'info'" size="small">
              {{ scope.row.neutered ? '已绝育' : '未绝育' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="goToDetail(scope.row.id)">
              详情
            </el-button>
            <el-button size="mini" type="warning" @click="openEditDialog(scope.row)">
              编辑
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        />
      </div>
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="petForm" :rules="formRules" ref="petForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="宠物名" prop="name">
              <el-input v-model="petForm.name" placeholder="请输入宠物名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="物种" prop="species">
              <el-select v-model="petForm.species" placeholder="请选择物种" @change="onSpeciesChange">
                <el-option label="犬" value="犬" />
                <el-option label="猫" value="猫" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="品种" prop="breed">
              <el-select v-model="petForm.breed" placeholder="请选择品种" filterable>
                <el-option
                  v-for="breed in breedOptions"
                  :key="breed"
                  :label="breed"
                  :value="breed"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="petForm.gender" placeholder="请选择性别">
                <el-option label="公" value="公" />
                <el-option label="母" value="母" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄">
              <el-input-number v-model="petForm.age" :min="0" :max="50" :step="0.1" placeholder="岁" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="体重">
              <el-input-number v-model="petForm.weight" :min="0" :max="200" :step="0.1" placeholder="kg" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="毛色">
              <el-input v-model="petForm.fur_color" placeholder="请输入毛色" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否绝育">
              <el-switch v-model="petForm.neutered" active-text="是" inactive-text="否" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="主人姓名" prop="owner_name">
              <el-input v-model="petForm.owner_name" placeholder="请输入主人姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="owner_phone">
              <el-input v-model="petForm.owner_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { petsApi, constantsApi } from '@/api'

export default {
  name: 'PetList',
  data() {
    return {
      loading: false,
      pets: [],
      pagination: {
        page: 1,
        page_size: 20,
        total: 0
      },
      searchForm: {
        species: '',
        search: ''
      },
      dialogVisible: false,
      dialogTitle: '新建宠物档案',
      isEdit: false,
      editId: null,
      breedOptions: [],
      petForm: {
        name: '',
        species: '',
        breed: '',
        gender: '',
        age: null,
        weight: null,
        fur_color: '',
        neutered: false,
        owner_name: '',
        owner_phone: ''
      },
      formRules: {
        name: [{ required: true, message: '请输入宠物名', trigger: 'blur' }],
        species: [{ required: true, message: '请选择物种', trigger: 'change' }],
        gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
        owner_name: [{ required: true, message: '请输入主人姓名', trigger: 'blur' }],
        owner_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }]
      }
    }
  },
  async mounted() {
    await this.loadPets()
  },
  methods: {
    async loadPets() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.page_size,
          ...this.searchForm
        }
        if (!params.species) delete params.species
        if (!params.search) delete params.search
        
        const res = await petsApi.list(params)
        this.pets = res.items
        this.pagination.total = res.total
      } catch (e) {
        console.error('Failed to load pets:', e)
      } finally {
        this.loading = false
      }
    },
    resetSearch() {
      this.searchForm = { species: '', search: '' }
      this.pagination.page = 1
      this.loadPets()
    },
    handleSizeChange(val) {
      this.pagination.page_size = val
      this.loadPets()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadPets()
    },
    async onSpeciesChange(species) {
      if (species) {
        this.breedOptions = await constantsApi.getBreeds(species)
      } else {
        this.breedOptions = []
      }
      this.petForm.breed = ''
    },
    openCreateDialog() {
      this.isEdit = false
      this.dialogTitle = '新建宠物档案'
      this.dialogVisible = true
    },
    async openEditDialog(row) {
      this.isEdit = true
      this.editId = row.id
      this.dialogTitle = '编辑宠物档案'
      await this.onSpeciesChange(row.species)
      this.petForm = { ...row }
      this.dialogVisible = true
    },
    resetForm() {
      this.$refs.petForm?.resetFields()
      this.petForm = {
        name: '',
        species: '',
        breed: '',
        gender: '',
        age: null,
        weight: null,
        fur_color: '',
        neutered: false,
        owner_name: '',
        owner_phone: ''
      }
      this.breedOptions = []
      this.isEdit = false
      this.editId = null
    },
    async submitForm() {
      this.$refs.petForm.validate(async valid => {
        if (!valid) return
        
        try {
          if (this.isEdit) {
            await petsApi.update(this.editId, this.petForm)
            this.$message.success('更新成功')
          } else {
            await petsApi.create(this.petForm)
            this.$message.success('创建成功')
          }
          this.dialogVisible = false
          this.loadPets()
        } catch (e) {
          console.error('Submit failed:', e)
        }
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除宠物「${row.name}」吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await petsApi.delete(row.id)
          this.$message.success('删除成功')
          this.loadPets()
        } catch (e) {
          console.error('Delete failed:', e)
        }
      }).catch(() => {})
    },
    goToDetail(id) {
      this.$router.push(`/pets/${id}`)
    }
  }
}
</script>

<style lang="scss" scoped>
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
