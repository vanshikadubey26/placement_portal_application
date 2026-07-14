import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/authViews/LoginView.vue'
import StudentSignupView from '@/views/authViews/StudentSignupView.vue'
import CompanySignupView from '@/views/authViews/CompanySignupView.vue'
import AdminDashView from '@/views/adminViews/AdminDashView.vue'
import AllStudentView from '@/views/adminViews/AllStudentView.vue'
import AllCompanyView from '@/views/adminViews/AllCompanyView.vue'
import AllDrivesView from '@/views/adminViews/AllDrivesView.vue'
import AllApplicationsView from '@/views/adminViews/AllApplicationsView.vue'
import CompanyDashView from '@/views/companyViews/CompanyDashView.vue'
import CompanyProfileEditView from '@/views/companyViews/CompanyProfileEditView.vue'
import CompanyDrivesView from '@/views/companyViews/CompanyDrivesView.vue'
import CompanyApplicationsView from '@/views/companyViews/CompanyApplicationsView.vue'
import CompanyInterviewsView from '@/views/companyViews/CompanyInterviewsView.vue'
import CreateDriveForm from '@/views/companyViews/CreateDriveForm.vue'
import CompanyShortlistedView from '@/views/companyViews/CompanyShortlistedView.vue'
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
      path: '/signup/student',
      name: 'student-signup',
      component: StudentSignupView,
    },
    {
      path: '/signup/company',
      name: 'company-signup',
      component: CompanySignupView,
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
      path: '/company/profile',
      name: 'company-profile-edit',
      component: CompanyProfileEditView,
    },
    {
      path: '/company/drives',
      name: 'company-drives',
      component: CompanyDrivesView,
    },
    {
      path: '/company/drives/create',
      name: 'company-drives-create',
      component: CreateDriveForm,
    },
    {
      path: '/company/applications',
      name: 'company-applications',
      component: CompanyApplicationsView,
    },
    {
      path: '/company/shortlisted',
      name: 'company-shortlisted',
      component: CompanyShortlistedView,
    },
    {
      path: '/company/interviews',
      name: 'company-interviews',
      component: CompanyInterviewsView,
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
    {
      path: '/company/dashboard',
      name: 'company-dashboard',
      component: CompanyDashView,
    }
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userJson = localStorage.getItem('user')

  if (to.path === '/login' || to.path === '/signup/student' || to.path === '/signup/company') {
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
