import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { UserPlus, School } from 'lucide-react';
import { Button, Input, Select, Card, CardContent } from '@/components/ui';
import { authService } from '@/services/authService';
import { ROUTES, GENDER_OPTIONS } from '@/utils/constants';
import toast from 'react-hot-toast';

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  password_confirm: z.string(),
  name: z.string().min(1, 'Name is required'),
  father_name: z.string().optional(),
  gender: z.enum(['male', 'female']),
  email: z.string().email('Invalid email').optional().or(z.literal('')),
  phone_number: z.string().optional(),
}).refine((data) => data.password === data.password_confirm, {
  message: "Passwords don't match",
  path: ['password_confirm'],
});

type RegisterForm = z.infer<typeof registerSchema>;

export const Register: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      gender: 'male',
    },
  });

  const onSubmit = async (data: RegisterForm) => {
    setLoading(true);
    try {
      await authService.register(data);
      toast.success('Registration successful! Please wait for approval.');
      navigate(ROUTES.LOGIN);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <Card className="w-full max-w-2xl">
        <CardContent className="pt-6">
          <div className="flex flex-col items-center mb-6">
            <School className="h-16 w-16 text-primary-600 mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Student Registration
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Register your account and wait for approval
            </p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Username"
                {...register('username')}
                error={errors.username?.message}
                placeholder="Choose a username"
                required
              />

              <Input
                label="Full Name"
                {...register('name')}
                error={errors.name?.message}
                placeholder="Your full name"
                required
              />

              <Input
                label="Father's Name"
                {...register('father_name')}
                error={errors.father_name?.message}
                placeholder="Father's name"
              />

              <Select
                label="Gender"
                {...register('gender')}
                error={errors.gender?.message}
                options={GENDER_OPTIONS}
                required
              />

              <Input
                label="Email"
                type="email"
                {...register('email')}
                error={errors.email?.message}
                placeholder="your.email@example.com"
              />

              <Input
                label="Phone Number"
                {...register('phone_number')}
                error={errors.phone_number?.message}
                placeholder="+93 700 123 456"
              />

              <Input
                label="Password"
                type="password"
                {...register('password')}
                error={errors.password?.message}
                placeholder="Create a password"
                required
              />

              <Input
                label="Confirm Password"
                type="password"
                {...register('password_confirm')}
                error={errors.password_confirm?.message}
                placeholder="Confirm your password"
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              loading={loading}
              leftIcon={<UserPlus className="h-4 w-4" />}
            >
              Register
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <p className="text-gray-600 dark:text-gray-400">
              Already have an account?{' '}
              <Link
                to={ROUTES.LOGIN}
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                Login here
              </Link>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
