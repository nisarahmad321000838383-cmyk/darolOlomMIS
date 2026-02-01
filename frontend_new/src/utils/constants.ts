export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  ADMIN: 'ADMIN',
  TEACHER: 'TEACHER',
  STUDENT: 'STUDENT',
} as const;

export const APPROVAL_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
} as const;

export const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
];

export const EXAM_TYPES = [
  { value: 'midterm', label: 'Midterm' },
  { value: 'final', label: 'Final' },
  { value: 'quiz', label: 'Quiz' },
  { value: 'assignment', label: 'Assignment' },
];

export const ATTENDANCE_STATUS = [
  { value: 'present', label: 'Present', color: 'green' },
  { value: 'absent', label: 'Absent', color: 'red' },
  { value: 'late', label: 'Late', color: 'yellow' },
  { value: 'excused', label: 'Excused', color: 'blue' },
];

export const EDUCATION_LEVELS = [
  { value: 'p', label: 'چهارده پاس' },
  { value: 'b', label: 'لیسانس (Bachelor)' },
  { value: 'm', label: 'ماستر (Master)' },
  { value: 'd', label: 'دوکتور (PhD)' },
];

export const DOCUMENT_TYPES = [
  { value: 'certificate', label: 'Certificate' },
  { value: 'transcript', label: 'Transcript' },
  { value: 'id_document', label: 'ID Document' },
  { value: 'medical', label: 'Medical' },
  { value: 'letter', label: 'Letter' },
  { value: 'contract', label: 'Contract' },
  { value: 'other', label: 'Other' },
];

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  
  // Students
  STUDENTS: '/students',
  STUDENT_DETAIL: '/students/:id',
  STUDENT_CREATE: '/students/new',
  STUDENT_EDIT: '/students/:id/edit',
  
  // Teachers
  TEACHERS: '/teachers',
  TEACHER_DETAIL: '/teachers/:id',
  TEACHER_CREATE: '/teachers/new',
  TEACHER_EDIT: '/teachers/:id/edit',
  
  // Academics
  CLASSES: '/classes',
  SUBJECTS: '/subjects',
  SEMESTERS: '/semesters',
  
  // Grades
  GRADES: '/grades',
  GRADE_ENTRY: '/grades/entry',
  
  // Attendance
  ATTENDANCE_STUDENTS: '/attendance/students',
  ATTENDANCE_TEACHERS: '/attendance/teachers',
  
  // Documents
  DOCUMENTS: '/documents',
  
  // Admin
  USERS: '/users',
  PENDING_APPROVALS: '/users/pending',
  PERMISSIONS: '/permissions',
  
  // Profile
  PROFILE: '/profile',
  SETTINGS: '/settings',
} as const;
