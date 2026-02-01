import api from './api';
import { Semester, SchoolClass, Subject, Student } from '@/types';

export const academicService = {
  // Semesters
  getSemesters: async (): Promise<Semester[]> => {
    const response = await api.get<Semester[]>('/api/academics/semesters/');
    return response.data;
  },

  getSemesterById: async (id: number): Promise<Semester> => {
    const response = await api.get<Semester>(`/api/academics/semesters/${id}/`);
    return response.data;
  },

  createSemester: async (data: Partial<Semester>): Promise<Semester> => {
    const response = await api.post<Semester>('/api/academics/semesters/', data);
    return response.data;
  },

  updateSemester: async (id: number, data: Partial<Semester>): Promise<Semester> => {
    const response = await api.put<Semester>(`/api/academics/semesters/${id}/`, data);
    return response.data;
  },

  deleteSemester: async (id: number): Promise<void> => {
    await api.delete(`/api/academics/semesters/${id}/`);
  },

  // Classes
  getClasses: async (params?: Record<string, any>): Promise<SchoolClass[]> => {
    const response = await api.get<SchoolClass[]>('/api/academics/classes/', { params });
    return response.data;
  },

  getClassById: async (id: number): Promise<SchoolClass> => {
    const response = await api.get<SchoolClass>(`/api/academics/classes/${id}/`);
    return response.data;
  },

  createClass: async (data: Partial<SchoolClass>): Promise<SchoolClass> => {
    const response = await api.post<SchoolClass>('/api/academics/classes/', data);
    return response.data;
  },

  updateClass: async (id: number, data: Partial<SchoolClass>): Promise<SchoolClass> => {
    const response = await api.put<SchoolClass>(`/api/academics/classes/${id}/`, data);
    return response.data;
  },

  deleteClass: async (id: number): Promise<void> => {
    await api.delete(`/api/academics/classes/${id}/`);
  },

  getClassStudents: async (id: number): Promise<Student[]> => {
    const response = await api.get<Student[]>(`/api/academics/classes/${id}/students/`);
    return response.data;
  },

  // Subjects
  getSubjects: async (params?: Record<string, any>): Promise<Subject[]> => {
    const response = await api.get<Subject[]>('/api/academics/subjects/', { params });
    return response.data;
  },

  getSubjectById: async (id: number): Promise<Subject> => {
    const response = await api.get<Subject>(`/api/academics/subjects/${id}/`);
    return response.data;
  },

  createSubject: async (data: Partial<Subject>): Promise<Subject> => {
    const response = await api.post<Subject>('/api/academics/subjects/', data);
    return response.data;
  },

  updateSubject: async (id: number, data: Partial<Subject>): Promise<Subject> => {
    const response = await api.put<Subject>(`/api/academics/subjects/${id}/`, data);
    return response.data;
  },

  deleteSubject: async (id: number): Promise<void> => {
    await api.delete(`/api/academics/subjects/${id}/`);
  },

  getSubjectsBySemester: async (semesterId: number): Promise<Subject[]> => {
    const response = await api.get<Subject[]>(`/api/academics/subjects/by-semester/${semesterId}/`);
    return response.data;
  },
};
