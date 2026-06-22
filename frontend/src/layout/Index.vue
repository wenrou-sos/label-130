<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <i class="el-icon-plus"></i>
        <span>宠物医院EMR</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :router="true"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          <i class="el-icon-s-home"></i>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/pets">
          <i class="el-icon-dog"></i>
          <span>宠物管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item
              v-for="item in breadcrumbs"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="user-info">
          <i class="el-icon-user-solid"></i>
          <span>管理员</span>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'Layout',
  data() {
    return {
      breadcrumbMap: {
        '/dashboard': { title: '首页', path: '/dashboard' },
        '/pets': { title: '宠物管理', path: '/pets' }
      }
    }
  },
  computed: {
    activeMenu() {
      const path = this.$route.path
      if (path.startsWith('/pets/')) return '/pets'
      return path
    },
    breadcrumbs() {
      const path = this.$route.path
      const crumbs = []
      if (path === '/dashboard') {
        crumbs.push({ title: '首页', path: '/dashboard' })
      } else if (path === '/pets') {
        crumbs.push({ title: '首页', path: '/dashboard' })
        crumbs.push({ title: '宠物管理', path: '/pets' })
      } else if (path.startsWith('/pets/')) {
        crumbs.push({ title: '首页', path: '/dashboard' })
        crumbs.push({ title: '宠物管理', path: '/pets' })
        crumbs.push({ title: '宠物详情', path: '' })
      } else if (path.startsWith('/medical-records/')) {
        crumbs.push({ title: '首页', path: '/dashboard' })
        crumbs.push({ title: '宠物管理', path: '/pets' })
        crumbs.push({ title: '病历详情', path: '' })
      }
      return crumbs
    }
  }
}
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.sidebar {
  background-color: #304156;
  height: 100%;
  overflow: hidden;

  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 16px;
    font-weight: bold;
    background-color: #2b2f3a;

    i {
      font-size: 24px;
      margin-right: 8px;
    }
  }

  ::v-deep .el-menu {
    border-right: none;
  }
}

.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #606266;
  }
}

.main-content {
  padding: 0;
  background-color: #f0f2f5;
  overflow: hidden;
}
</style>
