import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/authViews/LoginView.vue'
import AdminDashView from '@/views/adminViews/AdminDashView.vue'
import AllStudentView from '@/views/adminViews/AllStudentView.vue'
import AllCompanyView from '@/views/adminViews/AllCompanyView.vue'
import AllDrivesView from '@/views/adminViews/AllDrivesView.vue'
import AllApplicationsView from '@/views/adminViews/AllApplicationsView.vue'
import CompanyDashView from '@/views/companyViews/CompanyView.vue'
import StudentDashView from '@/views/studentViews/StudentView.vue'
import StudentProfileView from '@/views/commonViews/StudentProfileView.vue'
import CompanyProfileView from '@/views/commonViews/CompanyProfileView.vue'
import DriveProfileView from '@/views/commonViews/DriveProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashView,
    },
    {
      path: '/admin/students',
      name: 'admin-students',
      component: AllStudentView,
    },
    {
      path: '/admin/companies',
      name: 'admin-companies',
      component: AllCompanyView,
    },
    {
      path: '/admin/drives',
      name: 'admin-drives',
      component: AllDrivesView,
    },
    {
      path: '/admin/applications',
      name: 'admin-applications',
      component: AllApplicationsView,
    },
    {
      path: '/company/dashboard',
      name: 'company-dashboard',
      component: CompanyDashView,
    },
    {
      path: '/student/dashboard',
      name: 'student-dashboard',
      component: StudentDashView,
    },
    {
      path: '/student/profile/:userid',
      name: 'student-profile',
      component: StudentProfileView,
    },
    {
      path: '/company/profile/:companyid',
      name: 'company-profile',
      component: CompanyProfileView,
    },
    {
      path: '/drive/profile/:driveid',
      name: 'drive-profile',
      component: DriveProfileView,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userJson = localStorage.getItem('user')

  if (to.path === '/login') {
    if (token && userJson) {
      try {
        const user = JSON.parse(userJson)
        if (user.role === 'admin') {
          return next('/admin/dashboard')
        } else if (user.role === 'student') {
          return next('/student/dashboard')
        } else if (user.role === 'recruiter') {
          return next('/company/dashboard')
        }
      } catch (e) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      }
    }
    return next()
  }

  if (!token) {
    return next('/login')
  }

  if (userJson) {
    try {
      const user = JSON.parse(userJson)
      if (to.path.startsWith('/admin') && user.role !== 'admin') {
        return next('/login')
      }
      if (to.path.startsWith('/student') && user.role !== 'student') {
        if (to.name === 'student-profile' && (user.role === 'admin' || user.role === 'recruiter')) {
          // Allow admin and recruiter to view student profile
        } else {
          return next('/login')
        }
      }
      if (to.path.startsWith('/company') && user.role !== 'recruiter') {
        if (to.name === 'company-profile' && (user.role === 'admin' || user.role === 'student')) {
          // Allow admin and student to view company profile
        } else {
          return next('/login')
        }
      }
    } catch (e) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      return next('/login')
    }
  }

  next()
})

export default router
