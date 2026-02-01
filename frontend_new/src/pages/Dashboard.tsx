import React from 'react';
import { Users, GraduationCap, School, BookOpen, Calendar, CheckCircle } from 'lucide-react';
import { Card, CardHeader, CardContent } from '@/components/ui';
import { useAuthStore } from '@/store/authStore';

const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => {
  return (
    <Card>
      <CardContent className="flex items-center justify-between py-6">
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${color}`}>{icon}</div>
      </CardContent>
    </Card>
  );
};

export const Dashboard: React.FC = () => {
  const { user, isSuperAdmin, isAdmin, isTeacher, isStudent } = useAuthStore();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          Welcome back, {user?.name}!
        </p>
      </div>

      {/* Stats Grid */}
      {(isSuperAdmin() || isAdmin()) && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Students"
            value="0"
            icon={<GraduationCap className="h-6 w-6 text-white" />}
            color="bg-blue-500"
          />
          <StatCard
            title="Total Teachers"
            value="0"
            icon={<Users className="h-6 w-6 text-white" />}
            color="bg-green-500"
          />
          <StatCard
            title="Total Classes"
            value="0"
            icon={<School className="h-6 w-6 text-white" />}
            color="bg-purple-500"
          />
          <StatCard
            title="Total Subjects"
            value="0"
            icon={<BookOpen className="h-6 w-6 text-white" />}
            color="bg-orange-500"
          />
        </div>
      )}

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">Quick Actions</h2>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {!isStudent() && (
              <>
                <button className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors text-left">
                  <Calendar className="h-6 w-6 text-primary-600 mb-2" />
                  <p className="font-medium">Mark Attendance</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Record daily attendance
                  </p>
                </button>
                <button className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors text-left">
                  <CheckCircle className="h-6 w-6 text-primary-600 mb-2" />
                  <p className="font-medium">Enter Grades</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Update student scores
                  </p>
                </button>
              </>
            )}
            {(isSuperAdmin() || isAdmin()) && (
              <button className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-primary-500 dark:hover:border-primary-400 transition-colors text-left">
                <Users className="h-6 w-6 text-primary-600 mb-2" />
                <p className="font-medium">Pending Approvals</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Review student registrations
                </p>
              </button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">Recent Activity</h2>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 dark:text-gray-400">No recent activity</p>
        </CardContent>
      </Card>
    </div>
  );
};
