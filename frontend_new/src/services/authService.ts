import api from './api';
import { AuthResponse, LoginCredentials, RegisterData, User } from '@/types';

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/auth/login/', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<{ message: string; user: User }> => {
    const response = await api.post('/api/auth/auth/register/student/', data);
    return response.data;
  },

  logout: async (refreshToken: string): Promise<void> => {
    await api.post('/api/auth/auth/logout/', { refresh: refreshToken });
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/auth/me/');
    return response.data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await api.put<User>('/api/auth/auth/update_profile/', data);
    return response.data;
  },

  changePassword: async (data: {
    old_password: string;
    new_password: string;
    new_password_confirm: string;
  }): Promise<{ message: string }> => {
    const response = await api.post('/api/auth/auth/change_password/', data);
    return response.data;
  },
};
