import api from './api';
import { StudentAttendance, TeacherAttendance, AttendanceStats, PaginatedResponse } from '@/types';

export const attendanceService = {
  // Student Attendance
  getStudentAttendance: async (
    params?: Record<string, any>
  ): Promise<PaginatedResponse<StudentAttendance>> => {
    const response = await api.get<PaginatedResponse<StudentAttendance>>(
      '/api/attendance/students/',
      { params }
    );
    return response.data;
  },

  getStudentAttendanceById: async (id: number): Promise<StudentAttendance> => {
    const response = await api.get<StudentAttendance>(`/api/attendance/students/${id}/`);
    return response.data;
  },

  markStudentAttendance: async (data: Partial<StudentAttendance>): Promise<StudentAttendance> => {
    const response = await api.post<StudentAttendance>('/api/attendance/students/', data);
    return response.data;
  },

  updateStudentAttendance: async (
    id: number,
    data: Partial<StudentAttendance>
  ): Promise<StudentAttendance> => {
    const response = await api.put<StudentAttendance>(`/api/attendance/students/${id}/`, data);
    return response.data;
  },

  deleteStudentAttendance: async (id: number): Promise<void> => {
    await api.delete(`/api/attendance/students/${id}/`);
  },

  getStudentAttendanceByStudent: async (
    studentId: number,
    params?: Record<string, any>
  ): Promise<StudentAttendance[]> => {
    const response = await api.get<StudentAttendance[]>(
      `/api/attendance/students/student/${studentId}/`,
      { params }
    );
    return response.data;
  },

  getStudentAttendanceStats: async (
    studentId: number,
    params?: Record<string, any>
  ): Promise<AttendanceStats> => {
    const response = await api.get<AttendanceStats>(
      `/api/attendance/students/stats/${studentId}/`,
      { params }
    );
    return response.data;
  },

  bulkMarkStudentAttendance: async (attendances: Partial<StudentAttendance>[]): Promise<any> => {
    const response = await api.post('/api/attendance/students/bulk-mark/', { attendances });
    return response.data;
  },

  // Teacher Attendance
  getTeacherAttendance: async (
    params?: Record<string, any>
  ): Promise<PaginatedResponse<TeacherAttendance>> => {
    const response = await api.get<PaginatedResponse<TeacherAttendance>>(
      '/api/attendance/teachers/',
      { params }
    );
    return response.data;
  },

  getTeacherAttendanceById: async (id: number): Promise<TeacherAttendance> => {
    const response = await api.get<TeacherAttendance>(`/api/attendance/teachers/${id}/`);
    return response.data;
  },

  markTeacherAttendance: async (data: Partial<TeacherAttendance>): Promise<TeacherAttendance> => {
    const response = await api.post<TeacherAttendance>('/api/attendance/teachers/', data);
    return response.data;
  },

  updateTeacherAttendance: async (
    id: number,
    data: Partial<TeacherAttendance>
  ): Promise<TeacherAttendance> => {
    const response = await api.put<TeacherAttendance>(`/api/attendance/teachers/${id}/`, data);
    return response.data;
  },

  deleteTeacherAttendance: async (id: number): Promise<void> => {
    await api.delete(`/api/attendance/teachers/${id}/`);
  },

  getTeacherAttendanceByTeacher: async (
    teacherId: number,
    params?: Record<string, any>
  ): Promise<TeacherAttendance[]> => {
    const response = await api.get<TeacherAttendance[]>(
      `/api/attendance/teachers/teacher/${teacherId}/`,
      { params }
    );
    return response.data;
  },

  getTeacherAttendanceStats: async (
    teacherId: number,
    params?: Record<string, any>
  ): Promise<AttendanceStats> => {
    const response = await api.get<AttendanceStats>(
      `/api/attendance/teachers/stats/${teacherId}/`,
      { params }
    );
    return response.data;
  },
};
