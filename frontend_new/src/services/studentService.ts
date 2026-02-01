import api from './api';
import { Student, PaginatedResponse, StudentScore, StudentAttendance, Document } from '@/types';

export const studentService = {
  getStudents: async (params?: Record<string, any>): Promise<PaginatedResponse<Student>> => {
    const response = await api.get<PaginatedResponse<Student>>('/api/students/', { params });
    return response.data;
  },

  getStudentById: async (id: number): Promise<Student> => {
    const response = await api.get<Student>(`/api/students/${id}/`);
    return response.data;
  },

  getCurrentStudent: async (): Promise<Student> => {
    const response = await api.get<Student>('/api/students/me/');
    return response.data;
  },

  createStudent: async (data: FormData | any): Promise<Student> => {
    const response = await api.post<Student>('/api/students/', data, {
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    });
    return response.data;
  },

  updateStudent: async (id: number, data: FormData | any): Promise<Student> => {
    const response = await api.put<Student>(`/api/students/${id}/`, data, {
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    });
    return response.data;
  },

  deleteStudent: async (id: number): Promise<void> => {
    await api.delete(`/api/students/${id}/`);
  },

  getStudentGrades: async (id: number): Promise<StudentScore[]> => {
    const response = await api.get<StudentScore[]>(`/api/students/${id}/grades/`);
    return response.data;
  },

  getStudentAttendance: async (id: number): Promise<StudentAttendance[]> => {
    const response = await api.get<StudentAttendance[]>(`/api/students/${id}/attendance/`);
    return response.data;
  },

  getStudentDocuments: async (id: number): Promise<Document[]> => {
    const response = await api.get<Document[]>(`/api/students/${id}/documents/`);
    return response.data;
  },

  getStudentsByClass: async (classId: number): Promise<Student[]> => {
    const response = await api.get<Student[]>(`/api/students/by-class/${classId}/`);
    return response.data;
  },
};
