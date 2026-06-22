<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">宠物医院电子病历管理系统</h1>
    </div>

    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon pet-icon">
            <i class="el-icon-dog"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.petCount }}</div>
            <div class="stat-label">宠物总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon record-icon">
            <i class="el-icon-document"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.recordCount }}</div>
            <div class="stat-label">病历总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon vaccine-icon">
            <i class="el-icon-s-goods"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.vaccineCount }}</div>
            <div class="stat-label">疫苗记录</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon exam-icon">
            <i class="el-icon-edit-outline"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.examCount }}</div>
            <div class="stat-label">检查记录</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="card-section">
          <h2 class="section-title">快速操作</h2>
          <div class="quick-actions">
            <el-button type="primary" size="large" icon="el-icon-plus" @click="goToPets">
              新建宠物档案
            </el-button>
            <el-button type="success" size="large" icon="el-icon-search" @click="goToPets">
              查询宠物信息
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card-section">
          <h2 class="section-title">系统功能</h2>
          <div class="feature-list">
            <div class="feature-item">
              <i class="el-icon-dog"></i>
              <div>
                <div class="feature-title">宠物建档</div>
                <div class="feature-desc">品种、性别、年龄、疫苗、过敏史</div>
              </div>
            </div>
            <div class="feature-item">
              <i class="el-icon-document"></i>
              <div>
                <div class="feature-title">病历管理</div>
                <div class="feature-desc">主诉、现病史、既往病史记录</div>
              </div>
            </div>
            <div class="feature-item">
              <i class="el-icon-s-check"></i>
              <div>
                <div class="feature-title">临床检查</div>
                <div class="feature-desc">体温、心率、心肺听诊等</div>
              </div>
            </div>
            <div class="feature-item">
              <i class="el-icon-data-line"></i>
              <div>
                <div class="feature-title">实验室检查</div>
                <div class="feature-desc">血常规、生化、异常值标红</div>
              </div>
            </div>
            <div class="feature-item">
              <i class="el-icon-edit"></i>
              <div>
                <div class="feature-title">诊断管理</div>
                <div class="feature-desc">ICD编码、病情分级</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { petsApi } from '@/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        petCount: 0,
        recordCount: 0,
        vaccineCount: 0,
        examCount: 0
      }
    }
  },
  async mounted() {
    await this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        const res = await petsApi.list({ page: 1, page_size: 1 })
        this.stats.petCount = res.total || 0
      } catch (e) {
        console.error('Failed to load stats:', e)
      }
    },
    goToPets() {
      this.$router.push('/pets')
    }
  }
}
</script>

<style lang="scss" scoped>
.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

  .stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: #fff;

    &.pet-icon {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    &.record-icon {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    &.vaccine-icon {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    &.exam-icon {
      background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
  }

  .stat-content {
    .stat-value {
      font-size: 28px;
      font-weight: bold;
      color: #303133;
    }

    .stat-label {
      font-size: 14px;
      color: #909399;
    }
  }
}

.quick-actions {
  display: flex;
  gap: 16px;
  flex-direction: column;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .feature-item {
    display: flex;
    align-items: center;
    gap: 12px;

    i {
      font-size: 24px;
      color: #409EFF;
    }

    .feature-title {
      font-size: 14px;
      font-weight: 600;
      color: #303133;
    }

    .feature-desc {
      font-size: 12px;
      color: #909399;
    }
  }
}
</style>
