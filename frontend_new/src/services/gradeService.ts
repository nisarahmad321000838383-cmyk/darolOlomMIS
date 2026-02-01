import api from './api';
import { StudentScore, PaginatedResponse } from '@/types';

export const gradeService = {
  getGrades: async (params?: Record<string, any>): Promise<PaginatedResponse<StudentScore>> => {
    const response = await api.get<PaginatedResponse<StudentScore>>('/api/grades/', { params });
    return response.data;
  },

  getGradeById: async (id: number): Promise<StudentScore> => {
    const response = await api.get<StudentScore>(`/api/grades/${id}/`);
    return response.data;
  },

  createGrade: async (data: Partial<StudentScore>): Promise<StudentScore> => {
    const response = await api.post<StudentScore>('/api/grades/', data);
    return response.data;
  },

  updateGrade: async (id: number, data: Partial<StudentScore>): Promise<StudentScore> => {
    const response = await api.put<StudentScore>(`/api/grades/${id}/`, data);
    return response.data;
  },

  deleteGrade: async (id: number): Promise<void> => {
    await api.delete(`/api/grades/${id}/`);
  },

  getGradesByStudent: async (studentId: number): Promise<StudentScore[]> => {
    const response = await api.get<StudentScore[]>(`/api/grades/student/${studentId}/`);
    return response.data;
  },

  getGradesBySubject: async (subjectId: number): Promise<StudentScore[]> => {
    const response = await api.get<StudentScore[]>(`/api/grades/subject/${subjectId}/`);
    return response.data;
  },

  getReportCard: async (studentId: number): Promise<any> => {
    const response = await api.get(`/api/grades/report-card/${studentId}/`);
    return response.data;
  },

  bulkCreateGrades: async (scores: Partial<StudentScore>[]): Promise<any> => {
    const response = await api.post('/api/grades/bulk-create/', { scores });
    return response.data;
  },
};
