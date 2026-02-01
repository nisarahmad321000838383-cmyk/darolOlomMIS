import api from './api';
import { Document, PaginatedResponse } from '@/types';

export const documentService = {
  getDocuments: async (params?: Record<string, any>): Promise<PaginatedResponse<Document>> => {
    const response = await api.get<PaginatedResponse<Document>>('/api/documents/', { params });
    return response.data;
  },

  getDocumentById: async (id: number): Promise<Document> => {
    const response = await api.get<Document>(`/api/documents/${id}/`);
    return response.data;
  },

  uploadDocument: async (data: FormData): Promise<Document> => {
    const response = await api.post<Document>('/api/documents/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  updateDocument: async (id: number, data: FormData | Partial<Document>): Promise<Document> => {
    const response = await api.put<Document>(`/api/documents/${id}/`, data, {
      headers: data instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : undefined,
    });
    return response.data;
  },

  deleteDocument: async (id: number): Promise<void> => {
    await api.delete(`/api/documents/${id}/`);
  },

  getDocumentsByStudent: async (studentId: number): Promise<Document[]> => {
    const response = await api.get<Document[]>(`/api/documents/student/${studentId}/`);
    return response.data;
  },

  getDocumentsByTeacher: async (teacherId: number): Promise<Document[]> => {
    const response = await api.get<Document[]>(`/api/documents/teacher/${teacherId}/`);
    return response.data;
  },

  verifyDocument: async (
    id: number,
    isVerified: boolean
  ): Promise<{ message: string; document: Document }> => {
    const response = await api.post(`/api/documents/${id}/verify/`, {
      is_verified: isVerified,
    });
    return response.data;
  },

  getUnverifiedDocuments: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/api/documents/unverified/');
    return response.data;
  },
};
