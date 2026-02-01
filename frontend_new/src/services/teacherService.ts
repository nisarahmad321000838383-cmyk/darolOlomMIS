import api from './api';
import { Teacher, PaginatedResponse, Student, TeacherAttendance } from '@/types';

export const teacherService = {
  getTeachers: async (params?: Record<string, any>): Promise<PaginatedResponse<Teacher>> => {
    const response = await api.get<PaginatedResponse<Teacher>>('/api/teachers/', { params });
    return response.data;
  },

  getTeacherById: async (id: number): Promise<Teacher> => {
    const response = await api.get<Teacher>(`/api/teachers/${id}/`);
    return response.data;
  },

  getCurrentTeacher: async (): Promise<Teacher> => {
    const response = await api.get<Teacher>('/api/teachers/me/');
    return response.data;
  },

  createTeacher: async (data: FormData | any): Promise<Teacher> => {
    const response = await api.post<Teacher>('/api/teachers/', data, {
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    });
    return response.data;
  },

  updateTeacher: async (id: number, data: FormData | any): Promise<Teacher> => {
    const response = await api.put<Teacher>(`/api/teachers/${id}/`, data, {
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    });
    return response.data;
  },

  deleteTeacher: async (id: number): Promise<void> => {
    await api.delete(`/api/teachers/${id}/`);
  },

  getTeacherStudents: async (id: number): Promise<Student[]> => {
    const response = await api.get<Student[]>(`/api/teachers/${id}/students/`);
    return response.data;
  },

  getTeacherAttendance: async (id: number): Promise<TeacherAttendance[]> => {
    const response = await api.get<TeacherAttendance[]>(`/api/teachers/${id}/attendance/`);
    return response.data;
  },

  getTeachersBySubject: async (subjectId: number): Promise<Teacher[]> => {
    const response = await api.get<Teacher[]>(`/api/teachers/by-subject/${subjectId}/`);
    return response.data;
  },

  getTeachersByClass: async (classId: number): Promise<Teacher[]> => {
    const response = await api.get<Teacher[]>(`/api/teachers/by-class/${classId}/`);
    return response.data;
  },
};
